from unittest.mock import patch
from django.conf import settings


class MockedSMSResponse:
    status_code = 0
    text = None
    json_data = None

    def __init__(self, status_code=201, data=None):
        self.status_code = status_code
        if status_code == 201:
            self.json_data = {
                "statusCode": 201,
                "messageId": 6014905066,
                "cost": "0.0500",
                "currency": "SAR",
                "totalCount": 1,
                "msgLength": 1,
                "accepted": f"[{data.get('recipients')},]",
                "rejected": "[]"
            }
        else:
            self.json_data = {
                "statusCode": status_code,
                "message": "invalid credentials information (mock)"
            }
        self.text = str(self.json_data)

    def json(self):
        return self.json_data


class MockedSMSRequests:

    @classmethod
    def post(cls, url, data=None, **kwargs):
        if url == settings.SMS_BASE_URL:
            if data and data["recipients"].startswith("966"):
                return MockedSMSResponse(data=data)
            if data and data["recipients"].isdigit():
                return MockedSMSResponse(data=data)
            return MockedSMSResponse(401)
