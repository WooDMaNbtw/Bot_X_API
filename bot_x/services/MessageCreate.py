from rest_framework.views import APIView
from core.Route import Route


class MessageCreate(Route, APIView):

    def get_path(self) -> str:
        return f"/dialogues/{self._dialogue_id}/messages"

    def get_method(self) -> str:

        return 'POST'