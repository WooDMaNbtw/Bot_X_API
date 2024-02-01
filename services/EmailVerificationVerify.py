from core.Route import Route
from rest_framework.views import APIView

from services.CustomRoute import CustomRoute


class EmailVerificationVerify(Route, APIView):
    def __init__(self, data: dict = None, headers: dict = {}, token=None, need_execute_local=False):
        self.data: dict = data
        self.headers: dict = headers
        self.headers["Authorization"] = f"Bearer {token}"
        super().__init__(need_execute_local)

    def get_method(self) -> str:
        return "POST"

    def get_path(self) -> str:
        return f"/users/email-verification/verify"
