from django.contrib import admin

# Register your models here.
from saveditem.models import SavedItem

admin.site.register(SavedItem)