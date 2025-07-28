from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import os

# for restricted login :
from django.contrib.auth.decorators import login_required

# for current user data :
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# for blogs :
from .models import Blog, Topic, Message
from .forms import BlogForm

# for seach bar :
from django.db.models import Q
from django.core.paginator import Paginator


from django_ratelimit.decorators import ratelimit


# create :
@login_required(login_url='login_page')
def post(request):
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            # if blog.image:
            #     print("Image saved to:", blog.image.url)

            # else:
            #     print("No image uploaded.")


            return redirect('home')
    context = {'form': form, }
    return render(request, 'add_blog.html', context=context)

# Update : 
@login_required(login_url='login_page')
def update(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_body', pk=blog.id)  # type: ignore

    context = {'form': form, }
    return render(request, 'add_blog.html', context=context)

# delete :
@login_required(login_url='login_page')
def delete(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('home')

    context = {'object': blog, }
    return render(request, 'delete.html', context=context)

@login_required(login_url='login_page')
def delete_msg(request, pk):
    message = Message.objects.get(id=pk)
    blog = message.blog
    if request.method == "POST":
        message.delete()
        return redirect('blog_body', pk=blog.id)  # type: ignore

    context = {'object': message, }
    return render(request, 'delete.html', context=context)


def users(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    blogs = Blog.objects.filter(user=user)

    return render(request, 'user.html', context={
        'current_user':user,
        'blogs': blogs,
        "num_blogs": len(blogs),
        'blogs_topics': set(b.topic for b in blogs)
    })


def home(request):
    blog = Blog.objects.all().order_by('-created')
    topics = Topic.objects.all()

    
    q = request.POST.get('q') or request.GET.get('q') or ''

    if q:
        blog = Blog.objects.filter(
            Q(topic__topic_name__icontains=q) |
            Q(user__username__icontains=q) |
            Q(name__icontains=q)
        ).order_by('-created')

    paginator = Paginator(blog, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blog': page_obj,
        'topics': topics,
        'page_obj':page_obj
    }

    return render(request, 'main.html', context)



def blog_body(request, pk):
    blog = Blog.objects.get(id=pk)
    msg = blog.message_set.all().order_by('-created')  # type: ignore

    if request.method == "POST":
        body = request.POST.get('msg')
        if body and body.strip():
            Message.objects.create(
                user=request.user,
                blog=blog,
                body=body.strip()
            )
            return redirect('blog_body', pk=blog.id)  # type: ignore
        else:
            return HttpResponse("Empty message received", status=400)

    context = {'blog': blog, 'message': msg}
    return render(request, 'view.html', context)


@login_required(login_url='login_page')
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        issues = request.POST.get('issues')
        
        # Compose email
        email_subject = f"Contact Form: {subject}"
        email_message = f"""
        From: {name} ({email})
        Subject: {subject}
        
        Message:
        {message}
        
        Issues/Details:
        {issues}
        """
        
        try:
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                ['syedameerdev@example.com'],  # Replace with your email
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
        
        return redirect('contact_us')
    
    return render(request, 'contact_us.html')



def developer_page(request):
    return render(request, 'developer_page.html')


import google.generativeai as genai  # type: ignore
@login_required(login_url='login_page')
@ratelimit(key='user_or_ip', rate='3/d', block=False)
def genai_title(request):
    
    # this is for custom rate limiting 
    if getattr(request, 'limited', True):
        return render(request, "ratelimit_exceeded.html", status=429)

    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))  # type: ignore
    model = genai.GenerativeModel("gemini-1.5-flash")  # type: ignore

    text = request.POST.get('title') 
    prompt = f"""
        role : system,
        warning : you are not advised to answer anything to the user except task  ,
        task : generate a single {text} SEO friendly title for the blog post 
                """


    answer = model.generate_content(prompt)
    
    return render(request, 'genai.html', context={'answer':answer.text.strip()})

    
