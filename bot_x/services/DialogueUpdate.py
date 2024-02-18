from core.Route import Route
from rest_framework.views import APIView


class DialogueUpdate(Route, APIView):

    def get_method(self) -> str:
        return "PUT"

    def get_path(self) -> str:
        return f"/dialogues/{self._dialogue_id}"
