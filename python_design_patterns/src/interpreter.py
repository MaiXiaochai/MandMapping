# -*- coding: utf-8 -*-

# @File         : interpreter.py
# @Project      : src
# @Time         : 2018/12/19 22:17
# @Site         : https://github.com/MaiXiaochai
# @Author       : maixiaochai

from pyparsing import Word, OneOrMore, Optional, Group, Suppress, alphanums


"""
1、解释器（interpreter）模式：
        思想：         让非初级用户和领域专家使用一门简单的语言来表达想法,解决他们的问题。
        简单的语言：    没有变成语言那么复杂的语言。

2、领域特定语言（Domain Specific Language, DSL）：一种针对一个特定领域的有限表达能力的计算机语言。
    1）内部 DSL语言：构建在一种宿主编程语言之上。比如，使用Python解决线性方程组的一种语言。
                优势：不必担心创建、编译及解析语法因为这些已经被宿主语言解决掉了。
                劣势：会受限于宿主语言的特性。

    2）外部 DSL语言：不依赖于宿主语言。DSL的创建者可以决定语言的方方面面（语法、句法等），
                但也要负责为其创建一个解析器和编译器。为一种新语言创建解析器和编译器是一个非常复杂、长期而又痛苦的过程。

3、解释器模式仅与内部 DSL相关。我们的目标是使用宿主语言特性构建一种简单但有用的语言。
   解释器根本不处理语言解析，它假设我们已经有某种便利形式的解析好的数据，
   可以是抽象语法树（abstract syntax tree, AST）或其它好用的数据结构。

4、列子：
    1)五线谱是音乐的语言，音乐演奏者是这种语言的解释器。
    2)pyT是一个用于生成(X)HTML的Python DSL，是内部 DSL。非常适合使用解释器模式。
"""

# --------------------------------------------------------------------------
# 创建一种内部DSL控制一个智能屋。（紧贴物联网时代）
# boiler 锅炉
"""
一个事件的形式为 command -> receiver -> arguments
    1)参数部分可选，并不是所有事件都要求有参数，如 open -> gate
    2)要求参数的事件例子，如 increase -> boiler temperature -> 3 degrees
    3)-> 符号用于标记事件一个部分的结束， 并声明下一个部分的开始

    4）实现一种内部DSL有多种方式，普通正则表达式、字符串处理、操作符重载的组合以及元编程，或者一个能帮我们完成困难工作的库/工具。
    5）解释器不处理解析，这里为实战例子，所以进行了解析。这里用标准Python3工具 Pyparsing来完成解析工作。
"""

# 定义简单语法，用 巴科斯-诺尔 形式表示法来定义语法
"""
    event :: = command token receiver token arguments
    command :: = word+
    word :: = a collection of one or more alphanumeric(字母数字的) characters
    token :: = ->
    receiver :: = word+
    arguments ::= word+
    
    这个语法告诉我们的是一个事件具有 command -> receiver -> arguments 的形式，
    并且命令、接收者及参数也具有相同的形式，即一个或多个字母数字字符的组合。
    数字部分是为了让我们能够在命令 increase -> boiler temperature -> 3 degrees 中传递3 degrees这样的参数
    
    代码和语法定义基本的不同点是，代码需要以自底向上的方式编写。如，如果不先为word赋一个值，那就不能使用它。
"""


class Gate:
    pass


class Garage:
    """
    garage 车库
    """
    pass


class AirCondition:
    """
    air condition 空调设备
    """
    pass


class Heating:
    pass


class Boiler:
    def __init__(self):
        self.temperature = 83 # 摄氏度

    def __str__(self):
        return 'boiler temperature: {}'.format(self.temperature)

    def increase_temperature(self, amount):
        # amount 数量
        print("increasing the boiler's temperature by {} degrees".format(amount))
        self.temperature += amount

    def decrease_temperature(self, amount):
        print("decreasing the boiler's temperature by {} degrees".format(amount))
        self.temperature -= amount


class Fridge:
    """
    fridge 冰箱
    """
    pass


def main():
    pass


if __name__ == '__main__':
    pass
