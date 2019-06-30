Light_Qiwi ![Python 3.5, 3.6, 3.7](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg?logo=python)
----------
**Light_Qiwi** – Python модуль для написания скриптов для Qiwi (qiwi.com) (API wrapper)

* [Документация](https://light-qiwi.readthedocs.io/en/latest/)
* [Примеры использования](./examples)
* [Документация по API](https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html)

```python
from Light_Qiwi import Qiwi

api = Qiwi('00000000000000000000000000000000', '+70123456789')


"""
Первый параметр - указать интервал обновления (по ум. 3 сек.)
Второй параметр - количество операций в 1 запросе (по ум. 25)
Третий параметр - тип операции Получение\Отправка денег или Все
    (по ум. только получение денег)
"""
@api.bind_check(5, 5)
def receive(payment):
    if payment.account == "79000000000":
        api.pay(payment.account, payment.amount, "Забери свои деньги!")
        
api.start()
```

Установка
----------
    $ pip install light_qiwi
    
Автор
----------
Вопросы задавать сюда или в **issue**:
* **[VK](https://vk.com/int.parse)**
* **[Telegram](https://t.me/vffuunnyy)**