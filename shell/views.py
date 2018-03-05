# -*- coding: utf-8 -*-
import itertools
from operator import itemgetter

from django.views.generic import TemplateView, ListView

from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView,CreateView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from opslib_boto3.ec2 import EC2Instance
from opslib_boto3.base import regions_get, env_get

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

import json
from django.utils.timezone import now
from shell.models import SshLog
from shell.interactive import get_redis_instance

REGIONS = regions_get()

# Create your views here.


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())

def ec2_list_instances(region, role, version=None, build=None, state=None, env='ops'):
    ec2 = EC2Instance(region=region, env=env)

    instances = ec2.instance_list(role=role, version=version, build=build, state=state)

    select_instances = []
    for instance in instances:
        tags = instance.get('Tags', [])
        id = instance.get('InstanceId', '')
        type = instance.get('InstanceType')
        tag_name = [tag.get('Value') for tag in tags if tag.get('Key') == 'Name'][0]
        tag_version = None
        name_list = tag_name.split('-')
        for value in name_list:
            if value == '20':
                tag_version = '20'
                break
            if value == '30':
                tag_version = '30'
                break

        public_ip = instance.get('PublicIpAddress', '')
        private_ip = instance.get('PrivateIpAddress', '')
        key_pair = instance.get('KeyName', '')
        state = instance.get('State', {}).get('Name', '')

        select_instances.append({
            'name': tag_name,
            'tag_version': tag_version,
            'public_ip' : public_ip,
            'private_ip': private_ip,
            'key_pair': key_pair,
            'state' : state
        })

    return select_instances


class SshTerminalKill(LoginRequiredMixin, View):
    login_required = True

    def post(self, request):
        if request.is_ajax():
            channel_name = request.POST.get('channel_name', None)
            try:
                data = SshLog.objects.get(channel=channel_name)
                if data.is_finished:
                    return JsonResponse({'status': False, 'message': 'Ssh terminal does not exist!'})
                else:
                    data.end_time = now()
                    data.is_finished = True
                    data.save()

                    queue = get_redis_instance()
                    redis_channel = queue.pubsub()
                    queue.publish(channel_name, json.dumps(['close']))

                    return JsonResponse({'status': True, 'message': 'Terminal has been killed !'})
            except ObjectDoesNotExist:
                return JsonResponse({'status': False, 'message': 'Request object does not exist!'})


class IndexView(LoginRequiredMixin, TemplateView):
    login_required = True
    template_name = 'base.html'


class ServerListView(LoginRequiredMixin, ListView):
    queryset = []
    login_required = True
    template_name = 'shell/server_list.html'

    def get_context_data(self, **kwargs):
        context = super(ServerListView, self).get_context_data(**kwargs)
        region = self.kwargs['region']
        role = self.kwargs['role']

        select_instances = ec2_list_instances(region=region, role=role)
        prod_select_instances = ec2_list_instances(region=region, role=role, env='pro')

        select_instances = sorted(select_instances, key=lambda k:k['name'])
        prod_select_instances = sorted(prod_select_instances, key=lambda k: k['name'])

        context['servers_ops'] =[]
        context['servers_prod'] = []

        for key, value in itertools.groupby(select_instances, key=itemgetter('name')):
            context['servers_ops'].append({
                'name': key,
                'servers': list(value)
            })

        for key, value in itertools.groupby(prod_select_instances, key=itemgetter('name')):
            context['servers_prod'].append({
                'name': key,
                'servers': list(value)
            })

        return context
