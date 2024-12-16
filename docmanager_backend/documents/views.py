from rest_framework import generics
from .serializers import (
    DocumentSerializer,
    DocumentFileSerializer,
    DocumentUploadSerializer,
    DocumentDeleteSerializer,
    DocumentUpdateSerializer
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from accounts.permissions import IsStaff, IsHead
from .models import Document


class DocumentUpdateView(generics.UpdateAPIView):
    """
    Used by staff to upload documents.
    """

    http_method_names = ["patch"]
    serializer_class = DocumentUpdateSerializer
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated, IsHead]


class DocumentUploadView(generics.CreateAPIView):
    """
    Used by staff to upload documents.
    """

    http_method_names = ["post"]
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated, IsStaff]


class DocumentDeleteView(generics.DestroyAPIView):
    """
    Used by staff to delete documents. Accepts the document id as a URL parameter
    """

    http_method_names = ["delete"]
    serializer_class = DocumentDeleteSerializer
    queryset = Document.objects.all()
    permission_classes = [IsAuthenticated, IsStaff]


class DocumentListView(generics.ListAPIView):
    """
    Used by clients to view documents. Does not include actual download links to documents
    """

    http_method_names = ["get"]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all().order_by("-date_uploaded")
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]


class DocumentStaffListView(generics.ListAPIView):
    """
    Used by staff to view documents. Includes actual download links to documents
    """

    http_method_names = ["get"]
    serializer_class = DocumentFileSerializer
    queryset = Document.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated, IsStaff]
