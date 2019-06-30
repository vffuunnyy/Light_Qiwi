# -*- coding: utf-8 -*-


def parse_item_enum(parse_item, enum):
    """
    Args:
        parse_item:
        enum:
    """
    for i in enum:
        if parse_item == i.value:
            return i

    return enum.UNKNOWN


def parse_item_multi_value_enum(parse_item, enum):
    """
    Args:
        parse_item:
        enum:

    :return Currency
    """
    for i in enum:
        if parse_item in i.values:
            return i

    return enum.UNKNOWN
