from rest_framework.viewsets import ModelViewSet

from account.serializers.passport import PassportVerificationSerializer
from account.models.passport import PassportVerification


class PassportVerificationViewSet(ModelViewSet):
    queryset = PassportVerification.objects.all()
    serializer_class = PassportVerificationSerializer
    
    def perform_create(self, serializer):
        self.request.user.is_passport_verified = True
        self.request.user.save()
        serializer.save() 
