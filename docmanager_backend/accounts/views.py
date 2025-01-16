from rest_framework import generics
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin
from .models import CustomUser


class CustomUserDeleteView(generics.DestroyAPIView):
    """
    Used by admin to delete users. Accepts the user id as a URL parameter
    """

    http_method_names = ["delete"]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
