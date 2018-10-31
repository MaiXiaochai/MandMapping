# -*- coding: utf-8 -*-

# @File         : decorator_pattern.py
# @Project      : src
# @Time         : 2018/10/29 22:50
# @Site :       : https://github.com/MaiXiaochai
# @Author       : maixiaochai

from timeit import Timer
from functools import wraps


"""
修饰（装饰）器模式： 以透明的方式，动态地（运行时）扩展一个对象的功能
修饰器：            一个可调用函数对象（函数，方法，类），接受一个函数对象fin作为输入，返回另一个函数对象fout。
修饰器模式和 Python修饰器之间并不是一对一的等价关系。Python修饰器能做的实际上比修饰器模式多得多，其中之一就是实现修饰器模式。

实际例子：
    Django框架大量地使用修饰器。比如视图修饰器，他有以下用途
        1）控制某些HTTP请求对视图的访问；
        2）控制特定视图上的缓存行为；
        3）按单个视图控制压缩；
        4）基于特定HTTP请求头控制缓存。

    Grok框架也使用修饰器来实现不同的目标
        1）将一个函数注册为时间订阅者；
        2）以特定权限保护一个方法；
        3）实现适配器模式。

应用案例：
    当实现 横切关注点（cross-cutting concerns）时，修饰器会大显神威
        1)数据校验；
        2）事务处理（要么所有步骤都成功完成，要么事务失败）；
        3）缓存；
        4）日志；
        5）监控；
        6）调试；
        7）业务规则；
        8）压缩；
        9）加密。

"""
# ---------------------------------------------------------------------------------------------------------------------
# 实现一个memoization(记忆法)修饰器, 所有递归函数都能因memoization而提速，比如斐波那契数列。


def fibonacci(n):
    """
    朴素斐波那切数列
    性能较差
    :param n:       int     大于等于0的整数
    :return:
    """
    assert(n >= 0), 'n must be >= 0'
    return n if n in (0, 1) else fibonacci(n - 1) + fibonacci(n - 2)


known = {0: 0, 1: 1}


def fbnc(n):
    """
    改进菲波那切数列
    性能不再是问题，但代码不够简洁
    :param n:       int     大于等于0的整数
    :return:
    """
    assert(n >= 0), 'n must be >= 0'

    if n in known:
        return known[n]

    res = fbnc(n - 1) + fbnc(n - 2)
    known[n] = res
    return res


# --------------------------------------------------------------------------------------------------------------
# 扩展代码，加入更多的数学函数，并将其转变成一个模块。加入nsum()函数，返回前n个数字的和。
# 该函数已由math.fsum()实现，这里假设Python自带库并未实现该功能，因为你会遇到很多需求但是标准库里没有的情况。


known_sum = {0: 0}


def nsum(n):
    assert(n >= 0), 'n must be >= 0'
    if n in known_sum:
        return known_sum[n]

    res = n + nsum(n - 1)
    known_sum[n] = res
    return res

# 多了一个known_sum的新字典，为nsum提供缓存，函数本身也比不使用memoization时的更复杂。
# 这个模块逐步变得不必要地复杂。如何保持递归函数与朴素版本的一样简单，但在性能上又能与使用memoization的函数相近？--修饰器


def memoize(fn):
    """
    该修饰器接受一个需要使用memoization的函数fn作为输入，使用一个名为known的dict作为缓存。
    warps能保留被它修饰的函数的文档和签名。推荐使用。
    这里设置了参数列表*args,因为被修饰的函数有可能有输入参数。
    :param fn:      obj     函数
    :return:        obj     函数
    """
    known = dict()

    @wraps(fn)
    def memoizer(*args):
        if args not in known:
            known[args] = fn(*args)
        return known[args]

    return memoizer


# -----------------------------------------------------------------------------------------------------------------
# 修饰器应用

@memoize
def nsum(n):
    """
    返回前n个数字的和
    :param n:       int     整数
    :return:        int     前n个数字的和
    """
    assert(n >= 0), 'n must be >= 0'
    return 0 if n == 0 else n + nsum(n - 1)


@memoize
def fbncd(n):
    """
    返回菲波那切数列第n个数
    :param n:
    :return:
    """
    assert(n >= 0), 'n must be >= 0'
    return n if n in (0, 1) else fbncd(n - 1) + fbncd(n - 2)


def main_test():
    """
    展示如何使用被修饰的函数，并测试其性能。
    measure是一个字典列表，用于避免代码重复。
    __name__和__doc__分别是如何展示正确的函数名称和文档字符串值的。
    :return:

    Out:
    name: fbncd,doc:
    返回菲波那切数列第n个数
    :param n:
    :return:
    ,executing: fbncd(100), time: 0.23861463099999997

    name: nsum,doc:
    返回前n个数字的和
    :param n:       int     整数
    :return:        int     前n个数字的和
    ,executing: nsum(200), time: 0.24195961499999996
    """

    measure = [
        {'exec': 'fbncd(100)',
         'import': 'fbncd',
         'func': fbncd},
        {'exec': 'nsum(200)',
         'import': 'nsum',
         'func': nsum}
    ]

    for m in measure:
        t = Timer('{}'.format(m['exec']), 'from __main__ import {}'.format(m['import']))
        print('name: {},'
              'doc: {},'
              'executing: {}, '
              'time: {}'.format(m['func'].__name__,
                                m['func'].__doc__,
                                m['exec'],
                                t.timeit()))


def main():
    """
    :return:

    fibonacci(8)
    Out: 9.572507371

    fbnc(100):
    Out: 0.15732129500000003
    """
    # t = Timer('fibonacci(8)', 'from __main__ import fibonacci')
    # print(t.timeit())

    # t = Timer('fbnc(100)', 'from __main__ import fbnc')
    # print(t.timeit())


if __name__ == '__main__':
    main_test()
