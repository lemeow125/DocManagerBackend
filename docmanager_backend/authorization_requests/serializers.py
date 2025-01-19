from rest_framework import serializers
from accounts.models import CustomUser
from emails.templates import RequestUpdateEmail
from .models import AuthorizationRequest, AuthorizationRequestUnit


class AuthorizationRequestUnitCreationSerializer(serializers.ModelSerializer):
    document = serializers.CharField()
    copies = serializers.IntegerField(min_value=1)
    pages = serializers.IntegerField(min_value=1)

    class Meta:
        model = AuthorizationRequestUnit
        fields = ["document", "copies", "pages", "status"]


class AuthorizationRequestUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthorizationRequestUnit
        fields = ["id", "document", "status", "copies", "pages"]
        read_only_fields = ["id", "document", "status," "copies", "pages"]


class AuthorizationRequestCreationSerializer(serializers.ModelSerializer):
    requester = serializers.SlugRelatedField(
        many=False, slug_field="id", queryset=CustomUser.objects.all(), required=False
    )
    documents = AuthorizationRequestUnitCreationSerializer(
        many=True, required=True)
    college = serializers.CharField(max_length=64)
    purpose = serializers.CharField(max_length=512)

    class Meta:
        model = AuthorizationRequest
        fields = ["requester", "college", "purpose", "documents"]

    def create(self, validated_data):
        user = self.context["request"].user
        documents_data = validated_data.pop("documents")
        if not documents_data:
            raise serializers.ValidationError(
                {"error": "No documents provided"}
            )
        # Set requester to user who sent HTTP request to prevent spoofing
        validated_data["requester"] = user

        AUTHORIZATION_REQUEST = AuthorizationRequest.objects.create(
            **validated_data)

        AUTHORIZATION_REQUEST_UNITS = []
        for AUTHORIZATION_REQUEST_UNIT in documents_data:
            AUTHORIZATION_REQUEST_UNIT = AuthorizationRequestUnit.objects.create(
                authorization_request=AUTHORIZATION_REQUEST,
                document=AUTHORIZATION_REQUEST_UNIT["document"],
                copies=AUTHORIZATION_REQUEST_UNIT["copies"],
                pages=AUTHORIZATION_REQUEST_UNIT["pages"]
            )
            AUTHORIZATION_REQUEST_UNITS.append(AUTHORIZATION_REQUEST_UNIT)

        AUTHORIZATION_REQUEST.documents.set(AUTHORIZATION_REQUEST_UNITS)
        AUTHORIZATION_REQUEST.save()

        return AUTHORIZATION_REQUEST


class AuthorizationRequestSerializer(serializers.ModelSerializer):
    requester = serializers.SlugRelatedField(
        many=False,
        slug_field="full_name",
        queryset=CustomUser.objects.all(),
    )
    date_requested = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )
    documents = AuthorizationRequestUnitSerializer(many=True)

    class Meta:
        model = AuthorizationRequest
        fields = [
            "id",
            "requester",
            "college",
            "purpose",
            "date_requested",
            "documents",
            "remarks",
            "status",
        ]
        read_only_fields = [
            "id",
            "requester",
            "college",
            "purpose",
            "date_requested",
            "documents",
            "remarks,"
            "status",
        ]


class AuthorizationRequestUnitUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=AuthorizationRequestUnit.STATUS_CHOICES, required=True
    )

    class Meta:
        model = AuthorizationRequestUnit
        fields = ["id", "status"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        if instance.authorization_request.status != "pending":
            raise serializers.ValidationError(
                {
                    "error": "Already approved/denied requests cannot be updated. You should instead create a new request and approve it from there"
                }
            )
        if instance.status == "checked":
            raise serializers.ValidationError(
                {
                    "error": "Already approved/denied request units cannot be updated. You should instead create a new request and approve it from there"
                }
            )
        elif "status" not in validated_data:
            raise serializers.ValidationError(
                {
                    "error": "No status value update provided"
                }
            )
        elif validated_data["status"] == instance.status:
            raise serializers.ValidationError(
                {"error": "Request unit status provided is the same as current status"}
            )
        representation = super().update(instance, validated_data)

        # Check if the parent Authorization Request has had all its documents approved
        approved_all = True
        for AUTHORIZATION_REQUEST_UNIT in instance.authorization_request.documents.all():
            if AUTHORIZATION_REQUEST_UNIT.status != "checked":
                approved_all = False

        # If all documents have been checked
        if approved_all:
            # Set the parent request as approved
            instance.authorization_request.status = "approved"
            instance.authorization_request.save()
            # And send an email notification
            email = RequestUpdateEmail()
            email.context = {"request_status": "approved"}
            email.send(to=[instance.authorization_request.requester.email])
        return representation


class AuthorizationRequestUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=AuthorizationRequest.STATUS_CHOICES, required=True
    )

    class Meta:
        model = AuthorizationRequest
        fields = ["id", "status", "remarks"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        if "status" not in validated_data:
            raise serializers.ValidationError(
                {
                    "error": "No status value update provided"
                }
            )
        elif instance.status == "denied" or instance.status == "claimed":
            raise serializers.ValidationError(
                {
                    "error": "Already claimed/denied requests cannot be updated. You should instead create a new request and approve it from there"
                }
            )
        elif validated_data["status"] == instance.status:
            raise serializers.ValidationError(
                {"error": "Request form status provided is the same as current status"}
            )
        elif instance.status == "approved" and validated_data["status"] not in ["claimed", "unclaimed"]:
            raise serializers.ValidationError(
                {"error": "Approved request forms can only be marked as claimed or unclaimed"}
            )
        elif instance.status == "unclaimed" and validated_data["status"] not in ["claimed"]:
            raise serializers.ValidationError(
                {"error": "Unclaimed request forms can only be marked as claimed"}
            )
        elif validated_data["status"] == "denied" and "remarks" not in validated_data:
            raise serializers.ValidationError(
                {"error": "Request denial requires remarks"}
            )
        representation = super().update(instance, validated_data)

        # Send an email on request status update
        try:
            email = RequestUpdateEmail()
            if validated_data["status"] == "denied":
                email.context = {"request_status": "denied"}
                email.context = {"remarks": validated_data["remarks"]}
            else:
                email.context = {"request_status": "approved"}
                email.context = {"remarks": "N/A"}
            email.send(to=[instance.requester.email])
        except Exception as e:
            # Silence out errors if email sending fails
            print(e)
            pass

        return representation
