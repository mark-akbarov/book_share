from django.conf import settings
import requests


ESKIZ_EMAIL = settings.ESKIZ_EMAIL
ESKIZ_PASSWORD = settings.ESKIZ_PASSWORD
ESKIZ_URL = settings.ESKIZ_URL


def get_token():
    url = ESKIZ_URL + 'auth/login'
    body = {'email': ESKIZ_EMAIL, 'password': ESKIZ_PASSWORD}
    res = requests.post(url, json=body)
    if res.status_code == 200:
        return res.json().get('data').get('token')


def send_sms(phone_number, code):
    url = ESKIZ_URL + "message/sms/send"
    token = get_token()
    body = {'mobile_phone': phone_number, 'message': f"Appointee: {code} - verification code", 'from': 4546}
    headers = {'Authorization': f'Bearer {token}'}
    res = requests.post(url, headers=headers, json=body)
    if res.status_code == 200:
        return 'success'
