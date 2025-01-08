from rest_framework import serializers
from accounts.models import CustomUser
from emails.templates import RequestUpdateEmail
from .models import AuthorizationRequest


class AuthorizationRequestCreationSerializer(serializers.ModelSerializer):
    requester = serializers.SlugRelatedField(
        many=False, slug_field="id", queryset=CustomUser.objects.all(), required=False
    )
    documents = serializers.CharField(max_length=2048, required=True)
    college = serializers.CharField(max_length=64)
    purpose = serializers.CharField(max_length=512)

    class Meta:
        model = AuthorizationRequest
        fields = ["requester", "college", "purpose", "documents"]

    def create(self, validated_data):
        user = self.context["request"].user

        # Set requester to user who sent HTTP request to prevent spoofing
        validated_data["requester"] = user

        return AuthorizationRequest.objects.create(**validated_data)


class AuthorizationRequestSerializer(serializers.ModelSerializer):
    requester = serializers.SlugRelatedField(
        many=False,
        slug_field="full_name",
        queryset=CustomUser.objects.all(),
    )
    date_requested = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )

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


class AuthorizationRequestUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=AuthorizationRequest.STATUS_CHOICES, required=True
    )

    class Meta:
        model = AuthorizationRequest
        fields = ["id", "status", "remarks"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        print(validated_data)
        if instance.status == "denied" or instance.status == "approved":
            raise serializers.ValidationError(
                {
                    "error": "Already approved/denied requests cannot be updated. You should instead create a new request and approve it from there"
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
                {"error": "Request form status provided is the same as current status"}
            )
        elif validated_data["status"] == "denied" and "remarks" not in validated_data:
            raise serializers.ValidationError(
                {"error": "Request denial requires remarks"}
            )
        representation = super().update(instance, validated_data)

        # Send an email on request status update
        try:
            email = RequestUpdateEmail()
            email.context = {"request_status": validated_data["status"]}
            if validated_data["status"] == "denied":
                email.context = {"remarks": validated_data["remarks"]}
            else:
                email.context = {"remarks": "N/A"}
            email.send(to=[instance.requester.email])
        except:
            # Silence out errors if email sending fails
            pass

        return representation
