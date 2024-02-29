from datetime import datetime

from actstream.models import Action
from django.contrib.auth.models import Group
from django.utils import timezone
from rest_framework import serializers

from blog.models import Blog
from notifications.models import Message
from space.models import Space, SpacePost
from useraccount.api.serializers.user_api_serializer import CategorySerializer
from useraccount.models import ProfileModel, UserAccount, VerificationProRequest, Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = '__all__'


class RecommendedSpacesSerializer(serializers.ModelSerializer):
    is_allowed_to_join = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True)
    joined = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'cover', 'is_allowed_to_join', 'members_count', 'category',
                  'allowed_user_types', 'joined', 'users', 'posts_count']

    def get_posts_count(self, obj):
        return obj.posts.count()

    def get_users(self, obj):
        included_users = obj.include_users.all()[:5]
        return SpaceUserSerializer(included_users, many=True).data

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
    # user_activities = serializers.SerializerMethodField()
    # courses = serializers.SerializerMethodField()
    days_left = serializers.SerializerMethodField()
    is_staff = serializers.SerializerMethodField()
    is_superuser = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = UserAccount
        fields = "__all__"

    from django.utils import timezone

    def get_groups(self, obj):

        return UserAccount.objects.get(
            id=obj.id
        ).groups.all()

    def get_permissions(self, obj):
        return obj.get_all_permissions()

    def get_is_staff(self, obj):
        return obj.is_staff

    def get_is_superuser(self, obj):
        return obj.is_superuser

    def get_days_left(self, obj):
        # Check if user is not verified and joined date is not None
        if not obj.is_verified and obj.date_joined:
            # Get the current date and time with the timezone information from obj.date_joined
            current_datetime = timezone.now()

            # Calculate the difference between current date and joined date
            days_difference = (current_datetime - obj.date_joined).days

            # Check if 30 days have passed since the joined date
            if days_difference >= 30:
                return -1  # User is not verified and 30 days have passed
            else:
                return 30 - days_difference  # Return the number of days left
        elif obj.is_verified:
            return 0  # User is verified
        else:
            return -1  # Return -1 if date_joined is None

            # def get_courses(self, obj):
    #     user = self.context['request'].user
    #     if user.userRole == 2:
    #         return CourseSerializer(obj.courses.all(), many=True, context={'request': self.context['request']}).data
    #     else:
    #         return []
    #
    # def get_user_activities(self, obj):
    #     spaces = Space.objects.filter(include_users=obj.id)
    #     activities = Action.objects.filter(target_object_id__in=spaces).order_by(
    #         '-timestamp')

    # activities = Action.objects.filter(actor_object_id=obj.id, ).order_by(
    #     '-timestamp')
    # return ActivitySerializer(activities, many=True, read_only=True).data


class SpaceUserSerializer(serializers.ModelSerializer):
    profileImage = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = ['id', 'first_name', 'last_name', 'profileImage']

    def get_profileImage(self, obj):
        profile = ProfileModel.objects.filter(user=obj).first()
        return str(profile.profileImage)


class FullUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_me = serializers.SerializerMethodField()
    blog = serializers.SerializerMethodField()
    certificates = serializers.SerializerMethodField()
    unread_notifications = serializers.SerializerMethodField()

    # verified_pro_request = serializers.SerializerMethodField()

    class Meta:
        model = ProfileModel
        fields = ['title', 'bio', 'study_in', 'cover', 'profileImage', 'birth_date', 'place_of_work', 'speciality',
                  'user', 'is_me', 'id_card', 'selfie', 'blog', 'certificates', 'country', 'city', 'state','unread_notifications']

    def get_is_me(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user.id == obj.user.id:
                return True
            else:
                return False
        else:
            return False

    def get_certificates(self, obj):
        return CertificateSerializer(obj.certificates.all(), many=True, read_only=True).data

    def get_user(self, obj):
        return UserSerializer(obj.user, many=False, read_only=True).data

    def get_blog(self, obj):
        blog = Blog.objects.filter(user=obj.user).first()
        if blog:
            from blog.serializers import BlogInsideArticlesSerializer

            return BlogInsideArticlesSerializer(blog, many=False, read_only=True).data
        else:
            return None

    def get_unread_notifications(self, obj):
        user = self.context['request'].user
        messages = Message.objects.filter(recipients__in=[user]).exclude(read_by__in=[user]).count()

        return messages

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
                  'user_account', 'id',]

    def get_user_account(self, obj):
        return VisitorUserSerializer(obj, many=False, read_only=True).data


class VerifyUserSerializer(serializers.ModelSerializer):
    profile = FullUserSerializer(many=False, read_only=True)
    class Meta:
        model = VerificationProRequest
        fields = ['requestStatus', 'profile', 'id']


class UserUpdateSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)
    cover = serializers.ImageField(required=False)
    birth_date = serializers.DateField(required=False)
    id_card = serializers.FileField(required=False)
    selfie = serializers.ImageField(required=False)

    # profilemodel = FullUserSerializer(many=False, read_only=True)

    class Meta:
        model = UserAccount
        fields = "__all__"

    def update(self, instance, validated_data):
        if 'profile_image' in validated_data:
            instance.profilemodel.profileImage = validated_data['profile_image']
        if 'cover' in validated_data:
            instance.profilemodel.cover = validated_data['cover']
        if 'birth_date' in validated_data:
            instance.profilemodel.birth_date = validated_data['birth_date']
        if 'id_card' in validated_data:
            instance.profilemodel.id_card = validated_data['id_card']
        if 'selfie' in validated_data:
            instance.profilemodel.selfie = validated_data['selfie']
        if 'title' in validated_data:
            instance.profilemodel.title = validated_data['title']

        instance.profilemodel.save()
        # the rest of userAccount data
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)

        instance.save()
        instance.profilemodel.save()
        return instance


class SpaceSerializerJustName(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'cover']


class EmailVerificationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100, required=True)
