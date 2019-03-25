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

5)当我们希望在一个对象（主持者/发布者/可观察者）发生变化时通知/更新另一个或多个对象的时候，通常会使用观察者模式。
"""


# 实现一个数据格式化程序。默认格式化程序是以十进制格式展示一个数值，我们可以添加/注册十六进制和二进制格式化程序，
# 当然，我们可以添加/注册更多的格式化程序。每次更新默认格式化程序的值时，已注册的格式化程序就会收到通知，并采取行动。
# 在这里，行动就是以相关的格式展示新的值。
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
        # o.notify(self)这里其实是在调用订阅者本身的notify()方法
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

    @property
    def data(self):
        """
        @property修饰器，提供变量_data的读访问方式，使用object.data代替object.data()
        """
        return self._data

    @data.setter
    def data(self, new_value):
        """
        使用了@setter修饰器，该修饰器会在每次使用赋值操作(=)为_data变量赋新值时被调用。
        就方法本身而言，它尝试吧新值强制类型转换为一个整数，并在类型转换失败时处理异常。
        :param new_value:
        :return:
        """
        try:
            self._data = int(new_value)
        except ValueError as e:
            print("Error: {}".format(e))
        else:
            # 如果try里边的语句正常执行，然后就执行else里的语句
            self.notify()


class HexFormatter:
    """
    十六进制观察者
    """
    def notify(self, publisher):
        print("{}: '{}' has now hex data = {}".format(type(self).__name__, publisher.name, hex(publisher.data)))


class BinaryFormatter:
    """
    二进制观察者
    """
    def notify(self, publisher):
        print("{}: '{}' has now bin data = {}".format(type(self).__name__, publisher.name, bin(publisher.data)))


def main():
    df = DefaultFormatter('test1')
    print(df, '\n')

    hf = HexFormatter()
    df.add(hf)
    df.data = 3
    print(df, '\n')

    bf = BinaryFormatter()
    df.add(bf)
    df.data = 21
    print(df, '\n')

    df.remove(hf)
    df.data = 40
    print(df, '\n')

    df.remove(hf)
    df.add(bf)
    df.data = 'hello'
    print(df, '\n')

    df.data = 15.8
    print(df)


if __name__ == "__main__":
    main()
    """
    out:
    DefaultFormatter: 'test1' has data = 0 

    HexFormatter: 'test1' has now hex data = 0x3
    DefaultFormatter: 'test1' has data = 3 
    
    HexFormatter: 'test1' has now hex data = 0x15
    BinaryFormatter: 'test1' has now bin data = 0b10101
    DefaultFormatter: 'test1' has data = 21 
    
    BinaryFormatter: 'test1' has now bin data = 0b101000
    DefaultFormatter: 'test1' has data = 40 
    
    Failed to remove: <__main__.HexFormatter object at 0x00000236CF4151D0>
    Falied to add: <__main__.BinaryFormatter object at 0x00000236CF4155F8>
    Error: invalid literal for int() with base 10: 'hello'
    DefaultFormatter: 'test1' has data = 40 
    
    BinaryFormatter: 'test1' has now bin data = 0b1111
    DefaultFormatter: 'test1' has data = 15
    """
