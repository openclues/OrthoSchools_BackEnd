from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from blog.models import BlogPost


@admin.register(BlogPost)
class CustomAdminClass(ModelAdmin):
    # Preprocess content of readonly fields before render
    readonly_preprocess_fields = {
        # "content": "html.unescape",

        # "other_field_name": lambda content: content.strip(),
    }

    # Display submit button in filters
    list_filter_submit = True

    # Custom actions
    actions_list = []  # Displayed above the results list
    actions_row = [

        # Displayed in a table row in results list
        # "unfold.contrib.actions.row_actions.RowActions",
    ]  # Displayed in a table row in results list
    actions_detail = []  # Displayed at the top of for in object detail
    actions_submit_line = []  # Displayed near save in object detail

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,

        }
    }
