from rest_framework.views import APIView
from core.Route import Route
from services.CustomRoute import CustomRoute


class BotList(CustomRoute, APIView):

    def get_method(self) -> str:
        return "GET"

    def get_path(self) -> str:
        return "/bots"


