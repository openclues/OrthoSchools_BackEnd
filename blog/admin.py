from django.contrib import admin

# Register your models here.
from blog.models import Blog, BlogPost

admin.site.register(Blog)
admin.site.register(BlogPost)