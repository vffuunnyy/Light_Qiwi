# -*- coding: utf-8 -*-
from _thread import start_new_thread
from time import time, sleep
from typing import Callable, List
from urllib.parse import quote

from requests import Session, Response

from light_qiwi.enums import Provider, Field
from light_qiwi.errors import *
from light_qiwi.objects import *


class Qiwi:

    def __init__(self, token, phone):
        """
        :type token: str
        :type phone: str

        :param token: Токен от API Киви
        :param phone: Номер для которого был получен токен
        """

        self._s = Session()

        self._s.headers['Accept'] = 'application/json'
        self._s.headers['Content-Type'] = 'application/json'
        self._s.headers['Authorization'] = 'Bearer ' + token

        self._host = 'https://edge.qiwi.com'

        self.phone = phone.replace('+', '')

        self.func = None
        # self.bill_func = None
        self._bind_payments: List[str, object] = []
        # self._bind_bills = []

    @property
    def balance(self) -> float:
        """Получить баланс кошелька"""
        balances = self.get_balance()

        assert balances, 'Список балансов пуст!'

        for balance in balances:
            if balance.fs_alias == 'qb_wallet':
                return balance

        return balance

    @property
    def _transaction_id(self) -> str:
        """
        :return: UNIX time * 1000
        """

        return str(int(time() * 1000))

    def get_pay_url(self, amount: float, comment: str = '', account: str = None,
                    lock_fields: list = (Field.COMMENT, Field.ACCOUNT, Field.AMOUNT)) -> str:
        url = 'https://qiwi.com/payment/form/99'
        amount_int = int(amount)
        amount_frac = int(round(amount % 1, 2) * 100)

        # if nickname:
        #    url += f"999?extra['accountType']=nickname&extra['account']={nickname}"
        # else:

        if not account:
            account = self.phone
        url += f"?extra['account']={account}&extra['comment']={comment}" \
               f"&amountInteger={amount_int}&amountFraction={amount_frac}"

        for i, k in enumerate(lock_fields):
            url += f"&blocked[{i}]={k.value}"

        return quote(url, '/?=&:')

    @property
    def identification(self) -> dict:
        """Получить данные идентефикации аккаунта"""
        return self._req(f'{self._host}/identification/v1/persons/{self.phone}/identification').json()

    def pay(self, account: str, amount: float = 1.0, comment: str = '',
            currency: Currency = Currency.RUB, provider: Provider = Provider.QIWI) -> QiwiTransferAnswer:
        """Перевод денег на Qiwi кошелёк или Карты других банков.

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

        :returns: QiwiTransferAnswer object
        :rtype: QiwiTransferAnswer
        """

        url = f'{self._host}/sinap/api/v2/terms/{provider.value}/payments'

        json = {
            'id': self._transaction_id,
            'sum': {
                'amount': amount,
                'currency': str(currency.values[1])
            },
            'paymentMethod': {
                'type': 'Account',
                'accountId': str(currency.values[1])
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

        return QiwiTransferAnswer(data)

    def cancel_bill(self, uid: int) -> Response:
        """Отклонение счёта

        :type uid: int

        :param uid: ID счёта для отклонения

        :rtype: dict
        """

        return self._req(f'{self._host}/checkout/api/bill/reject', json={
            'id': uid
        })

    def pay_bill(self, uid: int, currency: Currency = Currency.RUB) -> dict:
        """Оплата выставленного счёта

        :param uid: ID счёта для оплаты
        :param currency: Валюта счёта (см. Enums.Currency)
        :return:
        """

        url = f'{self._host}/checkout/invoice/pay/wallet'

        json = {
            'invoice_uid': uid,
            'currency': str(currency.values[1])
        }

        response = self._req(url, json=json)
        data = response.json()

        if 'code' in data or 'errorCode' in data:
            data["status_code"] = response.status_code
            raise APIError(data)

        return data

    def _req(self, url, params: dict = None, json: dict = None) -> Response:
        """Метод для общения с API

        :type url: str
        :type params: dict
        :type json: dict

        :param url: Ссылка для запроса
        :param params: Для GET запроса
        :param json: Для POST запроса

        :rtype: Response
        """
        if json:
            response = self._s.post(url, json=json)
        else:
            response = self._s.get(url, params=params)

        if response.status_code != 200 and not response.content:
            RequestError(response.status_code)

        return response

    def get_balance(self, retry=False) -> List[Balance]:
        """Возвращает список балансов

        :type retry: bool

        :param retry: Служебное

        :rtype: list
        """
        url = f'{self._host}/funding-sources/v2/persons/{self.phone}/accounts'
        params = {'timeout': 1000} if retry else {}

        response = self._req(url, params).json()

        balances = []

        for account in response['accounts']:
            if account['hasBalance']:
                if not account['balance']:
                    return self.get_balance(True)
                balances.append(Balance(account))

        return balances

    def _person_profile(self, auth_info=True, contract_info=True, user_info=True) -> Response:
        """Возвращает профиль пользователя

        :type auth_info: bool
        :type contract_info: bool
        :type user_info: bool

        :param auth_info: Служебное
        :param contract_info: Служебное
        :param user_info: Служебное

        :rtype: Response
        """
        url = f'{self._host}/person-profile/v1/profile/current'

        params = {
            'authInfoEnabled': auth_info,
            'contractInfoEnabled': contract_info,
            'userInfoEnabled': user_info
        }

        return self._req(url, params)

    def get_payments(self, rows: int = 25, operation: OperationType = OperationType.ALL) -> List[Payment]:
        """Возвращает список последних операций

        :type rows: int
        :type operation: OperationType

        :param rows: Число платежей в ответе
        :param operation: Указывает какие типы операций отдать в ответе

        :rtype: list
        """
        url = f'{self._host}/payment-history/v2/persons/{self.phone}/payments'

        params = {
            'rows': min(rows, 50),
            'operation': operation.value
        }

        data = self._req(url, params).json()

        if 'error' in data:
            raise APIError(data['error'])
        elif 'data' not in data:
            raise APIError(data)
        else:
            return list(map(Payment, data['data']))

    def get_bills(self, rows: int = 25) -> List[Bill]:
        """Возвращает список выставленных счетов

        :type rows: int

        :param rows: Число счетов в ответе

        :rtype: list
        """

        url = f'{self._host}/checkout/api/bill/search'

        params = {
            'rows': rows,
            'statuses': 'READY_FOR_PAY'
        }

        data = self._req(url, params).json()

        if 'error' in data:
            raise APIError(data['error'])
        elif 'bills' not in data:
            raise APIError(data)
        else:
            return list(map(Bill, data['bills']))

    def get_transaction(self, transaction_id: int) -> Payment:
        """Получить транзакцию по её id
        :type transaction_id: int

        :param transaction_id:

        :rtype: Payment
        """
        url = f'{self._host}/payment-history/v2/transactions/{transaction_id}'

        return Payment(self._req(url).json())

    def check(self, interval: int = 3, amount: int = 25,
              operation: OperationType = OperationType.IN) -> Payment:
        """Проверяет на наличие новых операций
        :type interval: int
        :type amount: int
        :type operation: OperationType

        :param interval: Интервал обновления истории
        :param amount: Количество получаемых объектов за одно обновление
        :param operation: Тип операции, который следует получать

        :rtype: Payment
        """
        payments = []

        while True:
            new_payments = self.get_payments(amount, operation)

            for payment in new_payments:
                if payment not in payments:
                    yield payment

            payments = new_payments

            sleep(interval)

    def bind_check(self, interval: int = 3, amount: int = 25,
                   operation: OperationType = OperationType.IN) -> Callable:
        """
        :type interval: int
        :type amount: int
        :type operation: OperationType

        :param interval: Интервал обновления
        :param amount: Число получаемых платежей из истории
        :param operation: Тип операции плажетей
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
        """Запустить блокирующую обработку новых платежей"""
        return self.func()

    def start_threading(self):
        """Запустить обработку новых платежей в другом потоке"""
        return start_new_thread(self.func, ())

    def on_payment_func(self, interval: int = 3, amount: int = 25,
                        operation: OperationType = OperationType.IN) -> Callable:

        def decorator(func):
            if func.__code__.co_argcount not in (1, 2):
                raise ArgumentError('Функция должна принимать 1 или 2 аргумента!')

            def run():
                for payment in self.check(interval, amount, operation):
                    for bound in self._bind_payments:
                        if payment.comment in bound:
                            self._bind_payments.remove(bound)
                            if func.__code__.co_argcount == 1:
                                func(payment)
                            else:
                                func(payment, bound[1])

            self.func = run

        return decorator

    def bind(self, comment: str, payload: object = None):
        """Ожидание платежа с данным комментарием"""
        self._bind_payments.append((comment, payload))

    # def check_bill(self, interval: int = 3, amount: int = 3):
    #     bills = []
    #
    #     while True:
    #         new_bills = self.get_bills(amount)
    #
    #         for bill in new_bills:
    #             if bill not in bills:
    #                 yield bill
    #
    #         bills = new_bills
    #
    #         sleep(interval)
    #
    # def bind_check_bill(self, interval: int = 3, amount: int = 3):
    #     """
    #     :param interval:
    #     :param amount:
    #     :return decorator:
    #     """
    #
    #     def decorator(func):
    #         if func.__code__.co_argcount != 1:
    #             raise ArgumentError('Функция должна иметь 1 аргумент!')
    #
    #         def run():
    #             for bill in self.check_bill(interval, amount):
    #                 func(bill)
    #
    #         self.bill_func = run
    #
    #     return decorator
    #
    # def start_bill(self):
    #     return self.bill_func()
    #
    # def start_threading_bill(self):
    #     return start_new_thread(self.bill_func, ())
    #
    # def on_bill_func(self, interval: int = 3, amount: int = 3) -> Callable:
    #
    #     def decorator(func):
    #         if func.__code__.co_argcount != 1:
    #             raise ArgumentError('Функция должна иметь 1 аргумент!')
    #
    #         def run():
    #             for bill in self.check_bill(interval, amount):
    #                 if bill.comment in self._bind_bills:
    #                     self._bind_bills.remove(bill.comment)
    #                     func(bill)
    #
    #         self.bill_func = run
    #
    #     return decorator
    #
    # def bind_bill(self, comment):
    #     self._bind_bills.append(comment)
