from django.forms import ModelForm
from .models import Blog ,User

class UserForm(ModelForm):
    
    class Meta:
        model = User
        fields = ['email','bio','image']


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'body', 'topic', 'image']
