# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, ListView

from django.shortcuts import render

# Create your views here.


class IndexView(TemplateView):
    template_name = 'base.html'

class ServerListView(ListView):
    queryset = []
    template_name = 'shell/server_list.html'

    def get_context_data(self, **kwargs):
        context = super(ServerListView, self).get_context_data(**kwargs)
        region = self.kwargs['region']
        role = self.kwargs['role']
        context['20servers'] = ['111','222','3333']
        context['30servers'] = ['111', '222', '3333']
        # context['notice'] = Category.objects.last()
        return context
