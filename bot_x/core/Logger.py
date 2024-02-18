from datetime import datetime
from django.conf import settings
from .models import Log
from typing import Union


class Logger:
    NEED_LOGGER: bool = settings.NEED_LOGGER

    def __init__(self, options: dict = {}):
        self.__log_entry = Log()
        self.set_proxy_method(method=options.get("proxy_method"))
        self.set_core_method(method=options.get('core_method'))
        self.set_proxy_url(url=options.get('proxy_url'))
        self.set_core_url(url=options.get('core_url'))
        self.set_proxy_request_headers(headers=options.get('proxy_request_headers'))
        self.set_core_request_headers(headers=options.get('core_request_headers'))
        self.set_proxy_request_body(body=options.get('proxy_request_body'))
        self.set_core_request_body(body=options.get('core_request_body'))
        self.set_proxy_response_headers(headers=options.get('proxy_response_headers'))
        self.set_core_response_headers(headers=options.get('core_response_headers'))
        self.set_proxy_response_body(body=options.get('proxy_response_body'))
        self.set_core_response_body(body=options.get('core_response_body'))
        self.set_proxy_response_status_code(status_code=options.get('proxy_response_status_code'))
        self.set_core_response_status_code(status_code=options.get('core_response_status_code'))

    def _set(self, key: str, value: Union[str, dict, int]) -> None:
        if key is not None and value is not None:
            setattr(self.__log_entry, key, value)

    def set_proxy_method(self, method: str) -> None:
        self._set("proxy_method", method)

    def set_core_method(self, method: str) -> None:
        self._set("core_method", method)

    def set_proxy_url(self, url: str) -> None:
        self._set("proxy_url", url)

    def set_core_url(self, url: str) -> None:
        self._set("core_url", url)

    def set_proxy_request_headers(self, headers: dict) -> None:
        self._set("proxy_request_headers", headers)

    def set_core_request_headers(self, headers: dict) -> None:
        self._set("core_request_headers", headers)

    def set_proxy_request_body(self, body: dict) -> None:
        if type(body) == str:
            body = {
                "content": body
            }
        self._set("proxy_request_body", body)

    def set_core_request_body(self, body: dict) -> None:
        if type(body) == str:
            body = {
                "content": body
            }
        self._set("core_request_body", body)

    def set_proxy_response_headers(self, headers: dict) -> None:
        self._set("proxy_response_headers", headers)

    def set_core_response_headers(self, headers: dict) -> None:
        self._set("core_response_headers", headers)

    def set_proxy_response_body(self, body: dict) -> None:
        if type(body) == str:
            body = {
                "content": body
            }
        self._set("proxy_response_body", body)

    def set_core_response_body(self, body: dict) -> None:
        if type(body) == str:
            body = {
                "content": body
            }
        self._set("core_response_body", body)

    def set_proxy_response_status_code(self, status_code: int) -> None:
        self._set("proxy_response_status_code", status_code)

    def set_core_response_status_code(self, status_code: int) -> None:
        self._set("core_response_status_code", status_code)

    def write(self) -> None:
        if self.NEED_LOGGER:
            self.__log_entry.created_at = datetime.now().isoformat()
            self.__log_entry.save()
        self.clear_fields()

    def clear_fields(self) -> None:
        for field in self.__log_entry._meta.fields:
            setattr(self.__log_entry, field.attname, None)