from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

from django.conf import settings


class Topic(models.Model):
    topic_name = models.CharField(max_length=50)

    def __str__(self):
        return self.topic_name


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='authorized_blogs')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=50)
    body = HTMLField()
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, name='liked_blogs', blank=True)
    image = models.ImageField(upload_to='blog_images/',null=True , blank=True)
    

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,default=1)
    body = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.body
