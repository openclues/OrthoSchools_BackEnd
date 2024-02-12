from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from django.db import models
from commentable.models import Comment
from likable.models import Like
from notifications.models import Message


class Space(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='images/')
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField("useraccount.UserAccount", related_name='spaces_followed', blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField('useraccount.Category', related_name='spaces')
    # Define choices for user types with more readable keys
    USER_TYPES = (
        ('public', 'Public'),
        ('premium', 'Premium'),
    )

    # Field to specify allowed user types in the space
    allowed_user_types = models.CharField(max_length=100, choices=USER_TYPES, default=1)
    exclude_users = models.ManyToManyField("useraccount.UserAccount", related_name='spaces_excluded', blank=True)
    include_users = models.ManyToManyField("useraccount.UserAccount", related_name='spaces_included', blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def is_allowed_to_join(self, user):
        if self.allowed_user_types == "public":
            return True
        else:
            if user.userRole == 2:
                return True
            else:
                return False


class SpaceFile(models.Model):
    file = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey("space.SpacePost", on_delete=models.CASCADE, blank=True, null=True,
                             related_name='post_files')


class SpacePost(models.Model):
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    title = models.CharField(max_length=100)
    blogPost = models.ForeignKey("blog.BlogPost", on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='space_posts')
    content = models.TextField()
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    comments = GenericRelation(Comment, related_query_name='space_posts', on_delete=models.CASCADE)
    likes = GenericRelation(Like)


def __str__(self):
    return self.title





class ImageModel(models.Model):
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(SpacePost, on_delete=models.CASCADE, blank=True, null=True, related_name='post_images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostLike(models.Model):
    post = models.ForeignKey(SpacePost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PostComment(models.Model):
    content = models.TextField(
    )
    post = models.ForeignKey(SpacePost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)
        message = Message.objects.create(
            title="New Comment",
            message="You have a new comment",
            data={"type": "new_comment", "id": self.id},
        )
        message.recipients.set([self.post.user.id])
        message.save()
class CommentReply(models.Model):
    content = models.TextField(
    )
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']











class PostLike(models.Model):
    post = models.ForeignKey(SpacePost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CommentLike(models.Model):
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReplyLike(models.Model):
    reply = models.ForeignKey(CommentReply, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey("useraccount.UserAccount", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
