# -*- coding: utf-8 -*-
from _thread import start_new_thread
from time import time, sleep

from requests import Session

from Light_Qiwi.Callback import LightQiwiCallback
from Light_Qiwi.Enums import Currency, Provider, OperationType
from Light_Qiwi.Errors import APIError, RequestError, ArgumentError
from Light_Qiwi.Objects import Balance, Payment


class Qiwi:

    def __init__(self, token, phone):
        """
        :param token (str):
        :param phone (str):
        """

        self._s = Session()

        self._s.headers['Accept'] = 'application/json'
        self._s.headers['Content-Type'] = 'application/json'
        self._s.headers['Authorization'] = 'Bearer ' + token

        self._host = 'https://edge.qiwi.com/'

        self.phone = phone.replace('+', '')

        self.func = None

    @property
    def balance(self):
        return self.get_balance()[0].balance

    @property
    def _transaction_id(self):
        """
        :return: UNIX time *
        1000
        """

        return str(int(time() * 1000))

    def pay(self, account: str, amount: float = 1.0, comment: str = "",
            currency: Currency = Currency.RUB, provider: Provider = Provider.QIWI):
        """
        Перевод денег на Qiwi кошелёк или Карты других банков.

        :type account: str
        :type amount: float
        :type comment: str
        :type currency: Currency
        :type provider: Provider

        :param comment: Комментарий к переводу
        :param currency: Валюта. Разрешены только рубли
        :param amount: Сумма перевода
        :param provider: Провайдер (см. Enums.Provider). Куда необходимо переводить деньги:
            на Qiwi, на Карту
        :param account: Номер получателя

        :raises: APIError

        :returns: Json Object
        :rtype: dict
        """
        url = self._host + 'sinap/api/v2/terms/{}/payments'.format(provider.value)

        json = {
            'id': self._transaction_id,
            'sum': {
                'amount': amount,
                'currency': str(currency.values[1])
            },
            'paymentMethod': {
                'type': 'Account',
                'accountId': '643'
            },
            'fields': {'account': account},
            'comment': comment
        }

        if provider != Provider.QIWI:
            del json['comment']

        response = self._req(url, json=json)
        data = response.json()

        if 'code' in data or 'errorCode' in data:
            data["status_code"] = response.status_code
            raise APIError(data)

        return data

    def _req(self, url, params: dict = None, json: dict = None):
        """
        Args:
            url:
            params (dict):
            json (dict):
        """
        if json:
            response = self._s.post(url, json=json)
        else:
            response = self._s.get(url, params=params)

        if response.status_code != 200 and not response.content:
            RequestError(response.status_code)

        return response

    def get_balance(self, retry=False):
        """
        Args:
            retry:
        """
        url = self._host + 'funding-sources/v2/persons/{}/accounts'.format(self.phone)
        params = {}

        if retry:
            params = {
                'timeout': 1000
            }

        response = self._req(url, params).json()

        balances = []

        for account in response['accounts']:
            if account['hasBalance']:
                if not account['balance']:
                    return self.get_balance(True)
                balances.append(Balance(account))

        return balances

    def _person_profile(self, auth_info=True, contract_info=True, user_info=True):
        """
        Args:
            auth_info:
            contract_info:
            user_info:
        """
        url = self._host + 'person-profile/v1/profile/current'

        params = {
            'authInfoEnabled': auth_info,
            'contractInfoEnabled': contract_info,
            'userInfoEnabled': user_info
        }

        return self._req(url, params)

    def identification(self):
        url = self._host + 'identification/v1/persons/{}/identification'.format(self.phone)

        return self._req(url).json()

    def get_payments(self, rows: int = 25, operation: OperationType = OperationType.ALL):
        """
        Args:
            rows (int):
            operation (str):
        """
        url = self._host + 'payment-history/v2/persons/{}/payments'.format(self.phone)

        params = {
            'rows': rows,
            'operation': operation.value
        }

        return [Payment(i) for i in self._req(url, params).json()["data"]]

    def get_transaction(self, transaction_id: int):
        """
        Args:
            transaction_id (int):
        """
        url = self._host + 'payment-history/v2/transactions/{}'.format(transaction_id)

        return Payment(self._req(url).json())

    @staticmethod
    def __callback():
        LightQiwiCallback()

    def check(self, interval: int = 3, amount: int = 25,
              operation: OperationType = OperationType.IN):
        """

        :param interval:
        :param amount:
        :param operation:
        :return:
        """
        payments = self.get_payments(operation=operation)

        while True:
            sleep(interval)

            new_payments = self.get_payments(amount, operation)
            update = False
            for payment in new_payments:
                if payment not in payments:
                    update = True
                    yield payment
            if update:
                payments = new_payments

    def bind_check(self, interval: int = 3, amount: int = 25,
                   operation: OperationType = OperationType.IN):
        """

        :param interval:
        :param amount:
        :param operation:
        :return decorator:
        """

        def decorator(func):
            if func.__code__.co_argcount != 1:
                raise ArgumentError('Функция должна иметь 1 аргумент!')

            def run():
                for payment in self.check(interval, amount, operation):
                    func(payment)

            self.func = run

        return decorator

    def start(self):
        return self.func()

    def start_threading(self):
        return start_new_thread(self.func, ())
