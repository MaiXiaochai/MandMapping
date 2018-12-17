# -*- coding: utf-8 -*-

# @File         : prototype_design_pattern.py
# @Project      : mindmapping
# @Time         : 2018/10/15 23:44
# @Site         : https://github.com/MaiXiaochai
# @Author       : maixiaochai

import copy
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
        """rest的例子有：出版商、长度、标签、出版日期
        book = Book('python', 'Wang', 10, price=100)
        print(book)
        out:
            authors: Wang
            name: python
            pages: 100
            price: 10$
        """
        self.name = name
        self.authors = authors
        self.price = price

        # 将rest中的内容添加到类的内部字典中
        self.__dict__.update(rest)

    def __str__(self):
        my_list = []

        # 按照key排序，组成有序字典,sorted后边这种写法不优雅
        ordered = OrderedDict(sorted(self.__dict__.items()))

        for i in ordered.keys():
            my_list.append('{}: {}'.format(i, ordered[i]))
            if i == 'price':
                my_list.append('$')
            my_list.append('\n')
        return ''.join(my_list)


class Prototype:
    """
    该类实现了原型设计模式。核心是clone()方法，该方法使用copy.deepcopy()实现真正的克隆工作。
    但该类还做了更多的事情，它包含register()和unregister()，这两个方法用于在一个字典中追踪被克隆的对象。
    使用变长列表attr，可以仅传递那些在克隆一个对象时真正需要变更的属性变量。
    """
    def __init__(self):
        self.objects = dict()
        
    def register(self, identifier, obj):
        self.objects[identifier] = obj
    
    def unregister(self, identifier):
        del self.objects[identifier]
        
    def clone(self, identifier, **attr):
        found = self.objects.get(identifier)
        if not found:
            raise ValueError('Incorrect objects identifier: {}'.format(identifier))
        
        obj = copy.deepcopy(found)
        obj.__dict__.update(attr)
        return obj


def main():
    b1 = Book('The C Programming Language', ('Brian W Kernighan', 'Denis M Ritchie'),
              price=118, publisher='Prentice Hall', length='228',
              publication_date='1978-02-22', tags=('C', 'programming', 'algorithms', 'data structures'))
    prototype = Prototype()
    cid = 'k&r-first'

    # 这里注册了b1
    prototype.register(cid, b1)

    # 这里深层拷贝了b1，并对b1的一些属性进行了修改。不要被复杂的外表所迷惑，
    # 其实就是深层拷贝了一个字典，然后对字典里边的某些键值对进行了修改
    b2 = prototype.clone(cid, name='The C Programming Language(ANSI)', price=48.99,
                         length=274, publication_date='1988-04-01', edition=2)

    for i in (b1, b2):
        print(i)

    print("ID b1:{} != ID b2: {}".format(id(b1), id(b2)))

    """
    Out:
    authors: ('Brian W Kernighan', 'Denis M Ritchie')
    length: 228
    name: The C Programming Language
    price: 118$
    publication_date: 1978-02-22
    publisher: Prentice Hall
    tags: ('C', 'programming', 'algorithms', 'data structures')
    
    authors: ('Brian W Kernighan', 'Denis M Ritchie')
    edition: 2
    length: 274
    name: The C Programming Language(ANSI)
    price: 48.99$
    publication_date: 1988-04-01
    publisher: Prentice Hall
    tags: ('C', 'programming', 'algorithms', 'data structures')
    
    ID b1:2311079469968 != ID b2: 2311079472656"""


if __name__ == '__main__':
    main()

