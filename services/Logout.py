from core.Route import Route
from rest_framework.views import APIView
from services.CustomRoute import CustomRoute


class Logout(CustomRoute, APIView):

    def get_method(self) -> str:
        return "POST"

    def get_path(self) -> str:
        return f"/users/logout"
