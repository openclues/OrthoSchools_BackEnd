from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Message
from useraccount.models import UserAccount


class Course(models.Model):
    course_name = models.CharField(max_length=100, blank=True, null=True)
    course_description = models.TextField()
    course_cover = models.ImageField(upload_to='course_covers', blank=True, null=True)
    course_image = models.ImageField(upload_to='course_images', blank=True, null=True)
    course_video = models.FileField(upload_to='course_videos', blank=True, null=True)
    course_link = models.URLField()

    def __str__(self):
        return self.course_name


# on save

@receiver(post_save, sender=Course)
def send_notification(sender, instance, created, **kwargs):
    if created:
        message = Message.objects.create(title="New Course", message="New Course has been added", data={"course_id": instance.id})
        message.recipients.set(UserAccount.objects.filter(userRole=2))
        message.save()
