from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
# from useraccount.models import UserAccount


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField()
    likes = GenericRelation('likable.Like')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('useraccount.UserAccount', on_delete=models.CASCADE)  # Replace with your actual user model
    comments = GenericRelation('commentable.Comment')
    mentions = GenericRelation('commentable.Mention')
    replies = GenericRelation('commentable.Reply')

    def __str__(self):
        return f'{self.user.username} - {self.text}'


class Mention(models.Model):
    user = models.ForeignKey('useraccount.UserAccount', on_delete=models.CASCADE)  # Replace with your actual user model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.user.username} mentioned in {self.content_object}'


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('useraccount.UserAccount', on_delete=models.CASCADE)  # Replace with your actual user model
    mentions = GenericRelation(Mention)

    def __str__(self):
        return f'{self.user.username} - {self.text}'
