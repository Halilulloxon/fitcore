from tkinter import Image
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings 
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from app.models import BlogPost, Comment
from .forms import CommentForm
from django.db import connection
import os
from django.db import connection

from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Comment
from .forms import CommentForm
def blog_list(request):
    blog_posts = BlogPost.objects.all()  
    return render(request, 'blog_list.html', {'blog_posts': blog_posts})




def blog_detail(request, slug1):
    blog_posts = get_object_or_404(BlogPost, slug=slug1)
    blogs = BlogPost.objects.all() 
    categories = set(post.category for post in blogs)
    comments = Comment.objects.filter(blog_post=blog_posts).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comments = form.save(commit=False)
            comments.user = request.user
            comments.blog_post = blog_posts  
            comments.save()
            return redirect('blog_detail', slug1)  
    else:
        form = CommentForm()
    recent_posts = BlogPost.objects.order_by('-created_at')[:3]
    query = request.GET.get('q')  # Qidiruv so'rovini olish
    if query:
        results = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    else:
        results = BlogPost.objects.none()  

    return render(request, 'app/blog-details.html', {'blog_posts': blog_posts,
           'comments': comments, 
           'form': form,'results': results, 'query': query, 'blog_posts': blog_posts, 'recent_posts': recent_posts, 'categories':categories})


from .models import Course 

def courses_view(request):
  
    courses = Course.objects.all()  
    return render(request, 'app/classes.html', {'courses': courses})

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})
@login_required
def logout_view(request):
    logout(request) 
    return redirect('home')  


def contact(request):
    if request.method == 'POST':
        return redirect('app/thank-you.html')  
    return render(request, 'app/contact.html')  

def home(request):
    """Renders the home page."""
    blog_posts = BlogPost.objects.order_by('-created_at')[:4]
    courses= Course.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
            'user': request.user,
            'blog_posts': blog_posts,
            'courses': courses,
        }
    )

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"Yangi xabar:\n\nIsm: {name}\nEmail: {email}\nXabar: {message}"

        send_mail(
            subject='Saytdan yangi savol',
            message=full_message,
            from_email=email,
            recipient_list=['halilullohayotullo0608@gmail.com'],
            fail_silently=False,
        )
        return redirect('thank_you')

    return render(request, 'app/contact.html', {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
        'user': request.user,
    })

def thank_you(request):
    return render(request, 'app/thank-you.html')

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
            'user': request.user,
        }
    )
def loginpartial(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/loginpartial.html',
        {
            'title': 'Login',
            'message': 'Your login page.',
            'year': datetime.now().year,
            'user': request.user,
        }
    )

def gallery(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'app/gallery.html', {'blog_posts': blog_posts,'user': request.user})

def trainers(request):
    return render(request, 'app/trainers.html', {'user': request.user})

def blog(request):
    blog_posts = BlogPost.objects.all().order_by('-created_at')  
    paginator = Paginator(blog_posts, 10)  

    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)

    categories = set(post.category for post in blog_posts)
    recent_posts = BlogPost.objects.order_by('-created_at')[:3]

    context = {
        'blog_posts': blog_posts,
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'categories': categories,
    }

    return render(request, 'app/blog.html', context)


def contact_handler(request):
    if request.method == 'POST':
        name = request.POST['username']
        visitor_email = request.POST['usermail']
        visitor_phone = request.POST['userphone']
        message = request.POST['usermessage']

        email_subject = "New Contact"
        email_body = f"User Name: {name}\nUser Email: {visitor_email}\nUser Phone: {visitor_phone}\nUser Message: {message}\n"
        email_from = request.POST['usermail']
        to_email = 'halilullohayotullo0608@gmail.com'

        send_mail(
            email_subject,
            email_body,
            email_from,
            [to_email],
            fail_silently=True,
        )

        return HttpResponseRedirect(reverse('thank_you'))

    return render(request, 'app/contact.html', {'user': request.user})


def thank_you(request):
    return render(request, 'app/thank-you.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form, 'title': 'Log in'})
def delete_account(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None :
            logout(request)
            user.delete()
            return redirect('home')
        else:
            messages.error(request, "Username or password is incorrect.")

    return render(request, 'app/delete_account.html')
from django.db.models import Q

def blog_search(request):
    blog_posts = BlogPost.objects.all()
    recent_posts = BlogPost.objects.order_by('-created_at')[:3]
    query = request.GET.get('q')  # Qidiruv so'rovini olish
    if query:
        results = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
    else:
        results = BlogPost.objects.none()  # Agar qidiruv so'rovi bo'lmasa, bo'sh natija
    paginator = Paginator(results, 10)  

    page_number = request.GET.get('page',1)
    page_obj1 = paginator.get_page(page_number)
    return render(request, 'app/blog.html', {'results': results, 'query': query, 'blog_posts': blog_posts, 'recent_posts': recent_posts, 'page_obj1': page_obj1})
def course_detail_view(request, slug2):

    class_info = get_object_or_404(Course, slug=slug2)
  

    other_classes = Course.objects.order_by('-created_at')[:4]
    
 
    class_videos = class_info.videos.all()
    paginator = Paginator(class_videos, 5)  

    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    context = {
        'class_info': class_info,
        'class_videos': class_videos,
        'page_obj': page_obj,
        'other_classes': other_classes
    }
    
    return render(request, 'app/class-details.html', context)