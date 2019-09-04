"""
A line item for a bulk food order has description, weight and price fields::
    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.weight, raisins.description, raisins.price
    (10, 'Golden raisins', 6.95)
A ``subtotal`` method gives the total price for that line item::
    >>> raisins.subtotal()
    69.5
The weight of a ``LineItem`` must be greater than 0::
    >>> raisins.weight = -20
    Traceback (most recent call last):
        ...
    ValueError: value must be > 0
Negative or 0 price is not acceptable either::
    >>> truffle = LineItem('White truffle', 100, 0)
    Traceback (most recent call last):
        ...
    ValueError: value must be > 0
No change was made::
    >>> raisins.weight
    10
"""


# BEGIN LINEITEM_V3
class Quantity:  # 描述符类

    def __init__(self, storage_name):
        self.storage_name = storage_name  # 托管实例中储存值

    def __set__(self, instance, value):  # 尝试为委托属性赋值时调用
        if value > 0:
            instance.__dict__[self.storage_name] = value  # 为防止无限递归，直接处理instance.__dict__
        else:
            raise ValueError('value must be > 0')


class LineItem:
    weight = Quantity('weight')  # 绑定描述符实例
    price = Quantity('price')  # 绑定描述符实例
    test_book = 3

    def __init__(self, description, weight, price):  # 初始化
        self.description = description
        self.weight = weight
        self.price = price
    def subtotal(self):
        return self.weight * self.price
# END LINEITEM_V3

test1 = LineItem('123',12,12)
LineItem.test_book = 5
test2 = LineItem('345',12,12)