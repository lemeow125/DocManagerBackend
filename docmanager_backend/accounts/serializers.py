from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework.settings import api_settings


class CustomUserSerializer(serializers.ModelSerializer):
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
        ]
        read_only_fields = ["id", "username", "email", "full_name", "role"]


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, style={"input_type": "password", "placeholder": "Password"}
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "first_name", "last_name"]

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
        if self.Meta.model.objects.filter(username=attrs.get("username")).exists():
            raise serializers.ValidationError(
                "A user with that username already exists."
            )
        return super().validate(attrs)

    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.is_active = False
        user.set_password(validated_data["password"])
        user.save()

        return user
