# BOT_X

## Пример переопределения методов в классах (services/..class)

#### core_method - http-метод запроса, проксируемый из клиента проксёй на ядро.
    def get_method(self) -> str:
        return "GET"
    
#### core_url - полный путь сгенерированного core-URL проксёй на ядро.
    def set_url(self, url: str) -> None:
        url = "https://opentest.ru"
        super().set_url(url)

#### core_request_headers - http-заголовки, проксируемые из клиента проксёй на ядро.
    def set_headers(self, headers: dict) -> None:
        headers["NEW_CORE_REQUEST_HEADER"] = "CORE_VALUE_REQUEST_HEADER"
        super().set_headers(headers)

#### core_request_body - JSON-запроса, проксируемый из клиента проксёй на ядро. Если в проксе изменяется проксируемый
    def set_request(self, data: dict) -> None:
        data["NEW_CORE_REQUEST_BODY"] = "CORE_VALUE_REQUEST_BODY"
        super().set_request(data)

#### proxy_response_headers - http-заголовки, проксируемые клиенту проксёй из ядра.
#### proxy_response_body - JSON-ответа, проксируемый клиенту проксёй из ядра.
#### proxy_response_status_code - http-статусный код, проксируемый клиенту проксёй из ядра.

    def set_response(self, response: dict | None, headers: dict | None, status_code=None, ) -> None:
        for el in response['result']:
            el["newEveryBody"] = "EveryBody"
        response["New_body_response_proxy"] = "NEW BODY"
        headers["New_header_response_proxy"] = "NEW HEADER"
        status_code = 599
        super().set_response(response, headers, status_code)


## Пример переопределения set_response в CustomRoute (services/CustomRoute)

    class CustomRoute(Route):

    def set_response(self, response: dict | None, headers: dict | None, status_code=None, ) -> None:
        if response:
            if 'result' in response:
                super().set_response(response['result'], headers, status_code)
                response = super().get_response()
                for item in response:
                    item["NEW_BOT"] = "GPT BOT NEW"
            if 'error' in response:
                super().set_response(response['error'], headers, status_code)
                response = super().get_response()
        response[1]["NEW_BOT_UPDATE"] = "GPT BOT UPDATE"
        super().set_response(response, headers, status_code)
