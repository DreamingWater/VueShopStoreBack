from rest_framework import serializers
from accounts.models import Token, User as CustomUser, UserBaseModel, VerifyToken


class BaseUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserBaseModel
        fields = "__all__"


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =  ['email','password','id']


class TokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"

class VerifyTokenSerializers(serializers.ModelSerializer):
    class Meta:
        model = VerifyToken
        fields = "__all__"

