from rest_framework import serializers

from blog.models import BlogPost
from blog.serializers import BlogInsideArticlesSerializer
from space.models import SpacePost, Space, SpaceFile, ImageModel, PostLike
from useraccount.models import UserAccount, ProfileModel
from useraccount.serializers import RecommendedSpacesSerializer, VisitorProfileSerializer


class SimpleSpaceSerializer(serializers.ModelSerializer):
    isJoined = serializers.SerializerMethodField(read_only=True)
    members_count = serializers.SerializerMethodField(read_only=True)
    posts_count = serializers.SerializerMethodField(read_only=True)
    is_allowed_to_join = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'cover', 'isJoined', 'members_count',
                  'posts_count', 'is_allowed_to_join', 'allowed_user_types']

    def get_is_allowed_to_join(self, obj):
        user = self.context['request'].user
        return obj.is_allowed_to_join(obj, user)

    def get_members_count(self, obj):
        return obj.include_users.count()

    def get_posts_count(self, obj):

        return obj.posts.count()

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
        fields = ['id', 'first_name', 'last_name', 'profileImage', 'userRole', 'is_verified', 'is_verified_pro']

    def get_profileImage(self, obj):
        profile = ProfileModel.objects.filter(user=obj).first()
        return str(profile.profileImage)


class BlogPostNewSerializers(serializers.ModelSerializer):
    # content = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    blog = BlogInsideArticlesSerializer(read_only=True)
    # is_saved = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    # comments_count = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    user = VisitorProfileSerializer(read_only=True)
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'

    # def get_content(self, obj):
    #     print(obj.content.delta)
    #     return obj.content.delta

    def get_is_liked(self, obj):
        return obj.likes.filter(user=self.context['request'].user).exists()

    # def get_is_saved(self, obj):
    #     return obj.saves.filter(user=self.context['request'].user).exists()

    def get_likes_count(self, obj):
        return obj.likes.count()

    # def get_comments(self, obj):
    #     return CommentSerializer(obj.comments.all(), many=True, read_only=True).data

    def get_is_followed(self, obj):
        return obj.blog.followers.filter(id=self.context['request'].user.id).exists()


class SpacePostSerializer(serializers.ModelSerializer):
    space = RecommendedSpacesSerializer(read_only=True, many=False)
    blogPost = BlogPostNewSerializers(read_only=True, many=False)
    post_images = PostImageSerializer(many=True)
    user = UserPostSerializer(read_only=True, many=False)
    is_joined = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    space_name = serializers.SerializerMethodField(read_only=True)
    is_allowed_to_join = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)

    # newComments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SpacePost
        fields = ['id', 'space', 'post_images', 'blogPost', 'user', 'title', 'content', 'video', 'created_at',
                  'updated_at', 'is_joined', 'is_liked', 'space_name', 'is_allowed_to_join', 'comments_count',
                  'likes_count', 'video']

    # def get_newComments(self, obj):
    #     from space.serializers import PostCommentSerializer
    #
    #     return PostCommentSerializer(obj.comments.all(), many=True).data

    def get_content(self, obj):
        return str(obj.content)

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if obj.interactions.filter(user=user).exists():
                return True
            else:
                return False
        else:
            return False

    # def get_post_files(self, obj):
    #     return obj.post_files.all().values_list('file', flat=True)

    def get_likes_count(self, obj):
        return obj.interactions.count()

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
    blogPost = serializers.PrimaryKeyRelatedField(queryset=BlogPost.objects.all(), required=False, allow_null=True,
                                                  allow_empty=True, default=None)
    video = serializers.FileField(required=False)

    class Meta:
        model = SpacePost
        fields = '__all__'

    # def create(self, validated_data):
    #     print(validated_data)
    #     post_images = validated_data.pop('post_images', [])
    #     post = SpacePost.objects.create(**validated_data)
    #     video = validated_data.pop('video', None)
    #     print(video)
    #     if video:
    #         post.video = video
    #         post.save()
    #
    #     if validated_data.get('blogPost'):
    #         post.blogPost = validated_data.get('blogPost')
    #         post.save()
    #     for image in post_images:
    #         post.post_images.create(image=image)
    #     return post


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



