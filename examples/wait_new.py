# -*- coding: utf-8 -*-
from Light_Qiwi import Qiwi, OperationType

api = Qiwi("token", "phone")

"""
Возвращается объект Payment
В параметре interval можно указать интервал обновления (по ум. 3 сек.)
В параметре amount - количество операций в 1 запросе (по ум. 25)
В параметре operation - тип операции Получение/Отправка денег или оба (по ум. только получение денег)
"""


@api.bind_check(operation=OperationType.ALL)
def waiter(payment):
    if payment.type == OperationType.IN:
        print("Пришло: {} руб. От +{}.".format(
            payment.amount,
            payment.account
        ))

        # >>> Пришло 125.25 руб. От +70123456789.

    elif payment.type == OperationType.OUT:
        print("Ушло: {} руб. Кому: +{}.".format(
            payment.amount,
            payment.account
        ))

        # >>> Ушло 125.25 руб. Кому: +70123456789.


if __name__ == '__main__':
    """
        Первый сопособ подойдёт вам, если обработа платежей должна происходить фоново.
        Например, для ботов в телеграм и пр.
        
        Второй способ хорош, если программа нацелена на ожидание платежа.
        Например, если вы сделали оповещение себе о новых платежах.
    """
    api.start_threading()  # Запускает неблокирующиее ожидание платежей
    api.start()  # Запускает блокирующее ожидание платежей

    # Второй способ можно сделать без декоратора и функции:

    for payment in api.check(interval=5, amount=2, operation=OperationType.ALL):
        print(payment)  # Вывод всех новых операций

        # >>> {'txnId': ..., 'personId': ...,...}
