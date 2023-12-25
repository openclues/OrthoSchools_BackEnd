from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm

from djangoProject1.firebase_services import FirebaseServices
from notifications.models import Message

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm

from notifications.models import Message


class MessageAdminForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class MessageAdmin(ModelAdmin):
    form = MessageAdminForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Save the Message object
        recipients = form.cleaned_data['recipients']  # Get the recipients from the form
        read_by = form.cleaned_data['read_by']  # Get the recipients from the form

        recipient_ids = [recipient.id for recipient in recipients]
        obj.recipients.set(recipient_ids)
        obj.read_by.set(read_by)
        # Add recipient ids to the message
        # Extract the recipient ids
        FirebaseServices.sendNotification(
            title=obj.title,
            message=obj.message,
            data=obj.data,
            recipients=recipient_ids
        )  # Send push notification using FirebaseService


admin.site.register(Message, MessageAdmin)