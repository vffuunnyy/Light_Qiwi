# -*- coding: utf-8 -*-
from Light_Qiwi import Qiwi, OperationType


if __name__ == '__main__':
    token, phone = 'token', 'phone'
    api = Qiwi(token, phone)

    """
    Возвращается объект Payment
    В параметре interval можно указать интервал обновления (по ум. 3 сек.)
    В параметре amount - количество операций в 1 запросе (по ум. 25)
    В параметре operation - тип операции Получение\Отправка денег или оба (по ум. только получение денег)
    """
    for payment in api.check(interval=5, amount=2, operation=OperationType.ALL):
        if payment.type == OperationType.IN:
            print("Пришло: {} руб. От +{}.".format(
                payment.amount,
                payment.from_account
            ))

            # -> Пришло 125.25 руб. От +70123456789.

        elif payment.type == OperationType.OUT:
            print("Ушло: {} руб. Кому: +{}.".format(
                payment.amount,
                payment.from_account
            ))

            # -> Ушло 125.25 руб. Кому: +70123456789.
