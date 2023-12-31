from rest_framework import serializers

from notifications.models import Message
from useraccount.models import UserAccount


class MessageSerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_is_read(self, obj):
        user = self.context.get('request').user
        return user in obj.read_by.all()