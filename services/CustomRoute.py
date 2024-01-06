from core.Route import Route


class CustomRoute(Route):
    def set_response(self, response: dict | None, status=None) -> None:
        if response:
            if 'result' in response:
                super().set_response(response['result'], status)
                response = super().get_response()
            if 'error' in response:
                super().set_response(response['error'], status)
                response = super().get_response()
        super().set_response(response, status)
