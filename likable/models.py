from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Like(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey('useraccount.UserAccount',
                             on_delete=models.CASCADE)  # Replace 'YourUserModel' with your actual user model

    def __str__(self):
        return f'{self.user.username} liked {self.content_object}'

    def perform_like(self, user, obj):
        self.user = user
        self.content_object = obj
        self.save()

    def perform_unlike(self, user, obj):
        self.user = user
        self.content_object = obj
        self.delete()
