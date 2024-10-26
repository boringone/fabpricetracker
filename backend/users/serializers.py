from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.settings import api_settings
from django.utils.translation import gettext_lazy as _

from users.models import CustomUserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ['email', 'password']

    def validate(self, attrs):
        user = CustomUserModel(**attrs)
        # try:
        #     validate_password(attrs.get("password"), user)
        # except ValidationError as e:
        #     serializer_error = serializers.as_serializer_error(e)
        #     raise serializers.ValidationError(
        #         {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
        #     )
        try:
            validate_email(attrs.get("email"))
        except ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"email": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user = CustomUserModel.objects.create_user(**validated_data)
        return user

