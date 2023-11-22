from rest_framework import status
from rest_framework.response import Response

from account.models.account import User
from account.utils.verification import send_user_verify_code


def signup(
    username: str, 
    email: str,
    first_name: str, 
    last_name: str, 
    phone_number: str,
    password
    ):
    """
    Signup checks for email existence and sends a verification email 
    for the new user with given email.
    """
    check_username = User.objects.filter(username=username, is_active=True).exists()
    if check_username:
        return Response(
            {
                'type': 'E_USERNAME_EXISTS', 
                'message': 'Username already exists.'
             }, 
            status=status.HTTP_400_BAD_REQUEST
            )
    user = create_user(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        password=password
    )
    send_user_verify_code(user)
    return Response({'message': 'Successfully registered.'}, status=status.HTTP_201_CREATED)


def create_user(
    username: str, 
    email: str,
    first_name: str, 
    last_name: str,  
    phone_number: str, 
    password=None
    ):
    user = User.objects.create(
        username=username,
        email=email,
        first_name=first_name, 
        last_name=last_name,
        phone_number=phone_number,
        is_active=False,
        is_staff=False,
        is_superuser=False,
    )
    if password:
        user.set_password(password)
        user.save()
    return user
