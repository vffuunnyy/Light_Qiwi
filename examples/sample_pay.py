# -*- coding: utf-8 -*-
from Light_Qiwi import Qiwi, Provider


if __name__ == '__main__':
    token, phone = 'token', 'phone'
    api = Qiwi(token, phone)

    """ Перевод на Qiwi кошелёк """

    account = "77123456780"
    amount = 1050.55
    comment = "Спасибо за помощь!"

    response = api.pay(account, amount, comment)

    print(response)

    # -------------------------------------------

    """ Перевод на карту Visa по России """

    account = "4276640999999999"
    amount = 1050.55
    provider = Provider.RU_VISA

    response = api.pay(account, amount, provider=provider)  # Отправлять комментарии нельзя

    print(response)
