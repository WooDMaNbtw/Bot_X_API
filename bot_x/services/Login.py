from rest_framework.views import APIView
from core.Route import Route
from services.CustomRoute import CustomRoute


class Login(Route, APIView):

    def get_method(self) -> str:
        return "POST"

    def get_path(self) -> str:
        return "/users/login"
