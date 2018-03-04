# -*- coding: utf-8 -*-
import random
from django import template

from shell.models import Region

register = template.Library()


@register.inclusion_tag('sidebar.html')
def render_sidebar():
    return {
        'regions': Region.objects.all(),
    }