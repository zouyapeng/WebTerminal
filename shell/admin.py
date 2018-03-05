# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Role,Region, SshLog, Credential

# Register your models here.
admin.site.register(Role)
admin.site.register(Region)
admin.site.register(SshLog)
admin.site.register(Credential)
