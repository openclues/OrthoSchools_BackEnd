from rest_framework import serializers
from rest_framework.authtoken.models import Token

from useraccount.models import UserAccount, ProfileModel

from djoser.serializers import UserCreateSerializer


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
    address = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = ProfileModel
        fields = ['bio', 'profileImage', 'place_of_work', 'speciality', 'cover', 'first_name', 'last_name', 'email',
                  'phone', 'address', ]

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
        instance.save()
        return instance

    def get_user_id(self, obj):
        return obj


class CreateProfileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['bio', 'profileImage', 'place_of_work', 'speciality', 'cover']
