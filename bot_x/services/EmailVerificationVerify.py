from core.Route import Route
from rest_framework.views import APIView


class EmailVerificationVerify(Route, APIView):

    def get_method(self) -> str:
        return "POST"

    def get_path(self) -> str:
        return f"/users/email-verification/verify"
