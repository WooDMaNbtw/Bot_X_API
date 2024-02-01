from rest_framework.views import APIView
from core.Route import Route
from services.CustomRoute import CustomRoute


class BotList(Route, APIView):

    def get_method(self) -> str:
        return "GET"

    def get_path(self) -> str:
        return "/bots"

    def set_response(self, response: dict | None, headers: dict | None, status_code=None) -> None:
        if response and "result" in response:
            filtered_result = []
            for bot in response["result"]:
                if bot.get("status_code") == "active":
                    filtered_bot = {}
                    for key, value in bot.items():
                        if key == "id":
                            filtered_bot[key] = value
                        elif key == "author":
                            filtered_bot[key] = value
                        elif key == "name":
                            filtered_bot.update(self.__parse_name_field(value))
                    filtered_result.append(filtered_bot)
            response = filtered_result
        elif response and "error" in response:
            response = response["error"]

        super().set_response(response, headers, status_code)

    @staticmethod
    def __parse_name_field(name_field: str) -> dict:
        split_values = name_field.split('-')

        fields_to_add = {
            "model_name": f'{split_values[0]}-{split_values[1]}'.title()
        }

        mode_value = name_field.lower()
        if mode_value == 'gpt-3.5-turbo':
            fields_to_add['model_name'] = f'{fields_to_add["model_name"]} 4K'
        elif mode_value == 'gpt-4':
            fields_to_add['model_name'] = f'{fields_to_add["model_name"]} 8K'
        else:
            fields_to_add['model_name'] = f'{fields_to_add["model_name"]} {split_values[-1].title()}'

        return fields_to_add
