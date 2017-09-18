# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from posts.models import Post
# Create your models here.
class Votes(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	post = models.ForeignKey(Post)
	value = models.BooleanField()
	timestamp = models.DateTimeField(auto_now_add = True)
