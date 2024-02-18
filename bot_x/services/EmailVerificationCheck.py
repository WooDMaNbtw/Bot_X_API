from core.Route import Route
from rest_framework.views import APIView


class EmailVerificationCheck(Route, APIView):

    def get_method(self) -> str:
        return "GET"

    def get_path(self) -> str:
        return f"/users/email-verification/check"
