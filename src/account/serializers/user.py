from rest_framework import serializers

from account.models.account import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'profile_picture',
            ]
