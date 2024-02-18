from core.Route import Route
from rest_framework.views import APIView


class BotDetail(Route, APIView):

    def get_method(self) -> str:
        return "GET"

    def get_path(self) -> str:
        return f"/bots/{self._bot_id}"
