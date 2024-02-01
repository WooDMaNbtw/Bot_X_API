from core.Route import Route


class CustomRoute(Route):
    def set_response(self, response: dict | None, headers: dict | None, status_code=None, ) -> None:
        if response:
            if 'result' in response:
                super().set_response(response['result'], headers, status_code)
                response = super().get_response()
            if 'error' in response:
                super().set_response(response['error'], headers, status_code)
                response = super().get_response()
        super().set_response(response, headers, status_code)
