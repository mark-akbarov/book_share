from rest_framework import serializers


class UserVerifySerializer(serializers.Serializer):
    email = serializers.CharField()
    code = serializers.CharField()


class ReSendVerifyUserSerializer(serializers.Serializer):
    email = serializers.CharField()
