from abc import ABC,abstractmethod
#ABC标准继承类
#abstractmethod抽象方法装饰器
from collections import namedtuple#明天
Customer = namedtuple('Customer','name fidelity')

class LineItem():
    def __init__(self,product,quantity,price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity

class Order():
    '''
    上下文
    '''
    def __init__(self, customer,cart,promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion

    def total(self):
        if not hasattr(self,'__total'):#查看是否有指定的属性
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount
    
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(),self.due())

class Promotion(ABC):#策略：抽象基类
    @abstractmethod
    def discount(self,order):
        '''
        返回折扣金额
        '''

class FidelityPromotion(Promotion):#积分折扣
    '''
    为积分1000以上用户提供%5的折扣
    '''
    def discount(self, order):
        return order.total() *0.05 if order.customer.fidelity >= 1000 else 0

class BulkItemPromo(Promotion):#单品折扣
    '''
    单个商品20个以上时%10折扣
    '''
    def discount(self, order):
        discount = 0
        for item in order.cart:
            if item.quantity >=20:
                discount += item.total() * .1
        return discount

class LargeOrderPromo(Promotion):#类多从优
    '''
    订单不同商品大于10个提供%7
    '''
    def discount(self, order):
        discount_items = {item.product for item in order.cart}
        if len(discount_items) >= 10:
            return order.total() * 0.07
        return 0

print(Order(Customer('JoJo',1100),[LineItem('Banana',20,0.5),LineItem('Apple',5,2)],BulkItemPromo()))

#而因为python支持函数作为一等对象，就可以将策略写作普通的函数，从而传入类计算折扣

#在此基础上如果我们需要迭代最优的折扣方式呢？
'''
promos = [fidelity_promo,bulkItem_promo,large_order_promo]
def best_promo(order):
    return max(promo(order) for promo in promos)
'''

#如何找到模块中的全部策略呢？
promos = [globals()[name] for name in globals() if name.endswith('_promo') and name != 'best_promo']
#或者使用单独内省的promotions模块
import inspect
promos = [func for name,func in inspect.getmembers(Promotion,inspect.isfunction)]
#返回模块Promotion中用户定义的函数

