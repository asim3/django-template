from django.conf import settings

import string
import random


def generate_random_key(characters=None, length=100):
    """
    Generate random string with given characters and length.
    """
    if characters is None:
        characters = string.digits + string.ascii_letters
    return ''.join(random.choices(characters, k=length))


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


def send_sms_message(text):
    # print(text)
    pass
