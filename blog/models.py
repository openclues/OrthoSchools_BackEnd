from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from django_quill.fields import QuillField

from commentable.models import Comment
from likable.models import Like


class Blog(models.Model):
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
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
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    is_banned = models.BooleanField(default=False)
    category = models.ManyToManyField('useraccount.Category', related_name='categorie_posts')
    content = QuillField(
        blank=True,
        null=True
    )
    cover = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = GenericRelation(Comment)
    likes = GenericRelation(Like)

    def __str__(self):
        return f"{self.blog.title} - {self.title}"
