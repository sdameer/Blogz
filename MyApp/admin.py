from django.contrib import admin

from .models import Blog, Topic , Message 
admin.site.register(Blog)
admin.site.register(Topic)
admin.site.register(Message)
