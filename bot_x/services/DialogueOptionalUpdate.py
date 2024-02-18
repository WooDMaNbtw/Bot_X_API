from core.Route import Route
from rest_framework.views import APIView


class DialogueOptionalUpdate(Route, APIView):

    def get_method(self) -> str:
        return "PATCH"

    def get_path(self) -> str:
        return f"/dialogues/{self._dialogue_id}"
