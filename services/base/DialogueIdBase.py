from core.Route import Route
from rest_framework.views import APIView


class DialogueIdBase(Route, APIView):

    def get_method(self) -> str:
        if self.request.method == 'GET':
            from ..DialogueDetail import DialogueDetail
            self.__class__ = DialogueDetail

        elif self.request.method == 'PUT':
            from ..DialogueUpdate import DialogueUpdate
            self.__class__ = DialogueUpdate

        elif self.request.method == 'PATCH':
            from ..DialogueOptionalUpdate import DialogueOptionalUpdate
            self.__class__ = DialogueOptionalUpdate

        elif self.request.method == 'DELETE':
            from ..DialogueDelete import DialogueDelete
            self.__class__ = DialogueDelete

        try:
            return self.get_method()
        except Exception as e:
            return self.request.method.upper()

    def get_path(self) -> str:
        return f"/dialogues/{self._dialogue_id}"
