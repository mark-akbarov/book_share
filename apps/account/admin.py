from django.contrib import admin

from apps.account.models.account import User
from apps.account.models.otp import OTPVerification


admin.site.register(User)
admin.site.register(OTPVerification)