from rest_framework.views import APIView
from .CustomRoute import CustomRoute


class Login(CustomRoute, APIView):

    def get_method(self) -> str:
        return "POST"

    def get_path(self) -> str:
        return "/users/login"