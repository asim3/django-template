from django.conf import settings
import string
import random
import requests


class SMS_Error(Exception):
    pass


def generate_random_key(characters=None, length=100):
    """
    Generate random string with given characters and length.
    """
    if characters is None:
        characters = string.digits + string.ascii_letters
    return ''.join(random.choices(characters, k=length))


def generate_random_name(characters=None, length=10):
    if characters is None:
        characters = string.ascii_lowercase
    return generate_random_key(characters, length)


def generate_OTP_key(characters=string.digits, length=settings.OTP_MAX_LENGTH):
    return generate_random_key(characters, length)


def clean_arabic_digits(data):
    arabic_numbers = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩']
    new_data = ""
    for x in data:
        if x in arabic_numbers:
            new_data += str(arabic_numbers.index(x))
        else:
            new_data += str(x)
    return new_data


def clean_phone_number(phone):
    phone = clean_arabic_digits(phone)
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("00"):
        phone = phone[2:]
    if phone.startswith("05"):
        phone = "966" + phone[1:]
    if phone.startswith("5") and len(phone) == 9:
        phone = "966" + phone[-9:]
    return phone


def send_sms_message(phone, text, raise_exception=False):
    data = {
        "bearerTokens": settings.SMS_TOKEN,
        "sender": settings.SMS_DEFAULT_FROM,
        "recipients": str(phone),
        "body": str(text),
    }
    response = requests.post(settings.SMS_BASE_URL, data=data)
    if response.status_code == 200:
        accepted = response.json().get("accepted")
        if accepted[1:-2] == phone:
            return True
    if raise_exception:
        raise SMS_Error("Error while sending SMS. "
                        f"status code: [{response.status_code}] "
                        f"response: {response.text}")
    return False
