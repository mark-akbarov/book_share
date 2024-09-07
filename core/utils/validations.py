import re


def validate_phone_number(phone_number):
    phone_regex = r'\d{9}'
    return bool(re.match(phone_regex, phone_number))