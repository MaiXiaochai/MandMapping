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

        # ----------------------------------------------------------------------------------------------
        关于__get__():
            object.__get__(self, instance, owner)
            如果class定义了它，则这个class就可以称为descriptor。
            owner是所有者的类，instance是访问descriptor的实例，如果不是通过实例访问，而是通过类访问的话，instance则为None。
            （descriptor的实例自己访问自己是不会触发__get__，而会触发__call__，只有descriptor作为其它类的属性才有意义。）

        关于setattr():
            setattr(object, name, values)
            给对象的属性赋值，若属性不存在，先创建再赋值
            class test():
            ...     name='Tom'
            ...     def run(self):
            ...             return 'HelloWord'
            ...
            t=test()
            hasattr(t, "age")   #判断属性是否存在
            out:False

            setattr(t, "age", "18")   #为属相赋值，并没有返回值
            hasattr(t, "age")    #属性存在了
            Out:True

            有点烧脑，暂时略过整个案例。
            更多关于__get__ 和__set__的详细说明，请阅读
            https://blog.csdn.net/leafage_m/article/details/54960432

        """

        if not obj:
            return None

        value = self.method(obj)
        print('value {}'.format(value))
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


# ---------------------------------------------------------------------------------------------------------------------
"""
现实生活中的例子：
芯片（又名芯片密码）卡是现实生活中使用防护代理的一个好例子。
借记/信用卡包含一个芯片，ATM机或读卡器需要先读取芯片；在芯片通过验证后，需要一个密码（PIN）才能完成交易。
这意味着只有在物理地提供芯片卡且知道密码时才能进行交易。

使用银行指派哦代替现金进行购买和交易是远程代理的一个例子。
支票准许了对一个银行账户的访问。

对象关系映射（Object-Relational Mapping, ORM）API是一个如何使用远程代理的例子。


下面将实现一个简单的保护代理来查看和添加用户。该服务提供一下两个选项：
    1）查看用户列表：这一操作不需要特许权限；
    2）添加新用户：这一操作要求客户端提供一个特殊的密码。
    
"""


class SensitiveInfo:
    def __init__(self):
        self.users = ['nick', 'tom', 'ben', 'mike']

    def read(self):
        print('There are {} users: {}'.format(len(self.users), ' '.join(self.users)))

    def add(self, user):
        self.users.append(user)
        print('Added user {}'.format(user))


class Info:
    """
    Info 是SensitiveInfo的一个保护代理。secret变量值是客户端代码在添加新用户时被要求告知/提供的密码。
    注意，在实际应用中永远不要执行以下操作：
        1）在源码中存储密码；
        2）以明文形式存储密码；
        3）使用一种弱（例如，MD5）货自定义加密形式。
    """
    def __init__(self):
        self.protected = SensitiveInfo()
        self.secret = '0xdeadbeef'

    def read(self):
        self.protected.read()

    def add(self, user):
        sec = input('What is the secret? ')
        self.protected.add(user) if sec == self.secret else print("That's wrong!")


def secret_main():
    info = Info()

    while True:
        print("1. read list |==| 2. add user |==| 3. quit")
        key = input('choose option: ')

        if key == '1':
            info.read()

        elif key == '2':
            name = input('choose username: ')
            info.add(name)

        elif key == '3':
            exit()

        else:
            print('unknown option: {}'.format(key))


if __name__ == '__main__':
    # main()
    secret_main()
