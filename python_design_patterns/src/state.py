#!/usr/bin/python
# -*- coding: utf-8 -*-

# @File    : state.py
# @Time    : 2019/3/26 22:17
# @Author  : MaiXiaochai
# @Site    : https://github.com/MaiXiaochai

"""
state：状态设计模式
1) 有限状态机，通常名为状态机是一种非常方便的状态转换建模（并在必要时以数学方式形式化）工具,
2) 状态机：是一个抽象机器，有两个关键部分，状态 和 转换。
        状态：系统当前的激活状态。
            比如一个收音机，其有两种可能的状态，一种是在调频波段（FM）或者调幅波段（AM）上调节；
            另一种状态是从一个 FM/AM无线电台切换到另一个。
        转换：从一个状态切换到另一个状态，因某个时间或条件的触发而开始。

3) 状态机的一个特性： 可以用状态图来表现。每个状态都是一个节点，每个转换都是两个节点之间的边。
4) 一个状态机在一个特定的时间点只能有一个激活状态。
5)状态机可以解决的问题：
    > 自动售货机
    > 电梯
    > 交通灯
    > 暗码锁
    > 停车计时器
    > 自动加油泵
    > 自然语言文法描述
    > 编程语言解析

6)零食自动售货机的可能状态：
    > 拒绝我们的选择，因为请求的货物已售罄
    > 拒绝我们的选择，因为放入的钱币不足
    > 递送货物，且不找零，因为放入的钱币恰好足够
    > 递送货物，并找零

7) 专有词条：状态机编译器(State Machine Compiler, SMC)，你可以用一种简单的领域特定语言在文本文件中描述你的状态机，
            SMC会自动生成状态机的代码。

8) 状态设计模式解决的是一定上下文中无限数量状态的完全封装，从而实现更好的可维护性和灵活性。

9) 状态设计模式通常使用一个父State类和许多派生的ConcreteState(具体状态类)类来实现，父类包括所有状态共同的功能，
    每个派生类则仅包含特定状态要求的功能。

10) 这里我们用 Python 的第三方库 state_machine 来说明状态设计模式。
"""

# 完成一个简单的操作系统的进程的状态机
from state_machine import acts_as_state_machine, State, Event, before, after, InvalidStateTransition


@acts_as_state_machine
class Process:
    # 定义状态机的状态和初始状态
    # 初始状态用inital=True
    create = State(inital=True)
    waiting = State()
    running = State()
    terminated = State()
    blocked = State()
    swapped_out_waiting = State()
    swapped_out_blocked = State()

    # 定义状态转换。在state_machine中一个状态转换就是一个Event。
    # 我们使用参数from_states和to_state来定义一个可能的转换。
    # from_states可以是单个状态或一组状态（元祖）。
    wait = Event(from_states=(create, running, blocked, swapped_out_waiting), to_state=waiting)
    run = Event(from_states=waiting, to_state=running)
    terminate = Event(from_states=running, to_state=terminated)
    block = Event(from_states=(running, swapped_out_blocked), to_state=blocked)
    swap_wait = Event(from_states=waiting, to_state=swapped_out_waiting)
    swap_block = Event(from_states=blocked, to_state=swapped_out_blocked)

    # 每个进程都有一个名称。正式的场景中，一个进程需要很多信息才能发挥其作用（ID、优先级和装态等），这里我们进行了简化
    def __init__(self, name):
        self.name = name

    # 在发生状态转换时，如果什么影响都没有，那转换就没什么作用了
    # @before 和 @after用于在状态转换之前或之后执行动作。
    # 这里的动作限于输出进程状态转换的信息

    @after('wait')
    def wait_info(self):
        print("{} entered waiting mode".format(self.name))

    @after('run')
    def wait_info(self):
        print("{} is running".format(self.name))

    @before('terminate')
    def wait_info(self):
        print("{} terimated".format(self.name))

    @after('block')
    def wait_info(self):
        print("{} is blocked".format(self.name))

    @after('swap_wait')
    def wait_info(self):
        print("{} is wapped out and waiting".format(self.name))

    @after('swap_block')
    def wait_info(self):
        print("{} is swapped out and blocked".format(self.name))


def transition(process, event, event_name):
    """
    在尝试执行event时，如果发生错误，则会输出事件的名称
    """
    try:
        event()
    except InvalidStateTransition as err:
        print("Error: transition of {} from {} to {} failed".format(process.name, process.current_state, event_name))


def state_info(process):
    pass
