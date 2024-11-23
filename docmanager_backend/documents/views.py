from rest_framework import generics
from .serializers import (
    DocumentSerializer,
    DocumentUploadSerializer,
    DocumentDeleteSerializer,
)
from .permissions import IsStaff
from .models import Document
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


class DocumentUploadView(generics.CreateAPIView):
    http_method_names = ["post"]
    serializer_class = DocumentUploadSerializer
    # permission_classes = [IsAuthenticated, IsStaff]


class DocumentDeleteView(generics.DestroyAPIView):
    http_method_names = ["delete"]
    serializer_class = DocumentDeleteSerializer
    queryset = Document.objects.all()
    # permission_classes = [IsAuthenticated, IsStaff]


class DocumentListView(generics.ListAPIView):
    http_method_names = ["get"]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    pagination_class = PageNumberPagination
    # permission_classes = [IsAuthenticated]
