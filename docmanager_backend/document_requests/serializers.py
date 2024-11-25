from rest_framework import serializers
from documents.models import Document
from documents.serializers import DocumentSerializer, DocumentFileSerializer
from accounts.models import CustomUser
from emails.templates import RequestUpdateEmail
from .models import DocumentRequest, DocumentRequestUnit


class DocumentRequestUnitCreationSerializer(serializers.ModelSerializer):
    document = serializers.SlugRelatedField(
        many=False, slug_field="id", queryset=Document.objects.all(), required=True
    )
    copies = serializers.IntegerField(min_value=1)

    class Meta:
        model = DocumentRequestUnit
        fields = ["document", "copies"]


class DocumentRequestCreationSerializer(serializers.ModelSerializer):
    requester = serializers.SlugRelatedField(
        many=False, slug_field="id", queryset=CustomUser.objects.all(), required=False
    )
    documents = DocumentRequestUnitCreationSerializer(many=True, required=True)
    college = serializers.CharField(max_length=64)
    purpose = serializers.CharField(max_length=512)
    type = serializers.ChoiceField(
        choices=DocumentRequest.TYPE_CHOICES, required=True)

    class Meta:
        model = DocumentRequest
        fields = ["requester", "college", "type", "purpose", "documents"]

    def create(self, validated_data):
        user = self.context["request"].user
        documents_data = validated_data.pop("documents")
        # Set requester to user who sent HTTP request to prevent spoofing
        validated_data["requester"] = user

        DOCUMENT_REQUEST = DocumentRequest.objects.create(**validated_data)

        DOCUMENT_REQUEST_UNITS = []
        for DOCUMENT_REQUEST_UNIT in documents_data:
            DOCUMENT_REQUEST_UNIT = DocumentRequestUnit.objects.create(
                document_request=DOCUMENT_REQUEST,
                document=DOCUMENT_REQUEST_UNIT["document"],
                copies=DOCUMENT_REQUEST_UNIT["copies"],
            )
            DOCUMENT_REQUEST_UNITS.append(DOCUMENT_REQUEST_UNIT)

        DOCUMENT_REQUEST.documents.set(DOCUMENT_REQUEST_UNITS)
        DOCUMENT_REQUEST.save()

        return DOCUMENT_REQUEST


class DocumentRequestUnitSerializer(serializers.ModelSerializer):
    document = DocumentSerializer(many=False)

    class Meta:
        model = DocumentRequestUnit
        fields = ["id", "document", "copies"]
        read_only_fields = ["id", "document", "copies"]


class DocumentRequestUnitWithFileSerializer(serializers.ModelSerializer):
    document = DocumentFileSerializer(many=False)

    class Meta:
        model = DocumentRequestUnit
        fields = ["id", "document", "copies"]
        read_only_fields = ["id", "document", "copies"]


class DocumentRequestSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()
    requester = serializers.SlugRelatedField(
        many=False, slug_field="email", queryset=CustomUser.objects.all(), required=False
    )
    purpose = serializers.CharField(max_length=512)
    date_requested = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )

    class Meta:
        model = DocumentRequest
        fields = [
            "id",
            "requester",
            "college",
            "type",
            "purpose",
            "date_requested",
            "documents",
            "status",
        ]
        read_only_fields = [
            "id",
            "requester",
            "college",
            "type",
            "purpose",
            "date_requested",
            "documents",
            "status",
        ]

    def get_documents(self, obj):
        if obj.status != "approved":
            serializer_class = DocumentRequestUnitSerializer
        else:
            serializer_class = DocumentRequestUnitWithFileSerializer
        return serializer_class(obj.documents, many=True).data


class FullDocumentRequestSerializer(serializers.ModelSerializer):
    documents = DocumentRequestUnitWithFileSerializer()
    requester = serializers.SlugRelatedField(
        many=False, slug_field="email", queryset=CustomUser.objects.all(), required=False
    )
    purpose = serializers.CharField(max_length=512)
    date_requested = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )

    class Meta:
        model = DocumentRequest
        fields = [
            "id",
            "requester",
            "college",
            "type",
            "purpose",
            "date_requested",
            "documents",
            "status",
        ]
        read_only_fields = [
            "id",
            "requester",
            "college",
            "type",
            "purpose",
            "date_requested",
            "documents",
            "status",
        ]


class DocumentRequestUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=DocumentRequest.STATUS_CHOICES, required=True
    )

    class Meta:
        model = DocumentRequest
        fields = ["id", "status"]
        read_only_fields = ["id", "status"]

    def update(self, instance, validated_data):
        if instance.status == "denied" or instance.status == "approved":
            raise serializers.ValidationError(
                {
                    "error": "Already approved/denied requests cannot be updated. You should instead create a new request and approve it from there"
                }
            )
        elif validated_data["status"] == instance.status:
            raise serializers.ValidationError(
                {"error": "Request form status provided is the same as current status"}
            )

        representation = super().update(instance, validated_data)

        # Send an email on request status update
        try:
            email = RequestUpdateEmail()
            email.context = {"request_status": instance.status}
            email.send(to=[instance.requester.email])
        except:
            # Silence out errors if email sending fails
            pass

        return representation
