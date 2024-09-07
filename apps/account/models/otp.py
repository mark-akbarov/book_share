from django.db import models

from core.utils.base_model import BaseModel


class OTPVerification(BaseModel):
    phone_number = models.CharField(max_length=25)
    code = models.CharField(max_length=25)
    is_expired = models.BooleanField(default=False)
   
    def __str__(self) -> str:
        return self.phone_number