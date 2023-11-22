from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from account.serializers.verification import UserVerifySerializer, ReSendVerifyUserSerializer
from account.utils.verification import check_verify_signup_code, re_send_verify_user_code


class VerifyUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return check_verify_signup_code(**serializer.validated_data)


class ReSendVerifyUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ReSendVerifyUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return re_send_verify_user_code(**serializer.validated_data)
