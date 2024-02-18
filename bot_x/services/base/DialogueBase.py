from core.Route import Route
from rest_framework.views import APIView


class DialogueBase(Route, APIView):

    def get_method(self) -> str:
        if self.request.method == 'GET':
            from ..DialogueList import DialogueList
            self.__class__ = DialogueList

        elif self.request.method == 'POST':
            from ..DialogueCreate import DialogueCreate
            self.__class__ = DialogueCreate

        try:
            return self.get_method()
        except Exception as e:
            return self.request.method.upper()

    def get_path(self) -> str:
        return f"/dialogues"
