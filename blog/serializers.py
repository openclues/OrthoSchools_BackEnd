from rest_framework import serializers

from blog.models import Blog, BlogPost
from useraccount.api.serializers.user_api_serializer import CategorySerializer
from useraccount.serializers import VisitorProfileSerializer


class BlogSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    user = VisitorProfileSerializer(read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"

    def get_posts(self, obj):
        posts = BlogPost.objects.filter(blog=obj)[:5]
        return BlogPostSerializer(posts, many=True, read_only=True).data


class BlogPostSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = '__all__'

    def get_content(self, obj):
        print(obj.content.delta)
        return obj.content.delta
