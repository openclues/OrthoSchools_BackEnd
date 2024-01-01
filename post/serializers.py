from rest_framework import serializers

from blog.models import BlogPost
from space.models import SpacePost, Space, SpaceFile, ImageModel
from useraccount.models import UserAccount, ProfileModel


class SimpleSpaceSerializer(serializers.ModelSerializer):
    isJoined = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'created_at', 'updated_at','cover', 'isJoined']

    def get_isJoined(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user.spaces_included.filter(id=obj.id).exists():
                return True
            else:
                return False
        else:
            return False
class BlogPostSerializerForsPACEpOST(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'

    def get_content(self, obj):
        print(obj.content.delta)
        return obj.content.delta


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'


class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceFile
        fields = '__all__'


class UserPostSerializer(serializers.ModelSerializer):
    profileImage = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = ['id', 'first_name', 'last_name', 'profileImage']

    def get_profileImage(self, obj):
        profile = ProfileModel.objects.filter(user=obj).first()
        if profile:
            if profile.profileImage:
                return profile.profileImage
            else:
                return None
        else:
            return None


class SpacePostSerializer(serializers.ModelSerializer):
    post_files = PostFileSerializer(many=True)
    space = SimpleSpaceSerializer(read_only=True, many=False)
    blogPost = BlogPostSerializerForsPACEpOST(read_only=True, many=False)
    post_images = PostImageSerializer(many=True)
    user = UserPostSerializer(read_only=True, many=False)
    is_joined = serializers.SerializerMethodField(read_only=True)
    is_liked  = serializers.SerializerMethodField(read_only=True)
    space_name = serializers.SerializerMethodField(read_only=True)
    is_allowed_to_join = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = SpacePost
        fields = ['id', 'content', 'space', 'user', 'post_files', 'post_images', 'created_at',
                  'is_joined', 'updated_at', 'created_at', 'space_name', 'is_allowed_to_join', 'comments_count',
                  'blogPost', 'likes_count', 'is_liked' ]

    def get_is_liked(self,obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user in obj.likes.all():
                return True
            else:
                return False
        else:
            return False
    def get_post_files(self, obj):
        return obj.post_files.all().values_list('file', flat=True)

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_post_images(self, obj):
        return obj.post_images.all().values_list('image', flat=True)

    def get_is_joined(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user.spaces_included.filter(id=obj.space.id).exists():
                return True
            else:
                return False
        else:
            return False

    def get_is_allowed_to_join(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.space.is_allowed_to_join(obj.space, user)
        else:
            return False

    def get_space_name(self, obj):
        return obj.space.name


class AddPostSerializer(serializers.ModelSerializer):
    space = serializers.PrimaryKeyRelatedField(queryset=Space.objects.all(), required=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SpacePost
        fields = '__all__'

    def create(self, validated_data):
        post_images = validated_data.pop('post_images', [])
        post = SpacePost.objects.create(**validated_data)
        if validated_data.get('blogpost'):
            post.blogPost = validated_data.get('blogpost')
            post.save()
        for image in post_images:
            post.post_images.create(image=image)
        return post


class UpdatePostSerializer(serializers.ModelSerializer):
    post_files = serializers.ListField(child=serializers.FileField(), required=False)
    post_images = serializers.ListField(child=serializers.ImageField(), required=False)

    class Meta:
        model = SpacePost
        fields = '__all__'

    def update(self, instance, validated_data):
        post_files = validated_data.pop('post_files', [])
        post_images = validated_data.pop('post_images', [])
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        for file in post_files:
            instance.post_files.create(file=file)
        for image in post_images:
            instance.post_images.create(image=image)
        return instance


class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpacePost
        fields = '__all__'

    def delete(self, instance):
        instance.delete()
        return instance

# create a view api to get a list of spaces and blogs with search of category_name

#
