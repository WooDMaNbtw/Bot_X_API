# BOT_X

## Для начала
Для начала вам нужно склонировать проект в вашу локальную директорию - <code>git clone -b deployment</code>.

## Использование
Дальше, для того чтобы запустить проект, <b> должен быть установлен Docker </b>. 

<b><u>В даннй момент для запуска контейнера требуется ОС Linux</u></b>

<i>Сборка и запуск контейнера</i>

    docker-compose up -d

<b>При ошибке запуска контейнера используйте данную команду без дефиса "-"</b>

    docker compose up -d

<i>Остановка всех сервисов контейнера</i>

    docker compose down


В данном проекте используются 3 основных файла для запуска контейнера docker: <code>docker-compose.yml</code>, <code>Dockerfile</code> и <code>scripts/entrypoint.sh</code>.


### Пример переопределения методов в классах (services/..class)

    # core_request_headers - http-заголовки, проксируемые из клиента проксёй на ядро
    def set_headers(self, headers: dict) -> None:
        headers["NEW_COR_REQUEST_HEADERS"] = "CORE_VALUE_REQUEST_HEADERS"
        super().set_headers(headers)

    # proxy_response_headers - http-заголовки, проксируемые клиенту проксёй из ядра
        # ПОКА ЧТО НЕТУ В ROUTE LINE 127 self._logger.set_proxy_response_headers(response.headers)

    # core_request_body - JSON-запроса, проксируемый из клиента проксёй на ядро.

    def set_parameters(self, data: dict) -> None:
       data["NEW_COR_REQUEST_BODY"] = "CORE_VALUE_REQUEST_BODY" 
       super().set_parameters(data)
    
    # proxy_response_body - JSON-ответа, проксируемый клиенту проксёй из ядра

    def set_response(self, response: dict | None, status=None) -> None:
        for element in response["result"]:
            element["NEW_PROXY_RESPONSE_BODY"] = "PROXY_VALUE_RESPONSE_BODY"
        super().set_response(response, status)


### Пример переопределения set_response в CustomRoute (services/CustomRoute)

    class CustomRoute(Route):

    def set_response(self, response: dict | None, status=None) -> None:
        if response:
            if 'result' in response:
                super().set_response(response['result'], status)
                response = super().get_response()
                for item in response:
                    item["NEW_BOT"] = "GPT BOT NEW"
            if 'error' in response:
                super().set_response(response['error'], status)
                response = super().get_response()
        response[1]["NEW_BOT_UPDATE"] = "GPT BOT UPDATE"
        super().set_response(response, status)
