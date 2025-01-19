from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework.settings import api_settings
from django.utils.timezone import now, localdate


class CustomUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            "role"
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    birthday = serializers.DateField(format="%m-%d-%Y")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "birthday",
            "age",
            "sex",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "username",
            "email",
            "full_name",
            "role",
            "birthday",
            "age",
            "sex",
            "date_joined",
        ]


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, style={"input_type": "password", "placeholder": "Password"}
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    birthday = serializers.DateField(format="%m-%d-%Y", required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name",
                  "last_name", "sex", "birthday"]

    def validate(self, attrs):
        user_attrs = attrs.copy()
        user = self.Meta.model(**user_attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            errors = serializer_error[api_settings.NON_FIELD_ERRORS_KEY]
            if len(errors) > 1:
                raise serializers.ValidationError({"password": errors[0]})
            else:
                raise serializers.ValidationError({"password": errors})
        if self.Meta.model.objects.filter(username=attrs.get("email")).exists():
            raise serializers.ValidationError(
                "A user with that email already exists.")

        # Only allow major email providers
        email = attrs.get("email")
        allowed_email_domains = ["gmail.com", "outlook.com", "ustp.edu.ph"]

        if not any(provider in email for provider in allowed_email_domains):
            raise serializers.ValidationError(
                "Non-major email providers are not supported")

        # Validate age based on birthday
        birthday = attrs.get("birthday")
        date_now = localdate(now())
        age = (
            date_now.year
            - birthday.year
            - (
                (date_now.month, date_now.day)
                < (birthday.month, birthday.day)
            )
        )

        if age < 16:
            raise serializers.ValidationError(
                "You need to be at least 16 years old to avail of this USTP service")
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.is_active = False
        user.set_password(validated_data["password"])
        user.save()

        return user
