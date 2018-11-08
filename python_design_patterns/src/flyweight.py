# -*- coding: utf-8 -*-

# @File         : flyweight.py
# @Project      : src
# @Time         : 2018/11/5 23:16
# @Site :       : https://github.com/MaiXiaochai
# @Author       : maixiaochai

import random
from enum import Enum

"""
享元模式(flyweight)：
    通过为相似对象引入数据共享来最小化内存使用，提升性能。旨在优化性能和内存使用。
    一个享元(flyweight)就是一个包含状态独立的不可变（又称固有的）数据的共享对象。
    依赖状态的可变（又称非固有的）数据不应是享元的一部分，因为每个对象的这种信息都不同，不能共享。

    通俗的说，就是把大家都需要的做成公共工具放在那，谁想用就用，而不是每个人都造一个属于自己的相同工具。

实际例子：
    比如《反恐精英》中，同一个团队（反恐精英或者是恐怖分子）的所有士兵看起来都是一样的（外在表现）。
    同一个游戏中，（两个团队的）所有士兵都有一些共同的动作，比如，跳起、低头等（行为）。
    这意味着我们可以创建一个享元来包含所有共同的数据。士兵也有许多因人而异的可变数据，这些数据不是享元的一部分，
    比如，枪支、健康状况和地理位置等。

生活中的例子：
享元模式是一个用于优化的设计模式。我们可以把享元看做现实生活中的缓存区。例如，许多书店都有专用的书架来摆放最新和最流行的出版物。
这就是一个缓冲区，你可以现在这些专用书架上看看有没有正在找的书籍，如果没找到，可以让图书管理员来帮你。


若要使享元模式有效，需满足以下条件：
    1）应用需要使用大量的对象；
    2）对象太多，存储/渲染他们的代价太大；
    3）对象ID对于应用不太重要。

memoization 与 享元模式间的区别：
    1）memoization是一种优化技术，使用一个缓存来避免重复计算安歇在更早的执行步骤中已经计算好的结果；
    2）memoization并不是只能应用于某种特定的编程方式，比如面向对象编程(Object-Oriented Programming, OOP),
        他可以应用于方法和简单的函数；
    3）享元则是一种特定于面向对象编程优化的设计模式，关注的是共享对象数据。
"""

# -------------------------------------------------------------------------------------------------------------------
"""
构造一小片果树的森林，小到能确保在单个终端页面中阅读整个输出。然而，无论你构造的森林有多大，内存分配都保持相同。
"""

tree_type_all = Enum('TreeType', 'apple_tree cherry_tree peach_tree')


class Tree:
    """
    pool变量是一个对象池（换句话说，使我们的缓存）。pool是一个类属性，所有实例共享的一个变量。
    __new__方法在__init__方法之前被调用，使用__new__方法把Tree变成一个元类，元类支持自引用。这意味着cls引用的是Tree类。
    当客户端要创建Tree的一个实例时，会以tree_type参数传递树的种类。树的种类用于检查是否创建过相同种类的树。如果是，则返回之前
    创建的对象；否则，将这个新的书中添加到池中，并返回相应的新对象。

    关于__new__和__init__：
        1）__new__方法只负责创建，__init__ 方法只负责初始化；
        2）__new__至少要有一个参数cls，代表要实例化的类，此参数在实例化时由Python解释器自动提供;
        3)__new__必须要有返回值，返回实例化出来的实例，这点在自己实现__new__时要特别注意，可以return父类__new__出来的实例，
          或者直接是object的__new__出来的实例;
        4)__init__有一个参数self，就是这个__new__返回的实例，__init__在__new__的基础上可以完成一些其它初始化的动作，
         __init__不需要返回值。

        [参考文献：https://blog.csdn.net/qq_37616069/article/details/79476249]
    """
    pool = dict()

    def __new__(cls, tree_type):
        obj = cls.pool.get(tree_type, None)

        if not obj:
            obj = object.__new__(cls)
            cls.pool[tree_type] = obj
            obj.tree_type = tree_type
        return obj

    def render(self, age, x, y):
        """
        享元不知道的所有可变（外部）信息都需要由客户端代码显示地传递。
        每棵树都用到一个随机的年龄和一个x，y形式的位置。为了让render()更加有用，
        有必要确保没有树会被渲染到另一棵上。
        render 渲染，着色
        """
        print('render a tree of type {} at ({}, {})'.format(self.tree_type, age, x, y))


def main():
    """
    一棵树的年龄是1~30年间的随机数，坐标是0~100之间的随机值。虽然渲染了18棵树，但仅分配了3棵树的内存。
    输出的最后一行证明当时用享元时，我们不能依赖对象的ID。
    CPython(Python的官方实现)正好使用对象的内存地址作为唯一性ID。
    在本例中，即使两个对象看起来不相同，但是如果它们属于同一个享元家族（这里家族由tree_type定义），那么它们实际上有相同的ID。

    random.Random()和random.random()的关系：
    1）前者生成0和1之间的随机浮点数float；
    2）前者其实是一个隐藏的random.Random()类的实例的random方法；
    3）random.random()和random.Random().random()作用是一样的；
    4）random.Random()生成random模块里的Random类的一个实例，这个实例不会和其他Random实例共享状态，一般是在多线程的情况下使用。
    """
    rnd = random.Random()
    age_min, age_max = 1, 30
    point_min, point_max = 0, 100
    tree_counter = 0

    for _ in range(10):
        t1 = Tree(tree_type_all.apple_tree)
        t1.render(rnd.randint(age_min, age_max),
                  rnd.randint(point_min, point_max),
                  rnd.randint(point_min, point_max))
        tree_counter += 1

    print('-' * 60)
    for _ in range(3):
        t2 = Tree(tree_type_all.cherry_tree)
        t2.render(rnd.randint(age_min, age_max),
                  rnd.randint(point_min, point_max),
                  rnd.randint(point_min, point_max))
        tree_counter += 1
    print('-' * 60)

    for _ in range(5):
        t3 = Tree(tree_type_all.peach_tree)
        t3.render(rnd.randint(age_min, age_max),
                  rnd.randint(point_min, point_max),
                  rnd.randint(point_min, point_max))
        tree_counter += 1
    print('-' * 60)

    print('trees rendered: {}'.format(tree_counter))
    print('tree actually created: {}'.format(len(Tree.pool)))

    t4 = Tree(tree_type_all.cherry_tree)
    t5 = Tree(tree_type_all.cherry_tree)
    t6 = Tree(tree_type_all.apple_tree)

    print('{} == {} ? {}'.format(id(t4), id(t5), id(t4) == id(t5)))
    print('{} == {} ? {}'.format(id(t5), id(t6), id(t5) == id(t6)))


if __name__ == '__main__':
    """
    Out:
    render a tree of type TreeType.apple_tree at (14, 45)
    render a tree of type TreeType.apple_tree at (27, 98)
    render a tree of type TreeType.apple_tree at (10, 82)
    render a tree of type TreeType.apple_tree at (28, 18)
    render a tree of type TreeType.apple_tree at (12, 46)
    render a tree of type TreeType.apple_tree at (27, 50)
    render a tree of type TreeType.apple_tree at (15, 72)
    render a tree of type TreeType.apple_tree at (11, 32)
    render a tree of type TreeType.apple_tree at (2, 52)
    render a tree of type TreeType.apple_tree at (1, 45)
    ------------------------------------------------------------
    render a tree of type TreeType.cherry_tree at (5, 73)
    render a tree of type TreeType.cherry_tree at (9, 70)
    render a tree of type TreeType.cherry_tree at (18, 77)
    ------------------------------------------------------------
    render a tree of type TreeType.peach_tree at (29, 47)
    render a tree of type TreeType.peach_tree at (10, 49)
    render a tree of type TreeType.peach_tree at (22, 47)
    render a tree of type TreeType.peach_tree at (14, 43)
    render a tree of type TreeType.peach_tree at (29, 87)
    ------------------------------------------------------------
    trees rendered: 18
    tree actually created: 3
    1788111989560 == 1788111989560 ? True
    1788111989560 == 1788112076248 ? False
    """
    main()
