from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from post.serializers import SpacePostSerializer
from saveditem.models import SavedItem
from space.models import SpacePost


class UsersSavedItemsSerializer(serializers.ModelSerializer):
    savedPosts = serializers.SerializerMethodField()

    class Meta:
        model = SavedItem
        fields = ('savedPosts',)

    def get_savedPosts(self, obj):
        request = self.context.get('request')
        posts = SpacePost.objects.filter(user__saveditem__content_type=ContentType.objects.get_for_model(SpacePost), )
        return SpacePostSerializer(posts, many=True, context={'request': request}).data
