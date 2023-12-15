from admin_confirm import AdminConfirmMixin
from django.contrib.contenttypes.admin import GenericTabularInline
from unfold.admin import ModelAdmin, TabularInline as Tub
from django.contrib import admin

from commentable.models import Comment
from .models import Space, SpaceFile, SpacePost, ImageModel


# Register your models here.

# admin.site.register(Space)
# admin.site.register(SpaceFile)

# @admin.register(Space)
# class SpaceAdmin(ModelAdmin):
#     pass
#


class FileInline(Tub):
    model = SpaceFile

    extra = 0


class ImageInline(Tub):
    model = ImageModel
    extra = 0


class PostInline(Tub):
    inlines = [FileInline, ImageInline]

    model = SpacePost

    extra = 1


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    pass


@admin.register(SpacePost)
class SpacePostAdmin(AdminConfirmMixin, ModelAdmin):
    inlines = [ImageInline]


@admin.register(Space)
class SpaceAdmin(AdminConfirmMixin, ModelAdmin):
    # confirmation_fields = ['name', 'description', 'cover', 'created_at', 'updated_at']

    list_display_links = ["name", "description"]

    inlines = [PostInline]
    ordering = ['-created_at']
    list_display = ['name', 'description', 'created_at']

    # custom change page
    # change_form_template = 'admin/space_change_form.html'

    # filter_vertical = ('include_users',)  # Add other fields as needed
    # filter_horizontal = ('exclude_users',)  # Add other fields as needed
    # list_display = ('name', 'description', 'cover', 'created_at', 'updated_at')
    # list_filter = ('name', 'description', 'cover', 'created_at', 'updated_at')
    # search_fields = ('name', 'description', 'cover', 'created_at', 'updated_at')
    # readonly_fields = ('created_at', 'updated_at')

# name = models.CharField(max_length=100)
# description = models.CharField(max_length=100)
# cover = models.ImageField(upload_to='images/')
# created_at = models.DateTimeField(auto_now_add=True)
# updated_at = models.DateTimeField(auto_now=True)

# javescript
