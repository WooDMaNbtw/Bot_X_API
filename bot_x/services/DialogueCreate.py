from rest_framework.views import APIView
from core.Route import Route


class DialogueCreate(Route, APIView):

    def get_method(self) -> str:
        return "POST"

    def get_path(self) -> str:
        return f"/dialogues/"
