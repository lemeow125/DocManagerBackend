from rest_framework import serializers
from config import settings
from .models import Document


class DocumentUploadSerializer(serializers.ModelSerializer):
    # For staff
    file = serializers.FileField()
    date_uploaded = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )

    class Meta:
        model = Document
        fields = [
            "id",
            "name",
            "file",
            "document_type",
            "number_pages",
            "date_uploaded",
        ]
        read_only_fields = ["id", "date-uploaded"]


class DocumentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id"]


class DocumentSerializer(serializers.ModelSerializer):
    # Read-only serializer
    date_uploaded = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )

    class Meta:
        model = Document
        fields = ["id", "name", "document_type", "number_pages", "date_uploaded"]
        read_only_fields = [
            "id",
            "name",
            "document_type",
            "number_pages",
            "date_uploaded",
        ]


class DocumentFileSerializer(serializers.ModelSerializer):
    # Read-only serializer which includes the actual link to the file
    date_uploaded = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )
    file = serializers.FileField()

    class Meta:
        model = Document
        fields = [
            "id",
            "name",
            "document_type",
            "file",
            "number_pages",
            "date_uploaded",
        ]
        read_only_fields = [
            "id",
            "name",
            "document_type",
            "number_pages",
            "date_uploaded",
            "file",
        ]
