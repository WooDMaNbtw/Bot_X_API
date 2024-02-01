from rest_framework.views import APIView
from core.Route import Route
from services.CustomRoute import CustomRoute


class Login(CustomRoute, APIView):
    def __init__(self, data: dict = None, need_execute_local=False):
        self.data: dict = data
        super().__init__(need_execute_local)

    def get_method(self) -> str:
        return "POST"

    def get_path(self) -> str:
        return "/users/login"
