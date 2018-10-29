# -*- coding: utf-8 -*-

# @File         : decorator_pattern.py
# @Project      : src
# @Time         : 2018/10/29 22:50
# @Site :       : https://github.com/MaiXiaochai
# @Author       : maixiaochai

from timeit import Timer

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
    :param n:       int     大于等于0的整数
    :return:
    """
    assert(n >= 0), 'n must be >= 0'
    return n if n in (0, 1) else fibonacci(n - 1) + fibonacci(n - 2)


known = {0: 0, 1: 1}


def fbnc(n):
    """
    改进菲波那切数列
    :param n:       int     大于等于0的整数
    :return:
    """
    assert(n >= 0), 'n must be >= 0'

    if n in known:
        return known[n]

    res = fbnc(n - 1) + fbnc(n - 2)
    known[n] = res
    return res


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

    t = Timer('fbnc(100)', 'from __main__ import fbnc')
    print(t.timeit())


if __name__ == '__main__':
    main()
