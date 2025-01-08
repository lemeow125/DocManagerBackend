from rest_framework import serializers
from .models import Document


class DocumentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = [
            "name",
            "document_type",
            "number_pages",
        ]


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
            "sent_from",
            "date_uploaded",
        ]
        read_only_fields = [
            "id",
            "name",
            "document_type",
            "number_pages",
            "ocr_metadata",
            "sent_from",
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
            "sent_from",
            "file",
        ]
        read_only_fields = [
            "id",
            "name",
            "document_type",
            "number_pages",
            "ocr_metadata",
            "date_uploaded",
            "sent_from",
            "file",
        ]
