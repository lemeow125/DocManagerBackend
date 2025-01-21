from rest_framework import generics
from django.db.models import Q
from .serializers import NotificationSerializer
from .models import Notification
from rest_framework.permissions import IsAuthenticated


class NotificationListView(generics.ListAPIView):
    """
    Used by all users to view notifications. Returns user-specific notifications for clients.

    Returns role-wide notifications for staff and head roles
    """

    http_method_names = ["get"]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all().order_by("-timestamp")
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "client":
            queryset = Notification.objects.filter(client=user)
        elif user.role == "staff":
            queryset = Notification.objects.filter(audience="staff")
        elif user.role in ["head", "admin"]:
            queryset = Notification.objects.filter(
                Q(audience="staff") | Q(audience="head"))
        return queryset


class NotificationDeleteView(generics.DestroyAPIView):
    """
    Used by all users to dismiss or delete notifications.
    """

    http_method_names = ["delete"]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all().order_by("-timestamp")
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "client":
            return Notification.objects.filter(client=user)
        elif user.role == "staff":
            return Notification.objects.filter(audience="staff")
        else:
            # For head or admin roles
            return Notification.objects.filter(
                Q(audience="head") | Q(audience="staff")
            )
