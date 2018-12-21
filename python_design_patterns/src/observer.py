# -*- coding: utf-8 -*-

# @File         : observer.py
# @Project      : src
# @Time         : 2018/12/21 0:09
# @Site         : https://github.com/MaiXiaochai
# @Author       : maixiaochai

"""
1）观察者（observer）模式：
    背后的思想是降低发布者与订阅者之间的耦合度，从而易于在运行时添加/删除订阅者。

2）拍卖会类似于观察者模式，
    每个拍卖出价人都有一些拍牌，在他们想出价时就可以举起来。不论出价人在何时举起一块牌，
   拍卖师都会像主持者那样更新报价，并将新的价格广播给所有出价人（订阅者）。

3）RabbitMQ可用于为应用添加异步消息支持，支持多种消息协议（比如，HTTP和AMQP），
    可以在python 应用中用于实现发布-订阅模式，也就是观察者设计模式

4）事件驱动系统是另一个可以使用（通常也会使用）观察者模式的例子。监听者被用于监听特定事件（如键盘键入某个键）。
    事件扮演发布者的角色，监听者则扮演观察者的角色。

"""


# 实现一个数据格式化程序。默认格式化程序是以十进制格式展示一个数值，我们添加/注册十六进制和二进制格式化程序
# 在一些模式中，继承能体现自身价值，观察者模式是这些模式中的一个。我们实现一个基类Publisher，
# 包括添加、删除及通知观察者这些公用功能。


class Publisher:
    def __init__(self):
        self.observers = []

    def add(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
        else:
            print('Falied to add: {}'.format(observer))

    def remove(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print('Failed to remove: {}'.format(observer))

    def notify(self):
        """
        在变化发生时通知所有观察者
        """
        [o.notify(self) for o in self.observers]


class DefaultFormatter(Publisher):
    def __init__(self, name):
        """
        调用基类的__init__()方法，因为这在Python中没法自动完成。
        _data，我们使用了名称改变来声明不能直接访问该变量，虽然Python中直接访问一个变量始终是可能的，
        资深开发人员不会去访问_data变量，因为代码中已经声明不应该这样做。
        """
        Publisher.__init__(self)
        self.name = name
        self._data = 0

    def __str__(self):
        """
        type(self).__name__是一种获取类名的方便技巧，避免了硬编码类名。
        这降低了代码的可读性，却提高了代码的可维护性。
        """
        return "{}: '{}' has data = {}".format(type(self).__name__, self.name, self._data)
