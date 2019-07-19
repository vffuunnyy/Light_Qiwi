# -*- coding: utf-8 -*-
from Light_Qiwi import Qiwi, OperationType


api = Qiwi("token", "phone")


def write(payment):
    if payment.type == OperationType.IN:
        print("Пришло: {} руб. От +{}.".format(
            payment.amount,
            payment.account
        ))

        # -> Пришло 125.25 руб. От +70123456789.

    elif payment.type == OperationType.OUT:
        print("Ушло: {} руб. Кому: +{}.".format(
            payment.amount,
            payment.account
        ))

        # -> Ушло 125.25 руб. Кому: +70123456789.


@api.bind_check(amount=2, operation=OperationType.ALL)
def waiter(payment):
    write(payment)


if __name__ == '__main__':
    """
    Возвращается объект Payment
    В параметре interval можно указать интервал обновления (по ум. 3 сек.)
    В параметре amount - количество операций в 1 запросе (по ум. 25)
    В параметре operation - тип операции Получение\Отправка денег или оба (по ум. только получение денег)
    """
    
    mode = input("Напишите 1, если декоратор. Напишите 2, если цикл.\n")
    
    if mode == "1":
        api.start()
    elif mode == "2":
        for payment in api.check(amount=2, operation=OperationType.ALL):
            write(payment)
    else:
        print("unknown")
        
