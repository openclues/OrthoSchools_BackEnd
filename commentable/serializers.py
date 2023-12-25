from rest_framework import serializers

from commentable.models import Comment
from post.serializers import UserPostSerializer
from useraccount.models import ProfileModel


class CommentSerializer(serializers.ModelSerializer):
    user = UserPostSerializer(read_only=True, many=False)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'user', 'comments']

    def get_comments(self, obj):
        return CommentSerializer(obj.comments.all(), many=True).data


class Commentor(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['id', 'profileImage', 'user']
