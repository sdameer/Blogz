from django.db import models
from tinymce.models import HTMLField
from cloudinary.models import CloudinaryField
from django.conf import settings

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(null=True)
    image = models.ImageField(upload_to='blog_images/', null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Topic(models.Model):
    topic_name = models.CharField(max_length=50)

    def __str__(self):
        return self.topic_name


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='authorized_blogs')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)

    name = models.CharField(max_length=50)
    body = HTMLField()
    # image = models.ImageField(upload_to='blog_images/',null=True , blank=True)
    image = CloudinaryField('image', folder='blog_images/', blank=True, null=True)

    

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
