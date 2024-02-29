from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin import messaging

# from useraccount.models import UserAccount


class Device(models.Model):
    user = models.ForeignKey('useraccount.UserAccount', on_delete=models.CASCADE, related_name="device")
    device_id = models.CharField(max_length=255)
    device_type = models.CharField(max_length=255)
    device_os = models.CharField(max_length=255)
    fcm_token = models.CharField(max_length=255)

    def __str__(self):
        return self.device_id


class Message(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    data = models.JSONField(null=True, blank=True)
    recipients = models.ManyToManyField('useraccount.UserAccount', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField("useraccount.UserAccount", blank=True, null=True, related_name="read_messages")

    def __str__(self):
        return self.title

    # onsaved send notification to all users signal


@receiver(post_save, sender=Message)
def send_notification(sender, instance, created, **kwargs):
    if not created:
        if instance.recipients:
            fcm_messages = []
            notification = messaging.Notification(
                title=instance.title,
                body=instance.message
            )
            message_data = {
                "payload": str(instance.data)  # Add your custom data here
            }
            for user in instance.recipients.all():
                devices = Device.objects.filter(user_id=user.id)
                print(user.id, devices)
                if devices:
                    for device in devices:
                        token = device.fcm_token
                        fcm_message = messaging.Message(
                            notification=notification,
                            data=message_data,
                            token=token
                        )
                        fcm_messages.append(fcm_message)
                    messaging.send_each(fcm_messages)