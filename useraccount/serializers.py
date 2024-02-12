from actstream.models import Action
from rest_framework import serializers

from blog.models import Blog
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

    class Meta:
        model = UserAccount
        fields = "__all__"

    def get_days_left(self, obj):
        obj.date_joined
        # check if user is not verified and 30 days from date joined
        if obj.is_verified == False and obj.date_joined.day + 30 == obj.date_joined.day:
            days_left = 30 - obj.date_joined.day
            return days_left
        elif obj.is_verified == True:
            return 0

        else:
            return -1
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

    # verified_pro_request = serializers.SerializerMethodField()

    class Meta:
        model = ProfileModel
        fields = ['title', 'bio', 'study_in', 'cover', 'profileImage', 'birth_date', 'place_of_work', 'speciality',
                  'user', 'is_me', 'id_card', 'selfie', 'blog', 'certificates', 'country', 'city', 'state']

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
                  'user_account', 'id']

    def get_user_account(self, obj):
        return VisitorUserSerializer(obj, many=False, read_only=True).data


class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationProRequest
        fields = ['requestStatus', 'user', 'id']


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
