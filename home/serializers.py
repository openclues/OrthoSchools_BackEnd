from rest_framework import serializers

from post.serializers import SpacePostSerializer
from useraccount.models import ProfileModel
from useraccount.serializers import FullUserSerializer, RecommendedSpacesSerializer


class HomeDataSerializer(serializers.Serializer):
    recommended_spaces = serializers.SerializerMethodField()  # according to user's interests
    latest_updated_posts_from_recommended = serializers.SerializerMethodField()  # according to user's interests
    my_latest_updated_posts = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()


    # according to user's interests
    def get_recommended_spaces(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            profile = ProfileModel.objects.filter(user=user).first()
            spaces = profile.recommended_spaces(profile)
            return RecommendedSpacesSerializer(spaces, many=True, context={'request': self.context['request']}).data

    def get_latest_updated_posts_from_recommended(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            profile = ProfileModel.objects.filter(user=user).first()
            spaces = profile.recommended_spaces(profile)
            myspaces = user.spaces_included.all()
            all_spaces = spaces | myspaces
            posts_list = []
            for space in all_spaces:
                if space.is_allowed_to_join(space, user):
                    posts = space.posts.all().order_by('-updated_at')
                    for post in posts:
                        posts_list.append(post)

            return SpacePostSerializer(posts_list, many=True, context={'request': self.context['request']}).data

    def get_my_latest_updated_posts(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            spaces = user.spaces_included.all()
            if spaces.exists():
                for space in spaces:
                    posts = space.posts.all().order_by('-updated_at')
                    return SpacePostSerializer(posts, many=True, context={'request': self.context['request']}).data
            else:
                return []

    def get_user(self, obj):
        user = self.context['request'].user
        return FullUserSerializer(user.profilemodel, many=False, read_only=True,
                                  context={'request': self.context['request']}).data


