# BEGIN LINEITEM_V2_PROP_FACTORY_FUNCTION
def quantity(storage_name):  # <1>

    def qty_getter(instance):  # instance代指存储属性的LineItem实例(其实就是类里面第一个参数代表self)
        return instance.__dict__[storage_name]  # <3>

    def qty_setter(instance, value):  # <4>
        if value > 0:
            instance.__dict__[storage_name] = value  # 为嘛要用这种复制方法？因为设置特性会覆盖原有的属性值，要是用instance.storage_name，那会出现无限递归
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)  # <6>
# END LINEITEM_V2_PROP_FACTORY_FUNCTION


# BEGIN LINEITEM_V2_PROP_CLASS
class LineItem:
    weight = quantity('weight')  # <1>
    price = quantity('price')  # <2>

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # <3>
        self.price = price

    def subtotal(self):
        return self.weight * self.price  # <4>
# END LINEITEM_V2_PROP_CLASS