from rest_framework import serializers

from commentable.models import Comment
from likable.models import Like
from post.serializers import UserPostSerializer
from useraccount.models import ProfileModel


class CommentSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True, many=False)
    comments = serializers.SerializerMethodField(read_only=True)
    likesCount = serializers.SerializerMethodField(read_only=True)
    object_likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'user', 'comments', 'likesCount', 'object_likes_count']

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data

    def get_likesCount(self, obj):
        likes = Like.objects.filter(content_type__model='comment', object_id=obj.id)
        return likes.count()

    def get_object_likes_count(self, obj):
        conenttypeMode = obj.content_type.model
        likes = Like.objects.filter(content_type__model= conenttypeMode, object_id=obj.id)
        return likes.count()


class Commentor(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['id', 'profileImage', 'user']


class CommentOnPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'object_id']

        # class Comment(models.Model):
        #     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        #     object_id = models.PositiveIntegerField()
        #     content_object = GenericForeignKey('content_type', 'object_id')
        #     text = models.TextField()
        #     created_at = models.DateTimeField(auto_now_add=True)
        #     user = models.ForeignKey('useraccount.UserAccount',
        #                              on_delete=models.CASCADE)  # Replace with your actual user model
        #     comments = GenericRelation('commentable.Comment')
        #     mentions = GenericRelation('commentable.Mention')
        #     replies = GenericRelation('commentable.Reply')


class GetCommentsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['object_id']
