from django.db import models
from core.utils.base_model import BaseModel


class VerifyUser(BaseModel):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='verifications')
    code = models.CharField(max_length=25)
    is_active = models.BooleanField(default=False)
