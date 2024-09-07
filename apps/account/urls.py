from django.urls import path, include

from rest_framework.routers import DefaultRouter

from apps.account.views.otp import OTPSignupView, OTPVerificationAPIView
from apps.account.views.passport import PassportVerificationViewSet 
from apps.account.views.login import LoginAPIView
from apps.account.views.signup import SignupAPIView
from apps.account.views.verification import VerifyUserAPIView, ReSendVerifyUserAPIView


router = DefaultRouter()
router.register('passport', PassportVerificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    path('otp/', OTPSignupView.as_view(), name='otp_signup'),
    path('otp/verification/', OTPVerificationAPIView.as_view(), name='otp_verification'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyUserAPIView.as_view(), name='verify-user'),
    path('verify/resend/', ReSendVerifyUserAPIView.as_view(), name='resend-verify-user'),
    
    
]
