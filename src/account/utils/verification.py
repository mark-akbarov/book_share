from random import randint

from django.core.mail import send_mail
from django.conf import settings

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from account.models import VerifyUser, User


def send_user_verify_code(user: User, is_forgot_password=False):
    """
    This utility function sends an email with verification code
    upon new user registration.
    """
    code = randint(100_000, 999_999)
    if is_forgot_password is False:
        VerifyUser.objects.create(
            user=user,
            code=f'verify_user_{code}',
            is_active=False
        )
    elif is_forgot_password is True:
        VerifyUser.objects.create(
            user=user,
            code=f'forgot_password_{code}',
            is_active=False
        )
    send_mail(
        subject="Verification Code", 
        message=f"Here is your verification code {code}.", 
        from_email=settings.EMAIL_HOST_USER, 
        recipient_list=[user.email,]
        )


def check_verify_signup_code(email, code):
    check = VerifyUser.objects.filter(
        user__email=email,
        code=f'verify_user_{code}',
        is_active=False
    )
    if check.exists():
        verify = check.first()
        verify.is_active = True
        verify.save()
        user = verify.user
        user.is_active = True
        user.save()
        token = RefreshToken.for_user(user=user)
        return Response({"refresh": str(token), "access": str(token.access_token)})
    else:
        return Response({
            "type": "E_INVALID_CODE.", 
            "message": "The code provided is invalid, please check carefully."
            }, 
            status=status.HTTP_400_BAD_REQUEST
            )


def check_verify_forgot_password_code(email, code):
    check = VerifyUser.objects.filter(
        user__email=email,
        code=f'forgot_password_{code}',
        is_active=False
    )
    return check.exists()


def re_send_verify_user_code(email):
    try:
        user = User.objects.get(email=email)
        send_user_verify_code(user)
        return Response({'detail': 'successfully send new code'})
    except User.DoesNotExist:
        return Response({'detail': 'username does not exist'}, status=status.HTTP_400_BAD_REQUEST)
