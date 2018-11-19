# -*- coding: utf-8 -*-

# @File         : proxy.py
# @Project      : src
# @Time         : 2018/11/13 23:11
# @Site :       : https://github.com/MaiXiaochai
# @Author       : maixiaochai

"""
代理模式(Proxy design pattern)：该模式因使用代理（又名替代，surrogate）对象在访问实际对象之前执行重要操作而得其名。
    比较知名的代理：
        1）远程代理：实际用于在不同地址空间（例如，某个网络服务器）的对象在本地的代理者。
        2）虚拟代理：用于懒初始化，将一个大计算量对象的创建延迟到真正需要需要的时候进行。
        3）保护/防护代理：控制对敏感对象的访问。
        4）智能（引用）代理：在对象被访问时执行额外的动作。此类代理的例子包括引用计数和线程安全检查。
"""

# -------------------------------------------------------------------------------------------------------------------
"""
虚拟代理
"""


class LazyProperty:
    """
    修饰器
    当修饰某个特性时，该类惰性地（首次使用时）加载特性，而不是立即进行。
    该类实际上是一个描述符。
    描述符(descriptor)是Python中重写类属性访问方法（__get__()、__set__()和__delete__()）的默认行为要使用的一种推荐机制。
    该类仅重写了__get__()方法，因为这是器需要重写的唯一访问方法。我们无需重写所有方法。
    """
    def __init__(self, method):
        self.method = method
        self.method_name = method.__name__
        # print('function overrider: {}'.format(self.fget))
        # print("function's name: {}".format(self.func_name))

    def __get__(self, obj, cls):
        """
        __get__()方法所访问的特性值，正是下层方法想要赋的值，并用setattr()来手动赋值。
        __get__()实际做的事非常简单，就是使用值来替代方法！这意味着不仅特性是惰性加载的，而且仅可以设置一次。
        """
        if not obj:
            return None

        value = self.method(obj)
        # print('value {}'.format(value))
        setattr(obj, self.method_name, value)
        return value


class Test:
    """
    该类主要演示如何使用LazyProperty类。
    """
    def __init__(self):
        """我们想懒加载_resource变量，因此将其初始化为None"""
        self.x = 'foo'
        self.y = 'bar'
        self._resource = None

    @LazyProperty
    def resource(self):
        """
        使用LazyProperty类修饰。因演示目的，LazyProperty类将_resource属性初始化为一个tuple。
        通常来说这是一个缓慢/代价大的初始化过程（初始化数据库、图形等）。
        """
        print('initializing self._resource which is: {}'.format(self._resource))

        # 假设这一行的计算成本比较大
        self._resource = tuple(range(5))
        return self._resource


def main():
    """
    展示初始化是如何进行的。
    注意，__get__()访问方法的重写使得可以将resource()方法当作一个变量（可以使用t.resource代替t.resource()）。

    Out:
    foo
    bar
    initializing self._resource which is: None
    (0, 1, 2, 3, 4)
    (0, 1, 2, 3, 4)
    """
    t = Test()
    print(t.x)
    print(t.y)
    print(t.resource)
    print(t.resource)


if __name__ == '__main__':
    main()
