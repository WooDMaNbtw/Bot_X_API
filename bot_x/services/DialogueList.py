from rest_framework.views import APIView
from core.Route import Route


class DialogueList(Route, APIView):

    def get_method(self) -> str:
        return "GET"

    def get_path(self) -> str:
        return f"/dialogues"
