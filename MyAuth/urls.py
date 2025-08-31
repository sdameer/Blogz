from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name='login_page'),
    path('register/', register, name='register_page'),
    path('logout/', logout_page, name='logout_page'),    
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('set-password/', reset_password_confirm, name='set_password'),
]
