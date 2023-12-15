from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from blog.models import BlogPost, Blog


@admin.register(BlogPost)
class CustomAdminClass(ModelAdmin):
 pass



@admin.register(Blog)
class CustomAdminClass(ModelAdmin):
    pass