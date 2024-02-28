from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField

from commentable.models import Comment
from likable.models import Like
from notifications.models import Message


class Blog(models.Model):
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=100, default="#000000", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    category = models.ManyToManyField('useraccount.Category', related_name='blogs')
    followers = models.ManyToManyField("useraccount.UserAccount", related_name='blog_followed', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title + "-" + self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    is_featured = models.BooleanField(default=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    is_banned = models.BooleanField(default=False)
    category = models.ManyToManyField('useraccount.Category', related_name='categorie_posts')
    content = models.TextField(null=True, blank=True)
    cover = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)

    def __str__(self):
        return f"{self.blog.title} - {self.title}"


class PostLikeModel(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='blogPost_likes_1')
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.user.username}"


class ArticleCommentLikeModel(models.Model):
    comment = models.ForeignKey('ArticleComment', on_delete=models.CASCADE, related_name='articleComment_likes')
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment.content} - {self.user.username}"


class ArticleComment(models.Model):
    content = models.TextField(
    )
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']
