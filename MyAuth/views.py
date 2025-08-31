from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
import requests
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 

DJOSER_BASE_URL = 'https://blogz-sdameer.onrender.com/auth'






def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')



def register(request):
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmpassword = request.POST.get("confirmpassword")

        data = {
            'username': username,
            'email': email,
            'password': password,
            're_password': confirmpassword
        }

        response = requests.post(f'{DJOSER_BASE_URL}/users/', json=data)

        if response.status_code == 201:
            messages.success(
                request, "Registered successfully. Check your email to activate account.")
            return redirect('login_page')
        else:
            try:
                errors = response.json()
                for field, msgs in errors.items():
                    for msg in msgs:
                        messages.error(request, f"{field}: {msg}")
            except Exception:
                messages.error(
                    request, "Something went wrong during registration.")

    return render(request, 'register.html', )


def logout_page(request):
    # request.session.flush()
    logout(request)
    # messages.success(request, "Logged out successfully.")
    return redirect('home')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        response = requests.post(
            f'{DJOSER_BASE_URL}/users/reset_password/', json={"email": email})

        if response.status_code == 204:
            messages.success(request, "Password reset email sent.")
        else:
            messages.error(request, "Something went wrong.")

    return render(request, 'forgot_password.html')


def reset_password_confirm(request):
    uid = request.GET.get('uid')
    token = request.GET.get('token')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        re_password = request.POST.get('re_password')

        if new_password != re_password:
            messages.error(request, "Passwords do not match.")
        else:
            response = requests.post(f'{DJOSER_BASE_URL}/auth/users/reset_password_confirm/', data={
                "uid": uid,
                "token": token,
                "new_password": new_password,
                "re_new_password": re_password
            })

            if response.status_code == 204:
                messages.success(
                    request, "Password changed successfully. Please log in.")
                return redirect('login_page')
            else:
                messages.error(request, "Something went wrong. Try again.")

    return render(request, 'set_new_password.html',  context={'messages':messages})



def custom_404_view(request, exception):
    return render(request, 'custom_404.html', status=404)


def activate_url(request):
    return render(request ,  'activate.html')