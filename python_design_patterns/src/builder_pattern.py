# -*- coding: utf-8 -*-

# @File         : builder_pattern.py
# @Project      : MindMapping
# @Time         : 2018/10/3 23:53
# @Author       : maixiaochai

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


if __name__ == '__main__':
    # 工厂模式测试代码
    # afac = AppleFactory()
    # mac_mini = afac.builder_computer(MINI14)
    # print(mac_mini)
    pass
    main()


