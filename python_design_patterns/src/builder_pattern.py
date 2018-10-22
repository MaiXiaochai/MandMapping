# -*- coding: utf-8 -*-

# @File         : builder_pattern.py
# @Project      : MindMapping
# @Time         : 2018/10/3 23:53
# @Author       : maixiaochai

import time
from enum import Enum

# 建造者模式：
# 将一个复杂对象的建造过程与其表现分离，这样，同一个构造过程可用于创建多个不同的表现。
# 使用特征：一个对象必须经过多个步骤来创建，并且要求同一个构造过程可以产生不同的表现。

# 现实例子：
# 比如说快餐店使用的是建造者设计模式
# 即使存在多种汉堡包（经典款、奶油汉堡包等）和不同包装（小盒子、中等盒子等），
# 准备一个汉堡包及打包（盒子或纸袋）的流程都是相同的。
# 经典汉堡和奶油汉堡的区别在于表现，而不是制造过程。
# 指挥者是出纳员，将需要准备什么餐品的指定传达给工作人员，
# 建造者是工作人员中的个体，关注具体的顺序。

# 有些资料指出，建造者模式可以解决可伸缩性构造函数问题。
# 在pytho中并不存在这个问题，因为可以用以下方式解决：
#   1)使用命名参数；
#   2)使用实参列表展开
# 解决这一问题，可以用工厂模式或者建造者模式。

# 工厂模式和建造者模式的区分
# 用买电脑为例

# 如买一台最新的苹果1.4GHz Mac mini，则是在使用工厂模式，
# 所有的硬件规格都已由制造商预先确定，制造商不用向你咨询就知道自己该做什么。
# 他们通常接收的是单条指令。


MINI14 = '1.4GHz Mac mini'


class AppleFactory:
    """
    这里嵌套了MacMini14类。这是禁止直接实例化(指的是在AppleFactory外部实例化MacMini14类)一个类的简洁方式。
    """
    class MacMini14:
        def __init__(self):
            self.memory = 4
            self.hdd = 500
            self.gpu = 'Intel HD Graphics 5000'

        def __str__(self):
            info = ('Model: {}'.format(MINI14),
                    'Memory: {}GB'.format(self.memory),
                    'Hard Disk: {}GB'.format(self.hdd),
                    'Graphics Card: {}'.format(self.gpu))

            return '\n'.join(info)

    def builder_computer(self, model):
        if model == MINI14:
            return self.MacMini14()

        else:
            print("I don't know how to build {}".format(model))

    """
    工厂模式测试代码
    afac = AppleFactory()
    mac_mini = afac.builder_computer(MINI14)
    print(mac_mini)
    
    Out:
    Model: 1.4GHz Mac mini
    Memory: 4GB
    Hard Disk: 500GB
    Graphics Card: Intel HD Graphics 5000
    """
# --------------------------------------------------------------------------------
# 选择购买一台定制的PC。使用的是建造者模式。
# 你是指挥者，向制造商（建造者）提供指令说明心中理想的电脑规格。


class Computer:
    def __init__(self, serial_number):
        self.serial = serial_number
        self.memory = None
        self.hdd = None
        self.gpu = None

    def __str__(self):
        info = ('Model: {}'.format(self.serial),
                'Memory: {}GB'.format(self.memory),
                'Hard Disk: {}GB'.format(self.hdd),
                'Graphics Card: {}'.format(self.gpu))

        return '\n'.join(info)


class ComputerBuilder:
    def __init__(self):
        self.computer = Computer('AG23385193')

    def configure_memory(self, amount):
        self.computer.memory = amount

    def configure_hdd(self, amount):
        self.computer.hdd = amount

    def configure_gpu(self, gpu_model):
        self.computer.gpu = gpu_model


class HardwareEngineer:
    def __init__(self):
        self.builder = None

    def construct_computer(self, memory, hdd, gpu):
        self.builder = ComputerBuilder()
        self.builder.configure_memory(memory),
        self.builder.configure_hdd(hdd),
        self.builder.configure_gpu(gpu)

    @property
    def computer(self):
        return self.builder.computer


def main():
    engineer = HardwareEngineer()
    engineer.construct_computer(hdd=500, memory=8, gpu='GeForce GTX 650 Ti')
    computer = engineer.computer
    print(computer)
    """
    Out:
    Model: AG23385193
    Memory: 8GB
    Hard Disk: 500GB
    Graphics Card: GeForce GTX 650 T
    """


# --------------------------------------------------------------------------------
# # 建造者应用：披萨订购应用
"""
准备好一个披萨，要经过遵从特定顺序的许多步骤。
要添加调味料，得先准备生面团，
要添加配料，得先添加调味料，
要烤披萨，得添加了调味料和配料，
要烤好，得取决于生面团的厚度和配料。
生面团 -> 调味料 -> 配料 -> 烤（厚度，配料） 
"""

# 声明一些Enum参数
PizzaProgress = Enum('PizzaProgress', 'queued preparation baking ready')

# dough 生面团； thin 薄的； thick 厚的
PizzaDough = Enum('PizzaDough', 'thin thick')

# sauce 沙司，酱汁， 给 ... 调味； tomato 番茄；potato 土豆； creme fraiche 鲜奶油
PizzaSauce = Enum('PizzaSauce', 'tomato creme_fraiche')

# topping 蛋糕上的装饰配料； mozarella 奶酪，干酪； bacon 培根，熏肉； ham 火腿； mushroom 蘑菇；red onion 红皮洋葱；
# oregano 牛至叶，止痢草、土香薷、小叶薄荷
PizzaTopping = Enum('PizzaTopping', 'mozzarella double_mozzarella bacon ham mushroom red_onion oregano')

# 各个步骤间的延迟
STEP_DELAY = 3


class Pizza:
    """
    最终的产品是一个披萨，由Pizza类描述，若使用建造者模式，则最终产品（类）并没有多少职责，因为他不支持直接实例化。
    建造者会直接创建一个最终产品的实例，并确保这个实例万全准备好。这就是Pizza类这么小的缘由。它只是将所有数据初始化为合理的默认值，
    唯一的例外方法是prepare_dough。将该方法定义在Pizza类而不是建造者中，是考虑到以下两点：
        1）为了澄清一点，就是虽然最终产品类通常会最小化，但这并不意味着绝不应该给它分配任何职责；
        2）为了通过组合提高代码复用。
    """
    def __init__(self, name):
        self.name = name
        self.dough = None
        self.sauce = None
        self.topping = []

    def __str__(self):
        return self.name

    def prepare_dough(self, dough):
        self.dough = dough
        print('preparing the {} dough of your {} ...'.format(self.dough.name, self))
        time.sleep(STEP_DELAY)
        print('done with the {} dough'.format(self.dough.name))


"""
两个建造者，一个制作玛格丽特披萨（MargaritaBuilder）,另一个制作奶油熏肉披萨（CreamyBaconBuilder）。
每个建造者都创建一个Pizza实例，并包含遵从披萨制作流程的方法：prepare_dough()、add_sauce、add_topping()和bake()。
准确说，其中的prepare_dough只是对Pizza类中prepare_dough()方法的一层封装。注意每个建造者是如何处理所有披萨相关细节的。
"""


class MargaritaBuilder:
    """
    玛格丽特披萨
    生面团：薄
    调味料：番茄酱
    配料：双层马苏里拉奶酪（mozzarella）、牛至
    烘焙：5s

    """
    def __init__(self):
        self.pizza = Pizza('margarita')
        self.progress = PizzaProgress.queued
        self.baking_time = 5

    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thin)

    def add_sauce(self):
        print('adding the tomato sauce to your matgarita ...')
        time.sleep(STEP_DELAY)
        print('done with the tomato sauce')

    def add_topping(self):
        print('adding the topping (double mozzarella, oregano) to your margarita')
        self.pizza.topping.append([i for i in (PizzaTopping.double_mozzarella, PizzaTopping.oregano)])
        time.sleep(STEP_DELAY)
        print('done with the topping (double mozzarella, oregano)')

    def bake(self):
        self.progress = PizzaProgress.baking
        print('baking your margarita for {} seconds'.format(self.baking_time))
        time.sleep(self.baking_time)


class CreamyBaconBuilder:
    def __init__(self):
        self.pizza = Pizza('Creamy bacon')
        self.progress = PizzaProgress.queued
        self.baking_time = 7

    def prepare_dough(self):
        pass
        # to be continued ...


if __name__ == '__main__':
    pass
