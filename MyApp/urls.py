from django.urls import path
from .views import *


urlpatterns = [
    
    path('add_blog', post , name='add_blog'),
    path('update_blog/<str:pk>', update , name='update_blog'),
    path('delete_blog/<str:pk>', delete , name='delete_blog'),
    path('blog_body/<str:pk>', blog_body , name='blog_body'),
    path('user/<str:pk>', users , name='user'),
    path('delete_msg/<str:pk>', delete_msg , name='delete_msg'),
    path('contactus', contact_us, name='contact_us'),
    path('develpoer_page', developer_page, name='developer_page'),
    path('genai',genai_title,name='genai'),
    
]
