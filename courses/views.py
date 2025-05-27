from django.shortcuts import render

from .models import Course 

def courses_view(request):
  
    courses = Course.objects.all()  

   
    return render(request, 'class-details.html', {'courses': courses})