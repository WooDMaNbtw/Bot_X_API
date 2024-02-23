from rest_framework.views import APIView
from core.Route import Route

from services.CustomRoute import CustomRoute


class DialogueList(Route, APIView):
    def __init__(self, headers: dict = {}, token=None, need_execute_local=False):
        self.headers: dict = headers
        self.headers["Authorization"] = f"Bearer {token}"
        super().__init__(need_execute_local)

    def get_method(self) -> str:
        return "GET"

    def get_path(self) -> str:
        return f"/dialogues"
