from unfold.admin import ModelAdmin
from django.contrib import admin

from .models import Space, SpaceFile


# Register your models here.

# admin.site.register(Space)
# admin.site.register(SpaceFile)

@admin.register(Space)
class SpaceAdmin(ModelAdmin):
    list_display = ('name', 'description', 'cover', 'created_at', 'updated_at')
    list_filter = ('name', 'description', 'cover', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'cover', 'created_at', 'updated_at')

    # name = models.CharField(max_length=100)
    # description = models.CharField(max_length=100)
    # cover = models.ImageField(upload_to='images/')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
