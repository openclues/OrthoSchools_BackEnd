from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify


class Blog(models.Model):
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Generate a slug when saving the blog
        if not self.slug:
            self.slug = slugify(self.title + "-" + self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_banned = models.BooleanField(default=False)
    content = RichTextField(blank=True, null=True)
    cover = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blog.title} - {self.title}"