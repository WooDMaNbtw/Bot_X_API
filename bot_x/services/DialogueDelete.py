from core.Route import Route
from rest_framework.views import APIView


class DialogueDelete(Route, APIView):

    def get_method(self) -> str:
        return "DELETE"

    def get_path(self) -> str:
        return f"/dialogues/{self._dialogue_id}"
