# -*- coding: utf-8 -*-
import random
from django import template

from shell.models import Region

register = template.Library()


@register.inclusion_tag('sidebar.html', takes_context=True)
def render_sidebar(context):
    return {
        'request': context['request'],
        'regions': Region.objects.all(),
    }