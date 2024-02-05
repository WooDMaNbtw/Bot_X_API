from rest_framework.views import APIView
from botX.core.Route import Route


class Register(Route, APIView):

    def get_method(self) -> str:
        return "POST"

    def get_path(self) -> str:
        return "/users"
