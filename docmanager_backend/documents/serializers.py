from rest_framework import serializers
from .models import Document


class DocumentUpdateSerializer(serializers.ModelSerializer):
    # For Head to edit document info
    file = serializers.FileField(required=False)

    class Meta:
        model = Document
        fields = [
            "name",
            "file",
            "document_type",
            "number_pages",
            "date_uploaded",
        ]
        read_only_fields = ["id"]


class DocumentUploadSerializer(serializers.ModelSerializer):
    # For staff document uploads
    date_uploaded = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )
    file = serializers.FileField()

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
    # Read-only serializer without link to the file
    date_uploaded = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )

    class Meta:
        model = Document
        fields = [
            "id",
            "name",
            "document_type",
            "number_pages",
            "ocr_metadata",
            "date_uploaded",
        ]
        read_only_fields = [
            "id",
            "name",
            "document_type",
            "number_pages",
            "ocr_metadata",
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
            "number_pages",
            "ocr_metadata",
            "date_uploaded",
            "file",
        ]
        read_only_fields = [
            "id",
            "name",
            "document_type",
            "number_pages",
            "ocr_metadata",
            "date_uploaded",
            "file",
        ]
