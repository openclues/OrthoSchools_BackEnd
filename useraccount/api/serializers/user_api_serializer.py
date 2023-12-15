from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from useraccount.models import UserAccount, ProfileModel, Category

from djoser.serializers import UserCreateSerializer, TokenCreateSerializer


class CategorySerializer(serializers.ModelSerializer):
    is_selected = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_is_selected(self, obj):
        if self.context.get('request'):

            user = self.context['request'].user
            if user.is_authenticated:
                profile = ProfileModel.objects.get(user=user)
                if obj in profile.interstes.all():
                    return True
                else:
                    return False


class RegisterRequestSerializer(UserCreateSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'password', 'first_name', 'last_name']


class RegisterResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = ['email', 'first_name', 'last_name', 'token']

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class CreateProfileRequestSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=20, required=False)
    title = serializers.CharField(max_length=100, required=False)
    address = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = ProfileModel
        fields = ['bio', 'profileImage', 'place_of_work', 'speciality', 'cover', 'first_name', 'last_name', 'email',
                  'phone', 'address', 'title', 'birth_date', 'study_in']

    def create(self, validated_data):
        return ProfileModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = instance.user
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.email = validated_data.get('email', user.email)
        user.phone = validated_data.get('phone', user.phone)
        user.address = validated_data.get('address', user.address)
        user.save()
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)
        instance.place_of_work = validated_data.get('place_of_work', instance.place_of_work)
        instance.speciality = validated_data.get('speciality', instance.speciality)
        instance.cover = validated_data.get('cover', instance.cover)
        instance.title = validated_data.get('title', instance.title)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.study_in = validated_data.get('study_in', instance.study_in)

        instance.save()
        return instance

    def get_user_id(self, obj):
        return obj


class CreateProfileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['bio', 'profileImage', 'place_of_work', 'speciality', 'cover']


class CustomTokenCreateSerializer(TokenCreateSerializer):
    pass


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'address', 'is_active',
                  'last_login']
        extra_kwargs = {'password': {'write_only': True}}


class ProfileFullDataSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer(
        read_only=True
    )

    class Meta:
        model = ProfileModel
        fields = '__all__'


class ProfileInterestesSerializer(serializers.ModelSerializer):
    interests = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = ProfileModel
        fields = '__all__'

    def get_interests(self, obj):
        return obj.interests.all()
