# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
class Post(models.Model):
	title = models.CharField(max_length=500)
	image = models.FileField(null=True, blank=True)
	author = models.CharField(max_length=200)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"id" : self.id})

	class Meta:
		ordering = ["-id"]

	@property 
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type

