# -*- coding: utf-8 -*-
import os
import random
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
def upload(instance, filename):
    file_name = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    return os.path.join(settings.UPLOAD_TO, file_name)


def random_default_avatar():
    default = random.randint(1, 46)
    return "upload/default/%02d.png" % (default)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    role = models.CharField(choices=(('QA', 'QA'), ('Admin', 'Admin'), ('DEV', 'DEV'), ('SEG', 'SEG'), ('OPS', 'OPS')),
                            max_length=8,
                            default='DEV')
    avatar = models.ImageField("avatar", upload_to=upload, default='upload/default.png')

    def __str__(self):
        return self.user.username
