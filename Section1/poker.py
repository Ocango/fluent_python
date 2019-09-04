#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
#获取序列的值
__getitem__()
#获取序列的长度
__len__()
这些特殊方法就是为了让编译器调用的。比如getitem就是为了让我们能用下标访问序列
'''
import collections
#创建无方法只有少量属性的对象
Card = collections.namedtuple('Card',['rank','suit'])

class FrenchDeck(collections.MutableSequence):
    ranks = [str(n) for n in range(2,11)] + list('JQKA')
    suits = "红桃 梅花 红心 黑桃".split()

    def __init__(self):
        self._cards = [Card(rank,suit) for suit in self.suits
                                    for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)

    def __getitem__(self,position):
        return self._cards[position]
    
    def __setitem__(self,position,value):
        self._cards[position] = value
    
    def __delitem__(self,position):
        del self._cards[position]
    
    def insert(self,position,value):
        self._cards.insert(position,value)

#实现特殊方法的作用，凡是作为序列标准方法中借用了__len__或__getitem__都可以直接用了
from random import choice
deck = FrenchDeck()
print(len(deck))
#抽牌
print(choice(deck))
#切片
print(deck[:5])
print(deck[12::13])
#迭代
# for card in reversed(deck):
#     print(card)

#排序
suit_values = dict((['黑桃',0],['红心',1],['梅花',2],['红桃',3]))
def spades_high(card):
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]
for card in sorted(deck,key=spades_high):
    print(card)