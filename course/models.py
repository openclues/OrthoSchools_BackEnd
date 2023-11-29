from django.db import models


# Create your models here.

class Course(models.Model):
    course_name = models.CharField(max_length=100, blank=True, null=True)
    course_description = models.TextField()
    course_image = models.ImageField(upload_to='course_images', blank=True, null=True)
    course_video = models.FileField(upload_to='course_videos', blank=True, null=True)
    course_link = models.URLField()

    def __str__(self):
        return self.course_name

