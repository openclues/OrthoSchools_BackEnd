from django.db import models

from useraccount.models import UserAccount


class Device(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="device")
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
    recipients = models.ManyToManyField(UserAccount, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(UserAccount, blank=True, null=True, related_name="read_messages")

    def __str__(self):
        return self.title