from rest_framework.exceptions import APIException, _get_error_details
from rest_framework import status


class ServiceUnavailable(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Service is unavailable, try again in a few minuts'
    default_code = 'service unavailable'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)
