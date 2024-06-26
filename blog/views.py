import json

from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404
from django.shortcuts import get_object_or_404, render
from django.views import View
from django_quill.quill import Quill
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from commentable.models import Comment
from commentable.serializers import CommentSerializer, CommentOnPostCreateSerializer
from djangoProject1.send_notification_service import SendNotificationService
from likable.models import Like
from notifications.models import Message
from useraccount.api.serializers.user_api_serializer import CategorySerializer
from useraccount.models import Category
from .models import Blog, BlogPost, ArticleComment, PostLikeModel, ArticleCommentLikeModel
from rest_framework import generics, status

from .serializers import BlogSerializer, BlogPostSerializer, BlogPostNewSerializer, CreateBlogSerializer, \
    BlogCommentSerializer


class PaginationList(PageNumberPagination):
    page_size = 50
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
    # filter_backends = [SearchFilter]
    pagination_class = PaginationList
    # search_fields = ['category__name']  # Assuming 'name' is a field in your Category model

    def get_queryset(self):
        return BlogPost.objects.all().order_by('-updated_at')
class RecommendedBlogListView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        blogs = Blog.objects.order_by('?')
        return Response(BlogSerializer(blogs, many=True, context={
            'request': request
        }).data)


# class GetBlogPostsComments(APIView):
#
#     def get(self, request):
#         post_id = self.request.query_params.get('id', None)
#         post = BlogPost.objects.get(id=post_id)
#         comments = post.comments.all()
#         likes = Like.objects.filter(content_type=ContentType.objects.get_for_model(BlogPost), object_id=post_id)
#
#         return Response({'comments': CommentSerializer(comments, many=True).data, 'parent_likes_count': likes.count(),
#                          'isLiked': likes.filter(user=request.user).exists()})


class LikeAndUnlikeArticle(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        post_id = request.query_params.get('article_id', None)
        post = BlogPost.objects.get(id=post_id)
        if PostLikeModel.objects.filter(
                user=request.user,
                post=post
        ).exists():
            like = PostLikeModel.objects.get(
                user=request.user,
                post=post
            )
            like.delete()
            return Response({"parent_likes_count": PostLikeModel.objects.filter(
                post=post
            ).count(), 'message': 'unliked', 'isLiked': False},
                            status=status.HTTP_200_OK)
        else:
            like = PostLikeModel.objects.create(
                user=request.user,
                post=post
            )
            like.save()

            return Response({"parent_likes_count": PostLikeModel.objects.filter(
                post=post
            ).count(), 'message': 'like', 'isLiked': True},
                            status=status.HTTP_200_OK)
        # if post.likes.filter(d
        #         user=request.user
        #
        # ).exists():
        #     like = Like.objects.get(
        #         user=request.user,
        #         object_id=post_id,
        #         content_type=ContentType.objects.get_for_model(post)
        #     )
        #     like.delete()
        #
        #     return Response({"parent_likes_count": post.likes.count(), 'message': 'unliked', 'isLiked': False},
        #                     status=status.HTTP_200_OK)
        #
        # else:
        #     like = Like.objects.create(
        #         user=request.user,
        #         object_id=post_id,
        #         content_type=ContentType.objects.get_for_model(post)
        #     )
        #     like.save()
        #     return Response({"parent_likes_count": post.likes.count(), 'message': 'liked', 'isLiked': True},
        #                     status=status.HTTP_200_OK)


class BlogScreenView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        blog_id = request.query_params.get('blog_id', None)
        blog = Blog.objects.get(id=blog_id)
        featured_posts = BlogPost.objects.filter(blog=blog, is_featured=True).order_by('-updated_at')[:5]
        filter = request.query_params.get('filter', None)
        if filter:
            posts = BlogPost.objects.filter(blog=blog, is_banned=False, category__name=filter).order_by('-updated_at')
        else:
            posts = BlogPost.objects.filter(blog=blog, is_banned=False).order_by('-updated_at')
        return Response({
            'posts': BlogPostNewSerializer(posts, many=True, context={'request': request}).data,
            'blog': BlogSerializer(blog, context={'request': request}).data,
            'is_followed': blog.followers.filter(id=request.user.id).exists(),
            'featured_posts': BlogPostNewSerializer(featured_posts, many=True, context={'request': request}).data,
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

        request.data['user'] = request.user.id

        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            instance = serializer.instance
            # retireve list of integers from string list
            category_ids = request.data.get('category', [])
            # category_ids = list(map(int, category_ids))
            for category_id in category_ids:
                try:
                    if category_id.isdigit():
                        category = Category.objects.get(id=category_id)
                        instance.category.add(category)
                    else:
                        pass
                except Category.DoesNotExist:
                    # Handle the case where the category doesn't exist
                    pass
            instance.save()
            return Response(BlogSerializer(
                instance, context={'request': request}
            ).data, status=status.HTTP_201_CREATED)
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
            message.recipients.set([
                blog.user.id
            ])
            message.save()
            return Response({'message': 'followed', 'is_followed': True})


class UpdateBlogPatchApiView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(BlogSerializer(
                Blog.objects.get(id=serializer.data.get('id'), ), context={'request': request}
            ).data, status=status.HTTP_201_CREATED)
        else:
            print(
                serializer.errors
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateBlogPost(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogPostNewSerializer

    def post(self, request, *args, **kwargs):
        request.data['blog'] = request.data.get('blog_id')
        category_ids = request.data.get('categories', [])
        request.data['category'] = category_ids
        request.data['is_featured'] = request.data.get('is_featured') == 'true'
        request.data['is_banned'] = request.data.get('is_banned') == 'true'
        request.data['content'] = request.data.get('content')
        request.data['cover'] = request.data.get('cover')
        request.data['title'] = request.data.get('title')

        post = BlogPost.objects.create(

            blog=Blog.objects.get(id=request.data.get('blog_id')),
            title=request.data.get('title'),
            is_banned=request.data.get('is_banned'),
            is_featured=request.data.get('is_featured'),
            content=request.data.get('content'),
            cover=request.data.get('cover'),
        )
        categories_str = request.data.get('categories', '[]')

        # Use json.loads to convert the string into a Python list
        category_ids = json.loads(categories_str)
        post.category.set(Category.objects.filter(id__in=category_ids))
        # post.content = quill
        post.save()
        print(BlogPostNewSerializer(post, context={"request": request}).data)

        return Response(BlogPostNewSerializer(post, context={"request": request}).data, status=status.HTTP_201_CREATED)


class GetArticlesByCategory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        category_id = request.query_params.get('category_id', None)
        category = Category.objects.get(id=category_id)
        # randomly
        posts = BlogPost.objects.filter(category=category, is_banned=False).order_by('?')
        print(posts)
        return Response(BlogPostSerializer(posts, many=True).data)


class GetArticleComments(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        post_id = request.query_params.get('post_id', None)
        post = BlogPost.objects.get(id=post_id)
        comments = ArticleComment.objects.filter(post=post)

        return Response(
            {
                'comments': BlogCommentSerializer(comments, many=True, context={
                    'request': request
                }).data,
                'isLiked': PostLikeModel.objects.filter(post = post, user=request.user).exists(),
                'likes_count': PostLikeModel.objects.filter(post = post).count()
            }
        )


class CommentOnArticle(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        post_id = request.data.get('post_id', None)
        post = BlogPost.objects.get(id=post_id)
        comment = ArticleComment.objects.create(
            post=post,
            user=request.user,
            content=request.data.get('content')
        )
        SendNotificationService.seneMessagewithPaylod(
            title="New Comment",
            message=f"{request.user.first_name} {request.user.last_name} commented on your post",
            data={
                'type': 'blog_comment',
                'user': request.user.id,
                'postId': post.id,
                'post' : BlogPostNewSerializer(post, many=False, context={
                    'request': request}).data

            },
            recipients=[post.blog.user.id]
        )
        return Response({
            "comment" : BlogCommentSerializer(comment, many=False, context={
                    'request': request
                }).data,
        })
class EditBlogView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        blog_id = request.data.get('blog_id', None)
        blog = Blog.objects.get(id=blog_id)
        blog.title = request.data.get('title')
        blog.description = request.data.get('description')
        blog.cover = request.data.get('cover', blog.cover)
        category_ids = request.data.get('category', [])
        for category_id in category_ids:
            try:
                if category_id.isdigit():
                    category = Category.objects.get(id=category_id)
                    blog.category.add(category)
                else:
                    pass
            except Category.DoesNotExist:
                # Handle the case where the category doesn't exist
                pass
        blog.save()

        # blog.save()
        return Response(
            BlogSerializer(blog, context={
                'request': request
            }).data
        )

class ArticlesSearch(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        search_query = request.query_params.get('search', '')  # Retrieve 'search' query parameter
        posts = BlogPost.objects.filter(content__icontains=search_query).order_by('-updated_at')
        return Response(BlogPostNewSerializer(posts, many=True, context={
            'request': request
        }).data)


class BlogsSearchView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        search_query = request.query_params.get('search', '')  # Retrieve 'search' query parameter
        blogs = Blog.objects.filter(title__icontains=search_query)
        return Response(BlogSerializer(blogs, many=True, context={
            'request': request
        }).data)