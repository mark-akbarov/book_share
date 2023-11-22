from django.contrib import admin
from account.models.account import User
from account.models.otp import OTPVerification


admin.site.register(User)
admin.site.register(OTPVerification)