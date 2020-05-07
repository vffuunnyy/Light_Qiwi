# -*- coding: utf-8 -*-


class RequestError:

    def __init__(self, error_code):
        """
        Args:
            error_code:
        """
        if error_code == 400:
            raise RequestSyntaxError("Ошибка синтаксиса запроса (неправильный формат данных)")
        elif error_code == 401:
            raise InvalidTokenError("Неверный токен или истек срок действия токена")
        elif error_code == 403:
            raise RequestPermissionError(
                "Нет прав на данный запрос (недостаточно разрешений у токена)"
            )
        elif error_code == 404:
            raise APIError(
                "Список ошибок:https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html?http#errors"
            )
        elif error_code == 422:
            raise ArgumentError("Неправильно указаны домен/подсеть/хост веб-хука(в параметре URL), "
                                "неправильно указаны тип хука или тип транзакции, "
                                "попытка создать хук при наличии уже созданного")
        elif error_code == 423:
            raise TooManyRequests("Слишком много запросов, сервис временно недоступен")
        elif error_code == 500:
            raise APIError("Внутренняя ошибка сервиса (превышена длина URL)")


class APIError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class ArgumentError(Exception):
    pass


class RequestSyntaxError(Exception):
    pass


class RequestPermissionError(Exception):
    pass


class TooManyRequests(Exception):
    pass
