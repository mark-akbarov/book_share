import random, datetime

from django.db.models.functions import Now

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from account.models.account import User
from account.models.otp import OTPVerification


def otp_signup(phone_number: str):
    expiration_time = datetime.timedelta(minutes=10)
    not_expired = OTPVerification.objects.filter(created_at__gte=Now()-expiration_time, phone_number=phone_number)
    if not_expired:
        return Response(
            {
                "type": "E_MULTIPLE_REQUESTS", 
                "message": "Too many requests have been made. Please try again after some time."
                }, 
            status=status.HTTP_400_BAD_REQUEST
            )
    else:
        otp_code_generate(phone_number)
        verification = OTPVerification.objects.filter(phone_number=phone_number).order_by('-created_at').first()
        return Response(
            {
                "message": "Code has been sent", 
                "code": verification.code
                }, 
            status=status.HTTP_200_OK
            )


def otp_code_generate(phone_number: str):
    code = random.randint(100_000, 999_999)
    OTPVerification.objects.create(
        phone_number=phone_number,
        code=code,
        is_expired=False
    )


def otp_verification(phone_number: str, code: str):
    check = OTPVerification.objects.filter(
        phone_number=phone_number,
        code=code,
        is_expired=False
    )
    if check:
        expiration_time = datetime.timedelta(minutes=10)
        if OTPVerification.objects.filter(phone_number=phone_number, code=code, created_at__lte=Now()-expiration_time):
            verification = check.first()
            verification.is_expired = True
            return Response(
                {
                    "type": "E_EXPIRED_VERIFICATION_CODE", 
                    "message": "Verification code has expired."
                    }, 
                status=status.HTTP_400_BAD_REQUEST
                )
        existing_user = User.objects.filter(phone_number=phone_number).first()
        if existing_user:
            token, _ = Token.objects.get_or_create(user=existing_user)
            return Response({"token": token.key, "new_user": False}, status=status.HTTP_200_OK)
        else:
            user = create_user_via_otp(phone_number=phone_number)
            verification = check.first()
            verification.is_expired = True
            verification.save()
            user.is_active = True
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "new_user": True}, status=status.HTTP_201_CREATED)
    else:
        return Response({"type": "E_INVALID_VERIFICATION_CODE", "message": "Invalid verification code, please try again."}, status=status.HTTP_400_BAD_REQUEST)


def create_user_via_otp(phone_number: str):
    user = User.objects.create( 
        phone_number=phone_number,
        is_active=False,
        is_staff=False,
        is_superuser=False,
    )
    user.save()
    return user
