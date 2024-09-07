from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.account.utils.login import login
from apps.account.serializers.login import LoginSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return login(**serializer.validated_data)