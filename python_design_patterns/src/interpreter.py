# -*- coding: utf-8 -*-

# @File         : interpreter.py
# @Project      : src
# @Time         : 2018/12/19 22:17
# @Site         : https://github.com/MaiXiaochai
# @Author       : maixiaochai


"""
解释器（interpreter）模式：
        思想：         让非初级用户和领域专家使用一门简单的语言来表达想法。
        简单的语言：    没有变成语言那么复杂的语言。

领域特定语言（Domain Specific Language, DSL）：一种针对一个特定领域的有限表达能力的计算机语言。
    内部DSL语言：构建在一种宿主编程语言之上。比如，使用Python解决线性方程组的一种语言。
                优势：不必担心创建、编译及解析语法因为这些已经被宿主语言解决掉了。
                劣势：会受限于宿主语言的特性。

    外部DSL语言：不依赖于宿主语言。DSL的创建者可以决定语言的方方面面（语法、句法等），
                但也要负责为其创建一个解析器和编译器。为一种新语言创建解析器和编译器是一个非常复杂、长期而又痛苦的过程。

"""
