from unittest.mock import patch


def mocked_send_sms_message(text, *args, **kwargs):
    print("mocked")
