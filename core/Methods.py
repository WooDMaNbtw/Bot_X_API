from django.http import HttpResponse
from rest_framework.response import Response
from .settings import APP_ID


class Methods:

    def request_setter(self, request, *args, **kwargs):
        self.set_method(self.get_method())
        if self.get_method() == "GET" and request.query_params:
            query_params = '?' + '&'.join([f"{key}={value}" for key, value in request.query_params.items()])
            self.set_url(f'{self._THIRD_PARTY_APP_URL}{APP_ID}{self.get_path()}{query_params}')
        else:
            self.set_url(f'{self._THIRD_PARTY_APP_URL}{APP_ID}{self.get_path()}')

        self.set_headers(dict(request.headers))
        self.set_request(request.data)

    def get(self, request, *args, **kwargs):
        self.request_setter(request, *args, **kwargs)
        response, headers, status_code = self.send()
        if type(response) == str:
            return HttpResponse(status=status_code, content=response, headers=headers)
        return Response(status=status_code, data=response, headers=headers)

    def post(self, request, *args, **kwargs):
        self.request_setter(request, *args, **kwargs)
        response, headers, status_code = self.send()
        return Response(status=status_code, data=response, headers=headers)

    def put(self, request, *args, **kwargs):
        self.request_setter(request, *args, **kwargs)
        response, headers, status_code = self.send()
        return Response(status=status_code, data=response, headers=headers)

    def patch(self, request, *args, **kwargs):
        self.request_setter(request, *args, **kwargs)
        response, headers, status_code = self.send()
        return Response(status=status_code, data=response, headers=headers)

    def delete(self, request, *args, **kwargs):
        self.request_setter(request, *args, **kwargs)
        response, headers, status_code = self.send()
        return Response(status=status_code, data=response, headers=headers)

    def options(self, request, *args, **kwargs):
        self.request_setter(request, *args, **kwargs)
        headers: dict | None = {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        }
        return Response(status=200, data=None, headers=headers)
