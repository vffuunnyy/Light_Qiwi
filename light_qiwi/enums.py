# -*- coding: utf-8 -*-
from enum import Enum

from aenum import MultiValueEnum


class OperationType(Enum):
    """
    Тип операций в отчете, для отбора.
    Используется тут:
        https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html?http#payments_list
    """

    # Все операции
    ALL = 'ALL'

    # Только пополнения
    IN = 'IN'

    # Только исходящие переводы
    OUT = 'OUT'

    # Только платежи по картам QIWI (QVC, QVP)
    QIWI_CARD = 'QIWI_CARD'

    UNKNOWN = 'Unknown'


class Currency(MultiValueEnum):
    """
    Валюты
    """

    # Рубли
    RUB = 'RUB', 643

    # Доллары
    USD = 'USD', 840

    # Евро
    EUR = 'EUR', 978

    UNKNOWN = 'Unknown', -1


class PaymentStatus(Enum):
    """
    Статус платежей
    """

    # Платёж проводится
    WAITING = 'WAITING'

    # Успешный платёж
    SUCCESS = 'SUCCESS'

    # Ошибка платежа
    ERROR = 'ERROR'

    UNKNOWN = 'Unknown'


class Provider(Enum):
    """
    Провайдеры

    :param Provider.QIWI: Перевод на QIWI Wallet
    """

    # Перевод по номеру в киви
    QIWI = 99

    # Перевод на карту Visa (карты российских банков)
    RU_VISA = 1963

    # Перевод на карту MasterCard (карты российских банков)
    RU_MASTER_CARD = 21013

    # Для карт, выпущенных банками стран Азербайджан, Армения, Белоруссия,
    # Грузия, Казахстан, Киргизия, Молдавия, Таджикистан, Туркменистан, Украина, Узбекистан
    ANOTHER_VISA = 1960
    ANOTHER_MASTER_CARD = 21012

    # Перевод на карту национальной платежной системы МИР
    MIR = 31652
    
    # Перевод на Яндекс.Деньги
    YANDEX = 26476
    
    # Перевод в киви по нику
    NICKNAME = 99999
    
    # Перевод на Webmoney
    WEBMONEY = 31271

    UNKNOWN = 'Unknown'


class Field(Enum):
    """
    Поля в переводе
    """

    COMMENT = 'comment'

    AMOUNT = 'sum'

    ACCOUNT = 'account'
