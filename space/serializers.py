from actstream import action
from actstream.models import Action, user_stream
from rest_framework import serializers, viewsets

from djangoProject1.firebase_services import FirebaseServices
from notifications.models import Message
# from post.serializers import SpacePostSerializer
from space.models import Space, PostComment, CommentReply, CommentLike, ReplyLike, SpacePost
from useraccount.api.serializers.user_api_serializer import CategorySerializer
from useraccount.models import UserAccount
from useraccount.serializers import FullUserSerializer, SpaceUserSerializer


class SimpleSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'cover']


class SpaceSerializer(serializers.ModelSerializer):
    # posts = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Space
        fields = '__all__'

    # def get_posts(self, obj):
    #     request = self.context.get('request')
    #     return SpacePostSerializer(obj.posts.all(), many=True, read_only=True, context={'request': request}).data

    def get_users(self, obj):
        included_users = obj.include_users.all()
        return SpaceUserSerializer(included_users, many=True).data


class JoinSpaceSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        space_id = attrs.get('id')
        print(space_id)
        user = self.context['request'].user
        space = Space.objects.filter(id=space_id).first()
        if space is None:
            raise serializers.ValidationError("Space not found")
        if space.is_allowed_to_join(space, user):
            if space.exclude_users.filter(id=user.id).exists():
                raise serializers.ValidationError("You are not allowed to join this space")
            else:
                space.include_users.add(user)
                space.save()
                action.send(user, verb='joined', target=space)

                return attrs
        else:
            raise serializers.ValidationError("You are not allowed to join this space")

    def update(self, instance, validated_data):
        print("asdasdasd")
        space_id = validated_data.get('id')
        user = self.context['request'].user

        space = Space.objects.filter(id=space_id).first()
        if space is None:
            raise serializers.ValidationError("Space not found")
        if space.is_allowed_to_join(space, user):
            if space.exclude_users.filter(id=user.id).exists():
                raise serializers.ValidationError("You are not allowed to join this space")
            else:
                space.include_users.add(user)
                space.save()
                action.send(user, verb='joined', target=space)
                FirebaseServices.sendNotification(
                    title="New Member",
                    message=f"{user.first_name} {user.last_name} joined {space.name}",
                    data={"type": "space", "id": space.id},
                    recipients=[user.id]
                )

                return instance
        instance.save()
        return instance


class LeaveSpaceSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def validate(self, attrs):
        space_id = attrs.get('id')
        user = self.context['request'].user
        space = Space.objects.filter(id=space_id).first()
        if space is None:
            raise serializers.ValidationError("Space not found")
        else:
            print("removed")
            space.include_users.remove(user)
            space.save()
            return attrs

    def update(self, instance, validated_data):
        instance.save()
        return instance


class ActivitySerializer(serializers.ModelSerializer):
    actor = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()
    action_object = serializers.SerializerMethodField()
    verb = serializers.SerializerMethodField()
    target_content_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Action
        fields = '__all__'

    def get_actor(self, obj):
        return UserAccount.objects.get(id=obj.actor_object_id).email

    def get_target_content_type_name(self, obj):
        return obj.target_content_type.name

    def get_target(self, obj):
        if obj.target_content_type == 'space':
            return Space.objects.get(id=obj.target_object_id).name

    def get_action_object(self, obj):
        if obj.target_content_type.name == 'space':
            return Space.objects.get(id=obj.target_object_id).name

    def get_verb(self, obj):

        return obj.verb


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        user = self.request.user

        activities = Action.objects.filter(actor_object_id=user.id)

        return activities


class PostlikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):
    from post.serializers import UserPostSerializer
    is_liked = serializers.SerializerMethodField(read_only=True)
    user = UserPostSerializer(read_only=True, many=False)
    replies = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PostComment
        fields = '__all__'

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if obj.interActions.filter(user=user).exists():
                return True
            else:
                return False
        else:
            return False
    def get_replies(self, obj):
        request = self.context.get('request')
        return ReplySerializer(CommentReply.objects.filter(comment=obj)
                               , many=True, context={
                'request': request
            }).data

    def get_likes(self, obj):
        return obj.interActions.count()

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class ReplyLikeSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ReplyLike
        fields = '__all__'

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user in obj.likes.all():
                return True
            else:
                return False


class ReplySerializer(serializers.ModelSerializer):
    from post.serializers import UserPostSerializer
    # is_liked = serializers.SerializerMethodField(read_only=True)
    user = UserPostSerializer(read_only=True, many=False)
    # likes = serializers.SerializerMethodField(read_only=True)
    comment_id = serializers.SerializerMethodField(read_only=True)
    commet_user = serializers.SerializerMethodField(read_only=True)
    comment_text = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CommentReply
        fields = '__all__'

    # def get_is_liked(self, obj):
    #     user = self.context['request'].user
    #
    #
    #     if user.is_authenticated:
    #         if user in obj.likes.all():
    #             return True
    #         else:
    #             return False
    # def get_likes(self, obj):
    #     return CommentLikeSerializer(obj.likes.all(), many=True).data

    def get_comments(self):
        return

    def get_comment_id(self, obj):
        return obj.comment.id

    def get_comment_text(self, obj):
        return obj.comment.content

    def get_commet_user(self, obj):
        from post.serializers import UserPostSerializer
        return UserPostSerializer(obj.comment.user, many=False).data

    # def get_comment(self, obj):
    #     return PostCommentSerializer(obj.comment).data


class MakePostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['content', 'post']
