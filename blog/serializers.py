from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog, BlogPost
from useraccount.api.serializers.user_api_serializer import CategorySerializer
from useraccount.serializers import VisitorProfileSerializer


class CreateBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ['title', 'description', 'cover']


class BlogSerializer(serializers.ModelSerializer):
    # posts = serializers.SerializerMethodField()

    user = VisitorProfileSerializer(read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    is_followed = serializers.SerializerMethodField(read_only=True)
    articles_count = serializers.SerializerMethodField(
        read_only=True
    )
    followers_count = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Blog
        fields = "__all__"

    def get_is_followed(self, obj):
        return obj.followers.filter(id=self.context['request'].user.id).exists()

    # def get_posts(self, obj):
    #     posts = BlogPost.objects.filter(blog=obj)[:10]
    #     return BlogPostSerializer(posts, many=True, read_only=True).data

    def get_articles_count(self, obj):
        return BlogPost.objects.filter(blog=obj).count()

    def get_followers_count(self, obj):
        return obj.followers.count()


class BlogPostSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'

    def get_content(self, obj):
        return obj.content.delta


class BlogInsideArticlesSerializer(serializers.ModelSerializer):
    is_my_blog = serializers.SerializerMethodField()
    user = VisitorProfileSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'cover', 'description', 'created_at', 'updated_at', 'user', 'is_my_blog']

    def get_is_my_blog(self, obj):
        return obj.user.id


class BlogPostNewSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    blog = BlogInsideArticlesSerializer(read_only=True)
    # is_saved = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    # comments = serializers.SerializerMethodField()
    user = VisitorProfileSerializer(read_only=True)
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'

    def get_content(self, obj):
        print(obj.content.delta)
        return obj.content.delta

    def get_is_liked(self, obj):
        return obj.likes.filter(user=self.context['request'].user).exists()

    # def get_is_saved(self, obj):
    #     return obj.saves.filter(user=self.context['request'].user).exists()

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    # def get_comments(self, obj):
    #     return CommentSerializer(obj.comments.all(), many=True, read_only=True).data

    def get_is_followed(self, obj):
        return obj.blog.followers.filter(id=self.context['request'].user.id).exists()


class GetNotificationsCount(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({
                'notifications_count': user.notifications.filter(is_seen=False).count()
            })
        else:
            return Response({
                'notifications_count': 0
            })
