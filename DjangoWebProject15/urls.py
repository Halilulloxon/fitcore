"""
Definition of urls for DjangoWebProject15.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.urls import include 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
        path('', views.home, name='home'),
        path('home', views.home, name='home'),
        path('contact', views.contact, name='contact'),
        path('login', views.login_view, name='login'),
        path('login', views.login_view, name='login_view'),
        path('admin', admin.site.urls),
        path('register',views.register, name='register'),
        path('about', views.about, name='about'),
        path('gallery', views.gallery, name='gallery'),
        path('authors', views.trainers, name='trainers'),
        path('blog', views.blog, name='blog'),
        path('search', views.blog_search, name='blog_search'),
        path('contact-handler', views.contact_handler, name='contact_handler'),
        path('thank-you', views.thank_you, name='thank_you'),
        path('logout', views.logout_view, name='logout'),
        path('delete_account', views.delete_account, name='delete_account'),
        path('blog-<slug:slug1>', views.blog_detail, name='blog_detail'),
        path('classes', views.courses_view, name='classes'),
        path('classes-<slug:slug2>', views.course_detail_view, name='class_detail'),

       


]
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
