from rest_framework import serializers


class OTPSignupSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class OTPActivateAccountSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()
