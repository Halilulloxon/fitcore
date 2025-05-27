from django.contrib import admin
from .models import BlogPost, Comment

    

from django.contrib import admin
from .models import BlogPost
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','category','created_at','image_url')  



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog_post', 'content', 'created_at', 'is_approved') 
    list_filter = ('is_approved', 'created_at', 'blog_post')  
    search_fields = ('user__username', 'content') 
    ordering = ('-created_at',)  
from .models import Course, Video

class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
   
class CourseAdmin(admin.ModelAdmin):
    inlines = [VideoInline]
    list_display = ('title','description','created_at','image_url') 
admin.site.register(Course, CourseAdmin)
