# -*- coding: utf-8 -*-
from light_qiwi.enums import OperationType, Currency, PaymentStatus
from light_qiwi.utils import parse_item_enum, parse_item_multi_value_enum


class Payment:
    """Объект полученный от
        https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html#payments_list
    """

    transaction_id: int  # ID транзакции в процессинге QIWI Wallet
    trm_txn_id: int  # Клиентский ID транзакции
    type: OperationType  # Тип платежа (см. Enums.OperationType)
    phone: int  # Номер вашего кошелька
    error_code: int  # Код ошибки платежа
    error: str  # Описание ошибки
    status: PaymentStatus  # Статус платежа (см. Enums.PaymentStatus)
    status_text: str  # Текстовое описание статуса платежа
    comment: str  # Комментарий к платежу
    currency_rate: float  # Курс конвертации (если применяется в транзакции)
    cheque_ready: bool  # Специальное поле
    bank_document_available: bool  # Специальное поле
    bank_document_ready: bool  # Специальное поле
    repeat_payment_enabled: bool  # Специальное поле
    favorite_payment_enabled: bool  # Специальное поле
    regular_payment_enabled: bool  # Специальное поле
    extras: dict  # Служебная информация
    amount: float  # Сумма платежа без комиссии
    currency: Currency  # Валюта платежа (см. Enums.CurrencyStr)
    commission: float  # Комиссия платежа
    total: float  # Фактическая сумма платежа или пополнения
    provider_id: int  # ID провайдера в QIWI Wallet
    provider_short_name: str  # Краткое наименование провайдера
    provider_long_name: str  # Развернутое наименование провайдера
    provider_logo_url: str  # Ссылка на логотип провайдера
    provider_description: str  # Описание провайдера (HTML)
    provider_keys: str  # Список ключевых слов
    provider_site_url: str  # Сайт провайдера
    source: dict

    # Дата/время платежа, во временной зоне запроса (см. параметр startDate).
    date: str  # Формат даты ГГГГ-ММ-ДД'T'чч:мм:сс+03:00

    # Для платежей - номер счета получателя
    account: str  # Для пополнений - номер отправителя, терминала или название агента пополнения кошелька

    def __init__(self, raw: dict):
        self.raw = raw

        self._parse(**raw)

    def _parse(self, txnId: int = None, personId: int = None, date: str = None, errorCode: int = None,
               error: str = None, type: str = None, status: str = None, statusText: str = None, trmTxnId: str = None,
               account: str = None, sum: dict = None, commission: dict = None, total: dict = None,
               provider: dict = None, comment: str = None, currencyRate: float = None, extras: dict = None,
               chequeReady: bool = None, bankDocumentAvailable: bool = None, bankDocumentReady: bool = None,
               repeatPaymentEnabled: bool = None, favoritePaymentEnabled: bool = None,
               regularPaymentEnabled: bool = None, source: dict = None, **kwargs):
        self.transaction_id = txnId
        self.trm_txn_id = trmTxnId
        self.type = parse_item_enum(type, OperationType)
        self.phone = personId
        self.error_code = errorCode
        self.error = error
        self.date = date
        self.status = parse_item_enum(status, PaymentStatus)
        self.status_text = statusText
        self.account = account
        self.comment = comment
        self.currency_rate = currencyRate
        self.cheque_ready = chequeReady
        self.bank_document_available = bankDocumentAvailable
        self.bank_document_ready = bankDocumentReady
        self.repeat_payment_enabled = repeatPaymentEnabled
        self.favorite_payment_enabled = favoritePaymentEnabled
        self.regular_payment_enabled = regularPaymentEnabled
        self.extras = extras
        self.source = source
        self.other = kwargs

        if sum:
            self.amount = sum['amount']
            self.currency = parse_item_multi_value_enum(sum['currency'], Currency)

        if commission:
            self.commission = commission['amount']

        if total:
            self.total = total['amount']

        if provider:
            self.provider_id = provider['id']
            self.provider_short_name = provider['shortName']
            self.provider_long_name = provider['longName']
            self.provider_logo_url = provider['logoUrl']
            self.provider_description = provider['description']
            self.provider_keys = provider['keys']
            self.provider_site_url = provider['siteUrl']

    def __eq__(self, other):
        if isinstance(other, Payment):
            return self.transaction_id == other.transaction_id

    def __str__(self):
        return str(self.raw)

    def __repr__(self):
        return str(self.raw)


class Balance:
    """Объект полученный от
        https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html?http#balances_list
    """

    alias: str  # Псевдоним пользовательского баланса
    fs_alias: str  # Псевдоним банковского баланса
    bank_alias: str  # Псевдоним банка
    title: str  # Название соответствующего счета кошелька
    type_id: str  # Описание счета
    type_title: str  # Описание счета
    has_balance: bool  # Логический признак реального баланса в системе QIWI Кошелек
    amount: float  # Текущий баланс данного счета
    currency: Currency  # Валюта платежа (см. Enums.CurrencyStr)

    def __init__(self, raw: dict):
        """
        :param raw: Объект account от balances_list
        :type raw: dict
        """

        self.raw = raw

        self._parse(**raw)

    def _parse(self, alias: str = None, fsAlias: str = None, bankAlias: str = None, title: str = None,
               hasBalance: bool = None, currency: int = None, type: dict = None, balance: dict = None, **kwargs):
        self.alias = alias
        self.fs_alias = fsAlias
        self.bank_alias = bankAlias
        self.title = title
        self.has_balance = hasBalance
        self.currency = parse_item_multi_value_enum(currency, Currency)
        self.other = kwargs

        if type:
            self.type_id = type['id']
            self.type_title = type['title']

        if balance:
            self.amount = balance['amount']

    def __str__(self):
        return str(self.amount)

    def __repr__(self):
        return "<Balance: {}, Alias: {}, Currency: {}>".format(
            self.amount, self.alias, self.currency
        )


class QiwiTransferAnswer:
    """Объект полученный от
        https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html#p2p
    """

    id: int  # Копия параметра id из исходного запроса
    transaction_id: int  # ID транзакции в процессинге QIWI Wallet
    terms: int  # Константа, 99
    currency: Currency  # Валюта платежа (см. Enums.CurrencyStr)
    account: str  # Копия account из исходного запроса
    amount: float  # Копия amount из исходного запроса
    source: str  # Константа, account_643
    comment: str  # Копия параметра comment из исходного запроса
    status: str  # Текущий статус транзакции, только значение Accepted

    def __init__(self, raw: dict):
        self.raw = raw

        self._parse(**raw)

    def _parse(self, id: int = None, terms: int = 99, fields: dict = None, sum: dict = None, transaction: dict = None,
               comment: str = None, source: str = None, **kwargs):
        self.id = id
        self.terms = terms
        self.comment = comment
        self.source = source
        self.other = kwargs

        if fields:
            self.account = fields['account']

        if sum:
            self.amount = sum['amount']
            self.currency = parse_item_multi_value_enum(sum['currency'], Currency)

        if transaction:
            self.transaction_id = transaction['id']
            self.status = transaction['state']['code']

    def __str__(self):
        return str(self.raw)

    def __repr__(self):
        return str(self.raw)


class Bill:
    """

    """

    id: int  # Идентификатор счета в QIWI Кошельке
    external_id: str  # Идентификатор счета у мерчанта
    creation_datetime: int  # Дата/время создания счета, Unix-time
    expiration_datetime: int  # Дата/время окончания срока действия счета, Unix-time
    amount: float  # Сумма счета
    currency: Currency  # Валюта суммы счета (см. Enums.CurrencyStr)
    comment: str  # Комментарий к счету
    status: str  # Константа, READY_FOR_PAY
    repetitive: bool  # Служебное поле
    pay_url: str  # Ссылка для оплаты счета в интерфейсе QIWI
    type: str  # Константа, MERCHANT
    provider_id: int  # ID провайдера в QIWI Wallet
    provider_short_name: str  # Краткое наименование провайдера
    provider_long_name: str  # Развернутое наименование провайдера
    provider_logo_url: str  # Ссылка на логотип провайдера

    def __init__(self, raw: dict):
        self.raw = raw

        self._parse(**raw)

    def _parse(self, id: int = None, external_id: str = None, creation_datetime: int = None,
               expiration_datetime: int = None, sum: dict = None, comment: str = None, status: str = None,
               repetitive: bool = None, provider: dict = None, pay_url: str = None, type: str = None, **kwargs):
        self.id = id
        self.external_id = external_id
        self.creation_datetime = creation_datetime
        self.expiration_datetime = expiration_datetime
        self.status = status
        self.comment = comment
        self.repetitive = repetitive
        self.provider = provider
        self.pay_url = pay_url
        self.type = type
        self.other = kwargs

        if sum:
            self.amount = sum['amount']
            self.currency = parse_item_multi_value_enum(sum['currency'], Currency)

        if provider:
            self.provider_id = provider['id']
            self.provider_short_name = provider['shortName']
            self.provider_long_name = provider['longName']
            self.provider_logo_url = provider['logoUrl']

    def __str__(self):
        return str(self.raw)

    def __repr__(self):
        return str(self.raw)
