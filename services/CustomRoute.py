from core.Route import Route


class CustomRoute(Route):
    def set_response(self, response: dict | None, headers: dict | None, status_code=None, ) -> None:
        if response:
            if 'result' in response:
                super().set_response(response['result'], status_code)
                response['result'] = super().get_response()
            if 'error' in response:
                super().set_response(response['error'], status_code)
                response['error'] = super().get_response()
        super().set_response(response, headers, status_code)
