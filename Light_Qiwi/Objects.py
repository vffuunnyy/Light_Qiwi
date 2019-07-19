# -*- coding: utf-8 -*-
from Light_Qiwi.Enums import OperationType, Currency, PaymentStatus, Provider
from Light_Qiwi.Utils import parse_item_enum, parse_item_multi_value_enum


class Payment:
    def __init__(self, raw):
        """
        Объект полученный от
        https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html?http#payments_list

        Args:
            raw (dict): Объект data от payment_history
        """
        self.raw = raw

        #: ID транзакции в процессинге QIWI Wallet
        self.transaction_id = raw['txnId']

        #: Клиентский ID транзакции
        self.trm_txn_id = raw['trmTxnId']

        #: Тип платежа (см. Enums.OperationType)
        self.type = parse_item_enum(raw['type'], OperationType)

        #: Номер кошелька
        self.phone = raw['personId']

        #: Код ошибки платежа
        self.error_code = raw['errorCode']

        #: Описание ошибки
        self.error = raw['error']

        #: Фактическая сумма платежа или пополнения
        self.amount = raw['total']['amount']

        #: Валюта платежа (см. Enums.CurrencyStr)
        self.currency = parse_item_multi_value_enum(
            raw['total']['currency'], Currency
        )

        #: Статус платежа (см. Enums.PaymentStatus)
        self.status = parse_item_enum(raw['status'], PaymentStatus)

        #: Текстовое описание статуса платежа
        self.status_text = raw['statusText']

        #: Дата/время платежа, во временной зоне запроса (см. параметр startDate)
        #: Формат даты ГГГГ-ММ-ДД'T'чч:мм:сс+03:00
        self.date = raw['date']

        #: Для платежей - номер счета получателя
        #: Для пополнений - номер отправителя, терминала или название агента пополнения кошелька
        self.account = raw['account']

        #: Комментарий к платежу
        self.comment = raw['comment']

        #: Комиссия платежа
        self.commission = raw['commission']['amount']

    def __eq__(self, other):
        if isinstance(other, Payment):
            return self.transaction_id == other.transaction_id

    def __str__(self):
        return str(self.raw)


class Balance:

    def __init__(self, raw):
        """
        Объект полученный от
        https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html?http#balances_list

        Args:
            raw (dict): Объект account от balances_list
        """

        self.alias = raw['alias']
        self.balance = raw['balance']['amount']
        self.currency = parse_item_multi_value_enum(raw['currency'], Currency)

    def __str__(self):
        return str(self.balance)

    def __repr__(self):
        return "<Balance: {}, Alias: {}, Currency: {}>".format(
            self.balance, self.alias, self.currency
        )


class QiwiTransferAnswer:
    def __init__(self, raw):
        """
        Объект полученный от
        https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html?http#balances_list

        Args:
            raw (dict): Объект account от balances_list
        """

        self.raw = raw
        self.id = raw['id']
        self.transaction_id = raw['transaction']['id']
        self.terms = parse_item_enum(raw['terms'], Provider)
        self.currency = parse_item_multi_value_enum(raw['transaction']['currency'], Currency)
        self.phone = raw['fields']['account']
        self.amount = raw['sum']['amount']
        self.source = raw['source']
        self.comment = raw['comment']
        self.status = raw['transaction']['state']['code']

    def __str__(self):
        return str(self.raw)
