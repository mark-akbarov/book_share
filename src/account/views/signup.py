from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from account.serializers.signup import SignupSerializer
from account.utils.signup import signup


class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return signup(**serializer.validated_data)
