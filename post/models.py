from django.db import models


# Create your models here.


class Post(models.Model):
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('useraccount.UserAccount', on_delete=models.CASCADE, null=True,
                                related_name='user_posts')
    space = models.ForeignKey('space.Space', on_delete=models.CASCADE, null=True, related_name='space_posts')

    def __str__(self):
        return self.title


class Comment(models.Model):
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    creator = models.ForeignKey('useraccount.UserAccount', on_delete=models.CASCADE, null=True,
                                related_name='user_comments')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, related_name='post_comments')

    def __str__(self):
        return self.body

