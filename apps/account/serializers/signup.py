from rest_framework import serializers


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    telegram_username = serializers.CharField()
