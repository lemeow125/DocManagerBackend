from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from accounts.permissions import IsHead
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    DocumentRequestCreationSerializer,
    DocumentRequestSerializer,
    DocumentRequestUpdateSerializer,
)

from .models import DocumentRequest


class DocumentRequestCreateView(generics.CreateAPIView):
    """
    Used by clients to create document requests. Requires passing in request information in addition to the documents themselves
    """

    http_method_names = ["post"]
    serializer_class = DocumentRequestCreationSerializer
    permission_classes = [IsAuthenticated]


class DocumentRequestListView(generics.ListAPIView):
    """
    Returns document requests. If document requests are approved, also returns the link to download the document.
    Staff are able to view all document requests here. Clients are only able to view their own requests.
    """

    http_method_names = ["get"]
    serializer_class = DocumentRequestSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "client":
            queryset = DocumentRequest.objects.filter(requester=user)
        else:
            queryset = DocumentRequest.objects.all()
        return queryset


class DocumentRequestFullListView(generics.ListAPIView):
    """
    Returns document requests. Always returns the link to download the document.
    Head is able to view all document requests here. Staff and clients have no access
    """

    http_method_names = ["get"]
    serializer_class = DocumentRequestSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, IsHead]
    queryset = DocumentRequest.objects.all()


class DocumentRequestUpdateView(generics.UpdateAPIView):
    """
    Used by head approve or deny document requests.
    """

    http_method_names = ["patch"]
    serializer_class = DocumentRequestUpdateSerializer
    permission_classes = [IsAuthenticated, IsHead]
    queryset = DocumentRequest.objects.all()
