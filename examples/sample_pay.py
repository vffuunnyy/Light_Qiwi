# -*- coding: utf-8 -*-
from light_qiwi import Qiwi, Provider

api = Qiwi('00000000000000000000000000000000', '71234567890')

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
