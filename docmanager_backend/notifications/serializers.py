from rest_framework import serializers
from accounts.models import CustomUser
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(
        many=False, slug_field="id", queryset=CustomUser.objects.all(), required=False
    )
    timestamp = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "client",
            "timestamp",
            "content",
            "type",
            "audience",
        ]
