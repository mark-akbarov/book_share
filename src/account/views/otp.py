from rest_framework.views import APIView
from rest_framework import permissions

from account.serializers.otp import OTPSignupSerializer, OTPActivateAccountSerializer
from account.utils.otp import otp_signup, otp_verification


class OTPSignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return otp_signup(**serializer.validated_data)


class OTPVerificationAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPActivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return otp_verification(**serializer.validated_data)
