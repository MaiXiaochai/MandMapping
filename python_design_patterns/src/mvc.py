# -*- coding: utf-8 -*-

# @File         : mvc.py
# @Project      : src
# @Time         : 2018/11/8 21:45
# @Site :       : https://github.com/MaiXiaochai
# @Author       : maixiaochai

"""
1、模型-视图-控制器模式(Model-View-Controller, MVC):
    是应用到面向对象编程的SoC原则。模式的名称来自用来切分软件应用的三个主要部分，即模型部分、视图部分和控制器部分。
    MVC被认为是一种架构模式而不是一种设计模式。前者的范畴更广。

2、关注点分离(Separation of Concerns, SoC)：
    背后的思想是将一个应用切分成不同的部分，每个部分解决一个单独的关注点。
    分层设计中的层次（数据访问层、业务逻辑层和表示层等）即是每个关注点的例子。
    使用SoC原则能简化软件应用的开发和维护。

3、MVC细分：
    1）模型是核心。
        代表着应用的信息本源，包含和管理（业务）逻辑、数据、状态以及应用的规则。

    2）视图是模型的可视化表现。
        视图的例子有计算机图形用户界面、计算机中断的文本输出、智能手机的应用图形界面、PDF文档、饼图和柱状图等。

    3）控制器是模型与视图之间的链接和粘附。
        模型与视图之间的所有通信都通过控制器进行。

4、MVC简单使用
    对于将初始屏幕渲染给用户之后使用MVC的应用，典型使用方式如下
        1）用户通过单击（键入、触摸等）某个按钮触发一个视图；
        2）视图把用户操作告知控制器；
        3）控制器处理用户输入，并与模型交互；
        4）模型执行所有必要的校验和状态改变，并通知控制器应该做什么；
        5）控制器按照模型给出的指令，指导视图适当地更新和显示输出。

5、控制器的重要性：
    1）无需修改模型就行使用多个视图的能力（甚至可以根据需要同时使用多个视图）；
    2）为了实现模型与其表现之间的解耦，每个视图通常都需要属于它的控制器。
        如果模型直接与特定的视图通信，我们将无法对同一个模型使用多个视图（或者至少无法以简洁模块化的方式实现）。

6、SoC原则实际例子
    1）若造一座房子，通常会请不同的专业人员来完成 安装管道和电路、粉刷房子的工作；
    2）在一个餐馆中，服务员接收点菜单并为顾客上菜，但是饭菜由厨师烹饪。

7、Django是一个MVC框架。但是它使用了不同的命名约定:
    +--------------------------+
     MVC             Django
    +--------------------------+
     Model           Model
     View            Template
     Controller      View
    +--------------------------+

    在Django中，
        1）视图描述哪些数据对用户可见。因此，Django把对应于一个特定URL的Python回调函数成为视图。
        2）'模板'用于吧内容与其展现分开，其描述的是用户看到数据的方式，而不是哪些数据可见。

8、MVC模式的优点：
    1）视图与模型的分离允许美工一心搞UI部分，程序员一心搞开发，不会相互干扰；
    2）由于视图与模型之间的松耦合，每个部分可以单独修改/扩展，不会相互影响。例如，添加一个新视图的成本很小，
        只要为其实现一个控制器就可以了；
    3）因为职责明晰，维护每个部分也简单。

9、如何检验自己MVC的正确性：
    1）如果 你的应用有GUI，那么它可以换肤吗？
        易于改变它的皮肤/外观以及给人的感受吗？
        可以为用户提供运行期间改变应用皮肤的能力吗？
        如果这做起来并不简单，那就意味着你的MVC实现在某些地方存在问题；

    2）如果你的应用没有GUI（例如，是一个终端应用），为其添加GUI支持有多难？
        如果添加GUI没什么用，那么是否易于添加视图从而以图表（饼图、柱状图等）或文档（PDF、电子表格等）形式展示结果？
        如果因此而做出的变更不小（小的变更时，在不变更模型的情况下，创建控制器并绑定到视图），那你的MVC实现就有些不对了。

    如果以上两个条件都满足，那么与未使用MVC模式的应用相比，你的应用会更灵活、更好维护。
"""

# ----------------------------------------------------------------------------------------------------------------
"""
程序实现：名人名言打印机
    用户输入一个数字，然后就能看到与这个数字相关的名人名言。名人名言存储在一个quotes元组中。这种数据通常是存储在数据库、文件或
    其它地方，只有模型能够直接访问它。
    
    模型极为简单，只有一个get_quote()方法，基于索引n从quotes元组中返回对应的名人名言（字符串）。注意，n可以<=0,
    因为这种索引方式在Python中是有效的。
"""

quotes = ('A man is not complete until he is married. Then he is finished.',
          'As I said before, I never repeat myself.',
          'Behind a successful man is an exhausted woman.',
          'Black holes really suck...',
          'Facts are stubborn things.')

"""
蹩脚的翻译：
    1）未婚男人不完整，已婚男人则彻底完蛋了。
    2）就像我以前说过的，我从不重复自己。
    3）每一个成功的男人身后都有一个 无私奉献（exhausted，疲惫的，耗尽的）的女人。
    4）黑洞真的很烂？
    5）纸包不住火。（stubborn 顽固的，固执；倔强的）
"""


class QuoteModel:
    def get_quote(self, n):
        try:
            value = quotes[n]

        except IndexError as err:
            value = 'Not found!'

        return value


class QuoteTerminalView:
    """
    Terminal 末端，终端机

    视图有三个方法，
    1）show()            在屏幕上输出一句名人名言(或者输出提示信息 Not found!)
    2）error()           在屏幕上输出一条错误消息
    3）select_quote()    读取用户的选择
    """

    def show(self, quote):
        print('And the qoute is : "{}"'.format(quote))

    def error(self, msg):
        print('Error: {}'.format(msg))

    def select_quote(self):
        return input('Which quote number would you like ro see? ')


class QuoteTerminalController:
    """
    控制器负责协调。
    __init__负责初始化模型和视图。
    run()方法校验用户提供的名言索引，然后从模型中获取名言，并返回给视图展示，如一下代码所示。
    """
    def __init__(self):
        self.model = QuoteModel()
        self.view = QuoteTerminalView()

    def run(self):
        n, valid_input = '', False

        while not valid_input:
            n = self.view.select_quote()

            try:
                n = int(n)
                valid_input = True

            except ValueError as err:
                self.view.error("Incorrect index '{}'".format(n))

        quote = self.model.get_quote(n)
        self.view.show(quote)


def main():
    """
    Out:
    Which quote number would you like ro see? 1
    And the qoute is : "As I said before, I never repeat myself."
    Which quote number would you like ro see? 2
    And the qoute is : "Behind a successful man is an exhausted woman."
    Which quote number would you like ro see? 3
    And the qoute is : "Black holes really suck..."
    Which quote number would you like ro see? 4
    And the qoute is : "Facts are stubborn things."
    Which quote number would you like ro see? 5
    And the qoute is : "Not found!"
    Which quote number would you like ro see? 6
    And the qoute is : "Not found!"
    Which quote number would you like ro see? 0
    And the qoute is : "A man is not complete until he is married. Then he is finished."
    Which quote number would you like ro see?
    """
    controller = QuoteTerminalController()
    while True:
        controller.run()


if __name__ == '__main__':
    main()
