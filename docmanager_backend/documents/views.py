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
from django.db.models import Q
from operator import or_
from functools import reduce


class DocumentPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4


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
    queryset = Document.objects.all().order_by("-date_uploaded")
    pagination_class = DocumentPagination
    permission_classes = [IsAuthenticated, IsStaff]

    def get_queryset(self):
        # Get the base queryset
        queryset = super().get_queryset()

        # Check if 'keywords' query parameter is present
        keyword = self.request.query_params.get('search', None)

        if keyword:
            queries = []
            # Create a list to hold individual field conditions for this keyword
            field_queries = [
                Q(name__icontains=keyword),
                Q(document_type__icontains=keyword),
                Q(sent_from__icontains=keyword),
                Q(document_month__icontains=keyword),
                Q(document_year__icontains=keyword),
                Q(subject__icontains=keyword),
                Q(ocr_metadata__icontains=keyword)
            ]
            # Combine the field conditions with OR
            combined_query = Q()
            for q in field_queries:
                if not combined_query:
                    combined_query = q
                else:
                    combined_query |= q
            queries.append(combined_query)

            # Now combine all keyword conditions with OR
            final_query = Q()
            for q in queries:
                if not final_query:
                    final_query = q
                else:
                    final_query |= q

            queryset = queryset.filter(final_query)

        return queryset
