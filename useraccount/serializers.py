from actstream.models import Action
from rest_framework import serializers

from course.serializers import CourseSerializer
from post.serializers import SpacePostSerializer
from space.models import Space
from space.serializers import SpaceSerializer, ActivitySerializer
from useraccount.api.serializers.user_api_serializer import CategorySerializer
from useraccount.models import ProfileModel, UserAccount


class HomeDataSerializer(serializers.Serializer):
    recommended_spaces = serializers.SerializerMethodField()  # according to user's interests
    latest_updated_posts_from_recommended = serializers.SerializerMethodField()  # according to user's interests
    my_latest_updated_posts = serializers.SerializerMethodField()

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
        return str(user.email)
    #
    # def get_my_spaces(self, obj):
    #     user = self.context['request'].user
    #     if user.is_authenticated:
    #         spaces = user.spaces_included.all()
    #         return SpaceSerializer(spaces, many=True, context={'request': self.context['request']}).data
    #


class RecommendedSpacesSerializer(serializers.ModelSerializer):
    is_allowed_to_join = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True)
    joined = serializers.SerializerMethodField()

    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'cover', 'is_allowed_to_join', 'members_count', 'category',
                  'allowed_user_types', 'joined']

    def get_is_allowed_to_join(self, obj):
        user = self.context['request'].user
        return obj.is_allowed_to_join(obj, user)

    def get_members_count(self, obj):
        return obj.include_users.count()

    def get_joined(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user.spaces_included.filter(id=obj.id).exists():
                return True
            else:
                return False
        else:
            return False


class UserSerializer(serializers.ModelSerializer):
    user_activities = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = "__all__"

    def get_courses(self, obj):
        user = self.context['request'].user
        if user.userRole == 2:
            return CourseSerializer(obj.courses.all(), many=True, context={'request': self.context['request']}).data
        else:
            return []

    def get_user_activities(self, obj):
        spaces = Space.objects.filter(include_users=obj.id)
        activities = Action.objects.filter(target_object_id__in=spaces).order_by(
            '-timestamp')

        # activities = Action.objects.filter(actor_object_id=obj.id, ).order_by(
        #     '-timestamp')
        return ActivitySerializer(activities, many=True, read_only=True).data


class FullUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = ProfileModel
        fields = '__all__'


class VisitorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'last_name', 'userRole', 'phone', 'address', 'is_banned', 'is_suspend',
                  'is_verified', 'is_verified_pro']


class VisitorProfileSerializer(serializers.ModelSerializer):
    user_account = serializers.SerializerMethodField()

    class Meta:
        model = ProfileModel
        fields = ['title', 'bio', 'study_in', 'cover', 'profileImage', 'birth_date', 'place_of_work', 'speciality',
                  'user_account']

    def get_user_account(self, obj):
        return VisitorUserSerializer(obj, many=False, read_only=True).data
