from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from accounts.permissions import IsHead, IsStaff
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    AuthorizationRequestCreationSerializer,
    AuthorizationRequestSerializer,
    AuthorizationRequestUpdateSerializer
)

from .models import AuthorizationRequest


class AuthorizationRequestCreateView(generics.CreateAPIView):
    """
    Used by clients to create authorization requests. Requires passing in request information in addition to the documents themselves
    """

    http_method_names = ["post"]
    serializer_class = AuthorizationRequestCreationSerializer
    permission_classes = [IsAuthenticated]


class AuthorizationRequestListView(generics.ListAPIView):
    """
    Returns authorization requests. If authorization requests are approved, also returns the link to download the document.
    Staff/Head are able to view all authorization requests here. Clients are only able to view their own requests.
    """

    http_method_names = ["get"]
    serializer_class = AuthorizationRequestSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "client":
            queryset = AuthorizationRequest.objects.filter(requester=user)
        else:
            queryset = AuthorizationRequest.objects.all()
        return queryset


class AuthorizationRequestUpdateView(generics.UpdateAPIView):
    """
    Used by head approve or deny authorization requests.
    """

    http_method_names = ["patch"]
    serializer_class = AuthorizationRequestUpdateSerializer
    permission_classes = [IsAuthenticated, IsHead]
    queryset = AuthorizationRequest.objects.all()
