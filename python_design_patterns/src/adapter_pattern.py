# -*- coding: utf-8 -*-

# @File         : adapter_pattern.py
# @Project      : MindMapping
# @Time         : 2018/10/24 23:45
# @Site :       : https://github.com/MaiXiaochai
# @Author       : maixiaochai

"""
适配器模式：在两个接口外使得两个接口能正常通信的代码层。
            遵从开放/封闭原则(open/close principle)。

开放/封闭原则： 一个软件实体应该对扩展是开放的，对修改是封闭的。

应用场景：某个产品制造出来后，需要应对新的需求之时，如果希望其仍然有效，则可以使用适配器模式,原因：
            1）不要求访问他方接口的源代码；
            2）不要违反开放/封闭原则。
"""

# ----------------------------------------------------------------------------------------
# 客户端仅知道如何调用execute()方法，并不知道play()和speak()。在不改变Synthesizer和Human类的前提下，
# 我们改如何做才能让代码有效？适配器是救星。我们创建一个通用的adapter类，将一些带不同接口的对象适配到一个统一接口中。


class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} computer'.format(self.name)

    def execute(self):
        return 'executes a program'


class Synthesizer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} computer'.format(self.name)

    def play(self):
        return 'is playing an electronic song'


class Human:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '{} the human'.format(self.name)

    def speak(self):
        return 'says hello'


class Adapter:
    def __init__(self, obj, adapted_methods):
        """
        :param obj:                     我们想要适配的对象
        :param adapted_methods: dict    键：客户端要调用的方法， 值：被调用的方法
        """
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __str__(self):
        return str(self.obj)


def main():
    """
    列表objects容纳着所有对象。属于Computer类的可兼容对象不需要适配。
    可以直接把它们添加到列表中。不兼容的对象则不能直接添加。使用Adapter类来适配它们。
    结果是，对于所有对象，客户端代码都可以始终调用已知的execute()方法，而无需关心被使用的类之间的任何接口差异。

    对本例的解释：
    对于客户端而言，它只会调用 obj.execute()方法，因为它只知道execute()方法。而符合这一条件的对象只有Computer类，
    即执行Computer.execute()是可以正常运行的。而执行Synthesizer.execute()或者Human.execute()会报错，因为这两个类
    没有execute()方法。所以，要用适配器模式适配一下。

    __dict__ 是类中的字典，包含着着 方法名：方法对象 的键值对儿。
    在main()函数中，将所有execute应该指向的方法，在其对应的类的__dict__中，将key都改为了'execute'。
    :return:
    """

    objects = [Computer('Asus')]
    synth = Synthesizer('moog')
    objects.append(Adapter(synth, dict(execute=synth.play)))
    human = Human('Bob')
    objects.append(Adapter(human, dict(execute=human.speak)))

    for i in objects:
        print('{} {}'.format(str(i), i.execute()))


if __name__ == '__main__':
    """
    Out:
        the Asus computer executes a program
        the moog computer is playing an electronic song
        Bob the human says hello
    """
    main()
