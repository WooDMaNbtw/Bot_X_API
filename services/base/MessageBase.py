from core.Route import Route
from rest_framework.views import APIView


class MessageBase(Route, APIView):

    def get_path(self) -> str:
        return f"/dialogues/{self._dialogue_id}/messages"

    def get_method(self) -> str:
        if self.request.method == 'GET':
            from ..MessageList import MessageList
            self.__class__ = MessageList
        #
        elif self.request.method == 'POST':
            from ..MessageCreate import MessageCreate
            self.__class__ = MessageCreate

        try:
            return self.get_method()
        except Exception as e:
            return self.request.method.upper()
