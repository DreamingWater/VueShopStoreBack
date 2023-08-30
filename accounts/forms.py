from rest_framework import serializers


class SignUpForm(serializers.Serializer):
    email = serializers.EmailField(max_length=50, allow_null=False)
    password = serializers.CharField(max_length=255, allow_null=False)
    email_code = serializers.CharField(max_length=10, allow_null=False)


class LoginForm(serializers.Serializer):
    email = serializers.EmailField(max_length=50, allow_null=False)
    password = serializers.CharField(max_length=255, allow_null=False)
    img_code = serializers.CharField(max_length=10, allow_null=False)
