from typing import Any
from urllib.request import Request

from rest_framework.response import Response
from rest_framework.views import APIView

from common.Route import Route


class DialoguesView(APIView):
    """View for dialogues CRUD operations"""

    def get(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        """
        offset -- A first parameter
        limit -- A second parameter
        """
        dialogue_id = kwargs.get('dialogue_id')
        endpoint = f'dialogues/{dialogue_id}' if dialogue_id else 'dialogues'
        response = Route(request=request).send(endpoint=endpoint)
        return Response(data=response.json(), status=response.status_code, headers=response.headers)

    def post(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.__handle_request(request=request, kwargs=kwargs)

    def put(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.__handle_request(request=request, kwargs=kwargs)

    def patch(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.__handle_request(request=request, kwargs=kwargs)

    def delete(self, request: Request, *args: Any, **kwargs: dict) -> Response:
        return self.__handle_request(request=request, kwargs=kwargs)

    def __handle_request(self, request, **kwargs):
        dialogue_id = kwargs.get('dialogue_id')
        endpoint = f'dialogues/{dialogue_id}' if dialogue_id else 'dialogues'
        response = Route(request=request).send(endpoint=endpoint)
        return Response(data=response.json(), status=response.status_code, headers=response.headers)
