from rest_framework import serializers
from accounts.models import CustomUser
from document_requests.models import DocumentRequest
from .models import Questionnaire


class QuestionnaireSerializer(serializers.ModelSerializer):
    document_request = serializers.SlugRelatedField(
        many=False,
        slug_field="id",
        queryset=DocumentRequest.objects.all(),
        required=True,
        allow_null=True,
    )
    client = serializers.SlugRelatedField(
        many=False,
        slug_field="email",
        queryset=CustomUser.objects.all(),
        required=False,
    )
    client_type = serializers.ChoiceField(
        choices=Questionnaire.CLIENT_TYPE_CHOICES)

    date_submitted = serializers.DateTimeField(
        format="%m-%d-%Y %I:%M %p", read_only=True
    )
    age = serializers.SerializerMethodField()
    sex = serializers.SerializerMethodField()
    region_of_residence = serializers.CharField(max_length=64)
    service_availed = serializers.CharField(max_length=64)
    i_am_a = serializers.ChoiceField(choices=Questionnaire.I_AM_I_CHOICES)
    i_am_a_other = serializers.CharField(required=False, allow_blank=True)
    q1_answer = serializers.ChoiceField(choices=Questionnaire.Q1_CHOICES)
    q2_answer = serializers.ChoiceField(choices=Questionnaire.Q2_CHOICES)
    q3_answer = serializers.ChoiceField(choices=Questionnaire.Q3_CHOICES)
    sqd0_answer = serializers.ChoiceField(choices=Questionnaire.SQD_CHOICES)
    sqd1_answer = serializers.ChoiceField(choices=Questionnaire.SQD_CHOICES)
    sqd3_answer = serializers.ChoiceField(choices=Questionnaire.SQD_CHOICES)
    sqd4_answer = serializers.ChoiceField(choices=Questionnaire.SQD_CHOICES)
    sqd5_answer = serializers.ChoiceField(choices=Questionnaire.SQD_CHOICES)
    sqd6_answer = serializers.ChoiceField(choices=Questionnaire.SQD_CHOICES)
    sqd7_answer = serializers.ChoiceField(choices=Questionnaire.SQD_CHOICES)
    sqd8_answer = serializers.ChoiceField(choices=Questionnaire.SQD_CHOICES)
    extra_suggestions = serializers.CharField(
        max_length=512, required=False, allow_blank=True)

    def get_age(self, obj):
        return obj.client.age

    def get_sex(self, obj):
        return obj.client.sex

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["client"] = instance.client.email
        return super().to_representation(instance)

    def create(self, validated_data):
        user = self.context["request"].user
        # Set questionnaire user to the one who sent the HTTP request to prevent spoofing
        validated_data["client"] = user

        if (
            validated_data["client_type"] == "other"
            and not validated_data["client_type_other"]
        ):
            raise serializers.ValidationError(
                {"error": "Missing description for client type: Other"}
            )

        if "document_request" in validated_data:
            if validated_data["document_request"]:
                document_request_id = validated_data["document_request"].id
            else:
                document_request_id = None
            del validated_data["document_request"]

        instance = self.Meta.model(**validated_data)

        # Explicitly set the client_type attribute
        instance.client_type = validated_data.get("client_type")
        # Save the instance
        instance.save()

        # Update associated document request if it exists
        if document_request_id:
            DOCUMENT_REQUEST = DocumentRequest.objects.get(
                id=document_request_id
            )
            DOCUMENT_REQUEST.questionnaire = instance
            DOCUMENT_REQUEST.save()

        return instance

    class Meta:
        model = Questionnaire
        fields = [
            "id",
            "document_request",
            "client",
            "client_type",
            "date_submitted",
            "sex",
            "age",
            "region_of_residence",
            "service_availed",
            "i_am_a",
            "i_am_a_other",
            "q1_answer",
            "q2_answer",
            "q3_answer",
            "sqd0_answer",
            "sqd1_answer",
            "sqd2_answer",
            "sqd3_answer",
            "sqd4_answer",
            "sqd5_answer",
            "sqd6_answer",
            "sqd7_answer",
            "sqd8_answer",
            "extra_suggestions",
        ]
        read_only_fields = ["id", "date_submitted"]
