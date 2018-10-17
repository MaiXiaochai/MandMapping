# -*- coding: utf-8 -*-

# @File         : prototype_design_pattern.py
# @Project      : mindmapping
# @Time         : 2018/10/15 23:44
# @Site :       : https://github.com/MaiXiaochai
# @Author       : maixiaochai

from collections import OrderedDict

"""
原型设计模式(Prototype design pattern)，无非就是克隆一个对象。
如Python中的copy.deepcopy()实现的就是克隆一个对象。

应用场景：我们已经有了一个对象，并希望创建对象的一个完整副本时。
使用建议：如果可用资源有限（例如，嵌入式系统）或性能至关重要（例如，高性能计算），那么使用浅层副本（浅层复制）可能更加。

浅副本(copy.copy())和深副本(copy.deepcopy())的区别(Python官方解释)：
    浅副本构造一个新的符合对象后，（会尽可能地）将在原始对象中找到的对象的引用插入新对象中。
    深副本构造一个新的符合对象后，会递归地将在原对象中找到的对象的副本插入新对象中。
"""

"""
DEMO:
    同一本书，先后修订版本之间，
    有很多相似之处：作者、出版商、描述该书的标签/关键词是完全一样的；
    也有很多不同之处：价格、页数和出版日期。
    这表明从头创建一本新书并不总是最佳方式。如果知道这两个版本之间的诸多相似之处，则可以先克隆一份，
    然后仅修改新版本与旧版本之间的不同之处。
    以下例子，使用原型模式创建一个展示图书信息的应用。
"""


class Book:
    def __init__(self, name, authors, price, **rest):
        """rest的例子有：出版商、长度、标签、出版日期"""
        self.name = name
        self.authors = authors
        self.price = price

        # 将rest中的内容添加到类的内部字典中
        self.__dict__.update(rest)

    def __str__(self):
        my_list = []
        ordered = OrderedDict(sorted(self.__dict__.items()))

        for i in ordered.keys():
            my_list.append('{}: {}'.format(i, ordered[i]))
            if i == 'price':
                my_list.append('$')
            my_list.append('\n')
        print(my_list)
        return ''.join(my_list)


if __name__ == '__main__':
    book = Book('python', 'Zhang', 10, pages=100)
    print(book)
