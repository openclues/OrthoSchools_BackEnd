from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.views import View
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from commentable.models import Comment
from commentable.serializers import CommentSerializer, CommentOnPostCreateSerializer
from likable.models import Like
from notifications.models import Message
from useraccount.api.serializers.user_api_serializer import CategorySerializer
from useraccount.models import Category
from .models import Blog, BlogPost
from rest_framework import generics, status

from .serializers import BlogSerializer, BlogPostSerializer, BlogPostNewSerializer, CreateBlogSerializer


class PaginationList(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 100


class BlogDetailView(View):
    template_name = 'blog_detail.html'  # Adjust the template name as needed

    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        return render(request, self.template_name, {'blog': blog})


class AdminHomeScreenView(View):
    template_name = 'admin/index.html'  # Adjust the template name as needed

    def get(self, request):
        return render(request, self.template_name, {})


class BlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    filter_backends = [SearchFilter]
    pagination_class = PaginationList
    search_fields = ['category__name']  # Assuming 'name' is a field in your Category model

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        followed_only = self.request.query_params.get('followed', False)
        if followed_only:
            print("asdasdasd")
            queryset = queryset.filter(followers=self.request.user)

        return queryset

    def get_latest_created_posts(self):
        blogs = BlogPost.objects.filter(blog__is_published=True).order_by('-updated_at')[:5]
        return BlogSerializer(blogs, many=True, ).data


class FeaturedBlogListView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        blog = self.request.query_params.get('blog', None)
        blogPosts = BlogPost.objects.filter(is_featured=True, blog=blog).order_by('-updated_at')[:5]
        return Response(BlogPostSerializer(blogPosts, many=True, context={'request': self.request}).data)


class FilteredArticlesListView(generics.ListAPIView):
    serializer_class = BlogPostNewSerializer
    queryset = BlogPost.objects.all()
    filter_backends = [SearchFilter]
    pagination_class = PaginationList
    search_fields = ['category__name']  # Assuming 'name' is a field in your Category model

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_banned=False)
        category = self.request.query_params.get('category', None)
        following = self.request.query_params.get('following', None)
        if category:
            queryset = queryset.filter(category__name=category)
        if following:
            print("asdasdasd")
            queryset = queryset.filter(
                blog__followers__in=[self.request.user])  # Assuming 'name' is a field in your Category model

        return queryset


class GetBlogPostsComments(APIView):

    def get(self, request):
        post_id = self.request.query_params.get('id', None)
        post = BlogPost.objects.get(id=post_id)
        comments = post.comments.all()
        likes = Like.objects.filter(content_type=ContentType.objects.get_for_model(BlogPost), object_id=post_id)

        return Response({'comments': CommentSerializer(comments, many=True).data, 'parent_likes_count': likes.count(),
                         'isLiked': likes.filter(user=request.user).exists()})


class LikeAndUnlikeArticle(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        post_id = request.query_params.get('article_id', None)
        post = BlogPost.objects.get(id=post_id)
        if post.likes.filter(
                user=request.user

        ).exists():
            like = Like.objects.get(
                user=request.user,
                object_id=post_id,
                content_type=ContentType.objects.get_for_model(post)
            )
            like.delete()

            return Response({"parent_likes_count": post.likes.count(), 'message': 'unliked', 'isLiked': False},
                            status=status.HTTP_200_OK)

        else:
            like = Like.objects.create(
                user=request.user,
                object_id=post_id,
                content_type=ContentType.objects.get_for_model(post)
            )
            like.save()
            return Response({"parent_likes_count": post.likes.count(), 'message': 'liked', 'isLiked': True},
                            status=status.HTTP_200_OK)


class BlogScreenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        blog_id = request.query_params.get('blog_id', None)
        blog = Blog.objects.get(id=blog_id)
        featured_posts = BlogPost.objects.filter(blog=blog, is_featured=True).order_by('-updated_at')[:5]
        return Response({
            'blog': BlogSerializer(blog, context={'request': request}).data,
            'is_followed': blog.followers.filter(id=request.user.id).exists(),
            'featured_posts': BlogPostSerializer(featured_posts, many=True, context={'request': request}).data,
            'categories': CategorySerializer(Category.objects.filter(
                id__in=BlogPost.objects.filter(blog=blog).values_list('category', flat=True).distinct(),
            ), many=True).data
        })


class MakeArticleComment(generics.CreateAPIView):
    serializer_class = CommentOnPostCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        comment_content_type = ContentType.objects.get_for_model(BlogPost)
        commnet = Comment.objects.create(object_id=serializer.validated_data.get('object_id'),
                                         content_type=comment_content_type, user=self.request.user,
                                         text=serializer.validated_data.get('text'))
        commnet.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_content_type = ContentType.objects.get_for_model(BlogPost)
        comment = Comment.objects.create(
            object_id=serializer.validated_data.get('object_id'),
            content_type=comment_content_type,
            user=self.request.user,
            text=serializer.validated_data.get('text')
        )

        # Assuming AnotherSerializer is the serializer you want to use for the response
        another_serializer = CommentSerializer(comment)

        headers = self.get_success_headers(another_serializer.data)
        return Response(another_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BlogCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateBlogSerializer

    def post(self, request, *args, **kwargs):
        print(
            request.data
        )
        request.data['user'] = request.user.id

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(
                serializer.errors
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUnfollowBlogApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        blog_id = request.query_params.get('blog_id', None)
        blog = Blog.objects.get(id=blog_id)
        if blog.followers.filter(id=request.user.id).exists():
            blog.followers.remove(request.user)
            return Response({'message': 'unfollowed', 'is_followed': False})
        else:
            blog.followers.add(request.user)
            message = Message.objects.create(
                message=f"{request.user.username} followed you",
                title="New Follower",
               data={
                    'type': 'follow',
                    'user': request.user.id
                }
            )
            message.recipients.set([request.user.id])
            message.save()
            return Response({'message': 'followed', 'is_followed': True})
