from django.db import models

# Create your models here.


class ReportContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('useraccount.UserAccount', on_delete=models.CASCADE, related_name="reports")

    def __str__(self):
        return self.title

