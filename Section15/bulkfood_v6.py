import model_v6 as model

@model.entity
class LineItem():
    description = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()

    def __init__(self,description,weight,price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price


raisins = LineItem('abc',12,12)
dir(raisins)
