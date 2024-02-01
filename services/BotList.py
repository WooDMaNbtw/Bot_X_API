from rest_framework.views import APIView
from core.Route import Route

class BotList(Route, APIView):

    def get_method(self) -> str:
        return "GET"

    def get_path(self) -> str:
        return "/bots"

    # def set_url(self, url: str) -> None:
    #     url = "https://opentest.ru"
    #     super().set_url(url)

    # def set_headers(self, headers: dict) -> None:
    #     headers["NEW_CORE_REQUEST_HEADER"] = "CORE_VALUE_REQUEST_HEADER"
    #     super().set_headers(headers)

    # def set_request(self, data: dict) -> None:
    #     data["NEW_CORE_REQUEST_BODY"] = "CORE_VALUE_REQUEST_BODY"
    #     super().set_request(data)

    # def set_response(self, response: dict | None, headers: dict | None, status_code=None, ) -> None:
    #     response["New_body_response_proxy"] = "NEW BODY"
    #     headers["New_header_response_proxy"] = "NEW HEADER"
    #     status_code = 599
    #     super().set_response(response, headers, status_code)
