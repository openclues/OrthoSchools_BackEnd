from rest_framework import serializers
from rest_framework.authtoken.models import Token

from useraccount.models import UserAccount, ProfileModel


class RegisterRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['email', 'password', 'first_name', 'last_name']


class RegisterResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'first_name', 'last_name', 'token']

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class CreateProfileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['bio', 'profileImage', 'place_of_work', 'speciality', 'cover']

    def create(self, validated_data):
        return ProfileModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
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
