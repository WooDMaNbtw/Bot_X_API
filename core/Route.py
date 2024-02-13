import inspect
from typing import Any
from django.core.cache import cache
from core.settings import CACHE_DEFAULT_TTL
from django.core.management.commands.runserver import Command
import requests
from requests import JSONDecodeError
from .Logger import Logger
from .settings import APP_ID, THIRD_PARTY_APP_URL, LOCALHOST, BASE_URI
from .Methods import Methods


class Route(Methods):
    def __init__(self, need_execute_local=False, use_cache=False, *args, **kwargs):
        self._APP_ID = APP_ID
        self._THIRD_PARTY_APP_URL = THIRD_PARTY_APP_URL
        self._method: str | None = None
        self._request: dict | None = None
        self._response: dict | None = None
        self._headers: dict | None = None
        self.__request_headers: dict | None = None
        self._url: str | None = None
        self._status_code: int | None = None
        self._not_allowed_headers = ('Connection', 'Keep-Alive', "Content-Length", "Transfer-Encoding", "Content-Encoding")

        self._use_cache: bool = use_cache
        self._logger = Logger()
        if need_execute_local:
            request = requests.Request(
                method=self.get_method(),
                url=f"{self._THIRD_PARTY_APP_URL}{self._APP_ID}{self.get_path()}",
            )
            other_params: list = ["data", "query_params", "json", "headers"]
            for param in other_params:
                if param in inspect.signature(self.__init__).parameters:
                    setattr(request, param, getattr(self, param))
                else:
                    setattr(request, param, {})

            getattr(self, self.get_method().lower())(request)

    def request_setter(self, request, *args, **kwargs):
        self._dialogue_id = kwargs.get("dialogue_id")
        self._bot_id = kwargs.get("bot_id")
        self.__request_headers = dict(request.headers)
        self.__request_headers["Content-Type"] = "application/json"
        request.headers = self.__request_headers
        self._logger.set_proxy_method(request.method)
        try:
            self._logger.set_proxy_url(request.build_absolute_uri())
        except Exception as ex:
            self._logger.set_proxy_url(f"{LOCALHOST}{BASE_URI}{self.get_path()}")
        self._logger.set_proxy_request_headers(dict(request.headers))
        if self.get_method() == "GET":
            self._logger.set_proxy_request_body(dict(request.query_params))
        else:
            self._logger.set_proxy_request_body(request.data)
        super().request_setter(request)

    def response_core_setter(self, response, headers, status_code):
        self._logger.set_core_response_headers(headers)
        self._logger.set_core_response_body(response)
        self._logger.set_core_response_status_code(status_code)

    def response_proxy_setter(self, response, headers, status_code):
        self._logger.set_proxy_response_body(response)
        self._logger.set_proxy_response_headers(headers)
        self._logger.set_proxy_response_status_code(status_code)

    def set_method(self, method: str) -> None:
        self._method = method
        self._logger.set_core_method(method)

    def get_method(self) -> str:
        return self._method

    def set_url(self, url: str) -> None:
        self._url = url
        self._logger.set_core_url(url)

    def get_url(self) -> str:
        return self._url

    def set_headers(self, headers: dict) -> None:
        if "Host" in headers.keys():
            headers.pop("Host")
        self._headers = headers
        self._logger.set_core_request_headers(headers)

    def get_headers(self) -> dict:
        return self._headers

    def set_request(self, data: dict) -> None:
        self._request = data
        self._logger.set_core_request_body(data)

    def get_request(self) -> dict:
        return self._request

    def set_response(self, response: dict | None, headers: dict | None, status_code=None, ) -> None:
        if response is not None and status_code is not None:
            if 200 <= status_code < 300:
                response = self.on_success(response)
            if 400 <= status_code <= 500:
                response = self.on_error(response)

        self._response = response
        self._headers = headers
        self._status_code = status_code
        self.response_proxy_setter(response, headers, status_code)

    def get_response(self) -> dict | None:
        return self._response

    def on_success(self, response: dict) -> dict:
        return response

    def on_error(self, response: dict) -> dict:
        return response

    def send(self) -> tuple:
        response = cache.get(key=f"core_{self.__class__.__name__}_response") if self._use_cache else None
        if not response:
            response = requests.request(
                method=self.get_method(),
                url=self.get_url(),
                json=self.get_request(),
                headers=self.get_headers()
            )
            if self._use_cache:
                cache.set(key=f"core_{self.__class__.__name__}_response", value=response, timeout=CACHE_DEFAULT_TTL)
        try:
            response_body = response.json()
        except JSONDecodeError as ex:
            response_body = response.text if response.text else None
        finally:
            response_headers = dict(response.headers)
            response_status_code = response.status_code

        self.response_core_setter(response_body, response_headers, response_status_code)

        #  filtered headers
        response_headers = {k: v for k, v in response_headers.items() if k not in self._not_allowed_headers}
        response_headers.update({
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': '*'
        })

        self.set_response(response_body, response_headers, response_status_code)

        self._logger.write()

        return self.get_response(), self.get_headers(), self._status_code


