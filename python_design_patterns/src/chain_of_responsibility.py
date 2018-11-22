# -*- coding: utf-8 -*-

# @File         : chain_of_responsibility.py
# @Project      : src
# @Time         : 2018/11/21 22:41
# @Site :       : https://github.com/MaiXiaochai
# @Author       : maixiaochai

"""
责任链模式（Chain of Responsibility）: 通过责任链模式，我们能让许多不同对象来处理一个特定的请求。
                                        在我们预先不知道应该由哪个对象来处理某个请求时，这是有用的。

    如果所有请求都能被单个处理程序处理，责任链就没那么有用了，除非确实不知道会是哪个程序处理请求。这一模式的价值在于解耦。
    客户端仅需知道如何与链的起始节点（标头）进行通信。
    松耦合考虑的是简化维护，并让我们易于理解系统的工作原理。

    用于让多个对象来处理单个请求时，或者用于预先不知道应该由那个对象（来自某个对象链）来处理某个特定请求时。其原则如下
        1）存在一个对象链（链表、树链或任何其他便捷的数据结构）；
        2）我们一开始将请求发送给链中的第一个对象；
        3）对象决定其是否要处理该请求；
        4）对象将请求转发给下一个对象；
        5）重复该过程，直到到达链尾。

现实生活的例子
ATM机以及一般而言用于接收/返回钞票或硬币的任意机器（比如，零食自动贩卖机）都使用了责任链模式。
机器上总会有一个放置各种钞票的槽口，钞票放入之后，会被传递到恰当的容器。
钞票啊返回时，则是从恰当的容器中获取。我们可以把这个槽口视为共享通信媒介，不同的容器则是处理元素。
结果包含来自一个或多个容器的现金。


软件例子
Apache的 Cocoa和Touch框架使用责任链来处理事件。在某个视图接收到一个其并不知道如何处理的事件时，会将事件转发给超视图，
直到有个视图能够处理这个事件或者视图链接结束。


应用
采购系统，其中有许多核准权限。某个核准权限可能可以核准在一定额度之内的订单，比如有100元，如果订单超过了100美元，则会将订单发送给
链中的下一个核准权限，比如能够核准在200元以下的订单，等等。

另一个责任链场景，有多个对象都需要对同一请求进行处理时。这是基于事件的编程常有的事情。
单个事件，比如一次鼠标左击，可被多个事件监听者捕获。
"""

# ---------------------------------------------------------------------------------------------------------------------
# 实现简单的事件系统


class Event:
    """
    描述一个事件。为简化，案例中一个事件只有一个name属性。
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Widget:
    """
    应用的核心类
    每个控件都有一个到父对象的引用。我们嘉定副对象是一个Widget实例。根据继承规则，任何Widget子类的实例（如MsgText的实例）也是
    #Widget实例。

    handle()方法使用动态分发，通过hasattr()和getattr()决定一个特定请求（event）应该由谁来处理。
    如果被请求处理世间的控件并不支持该事件，则有两种回退机制。
    如果控件有parent,则执行parent的handle()方法。如果控件没有parent，但有handle_default()方法，则执行handle_default()。
    """
    def __init__(self, parent=None):
        self.parent = parent

    def handle(self, event):
        handler = 'handle_{}'.format(event)
        if hasattr(self, handler):
            method = getattr(self, handler)
            method(event)

        elif self.parent:
            self.parent.handle(event)

        elif hasattr(self, 'handle_default'):
            self.handle_default(event)


class MainWindow(Widget):
    """
    仅能处理close和default事件
    """
    def handle_close(self, event):
        print('MainWindow: {}'.format(event))

    def handle_default(self, event):
        print('MainWindow Default: {}'.format(event))


class SendDialog(Widget):
    def handle_paint(self, event):
        print('SendDialog: {}'.format(event))


class MsgText(Widget):
    """
    仅能处理down事件
    """
    def handle_down(self, event):
        print('MsgText: {}'.format(event))


def main():
    """
    如何创建控件和事件，以及控件如何对那些事件作出反应。
    所有事件都会被发送给所有控件。注意其中每个控件的父子关系。
    sd对象（SendDialog的一个实例）的父对象是mw（MainWindow的一个实例）。然而，并不是所有对象都需要一个MainWindow实例的父对象。
    例如，Msg对象（MsgText的一个实例）是以sd作为父对象。

    Out:
    -----------------------------------
    Sending event -down- to MainWindow
    MainWindow Default: down
    Sending event -down- to SendDialog
    MainWindow Default: down
    Sending event -down- to MsgText
    MsgText: down

    -----------------------------------
    Sending event -paint- to MainWindow
    MainWindow Default: paint
    Sending event -paint- to SendDialog
    SendDialog: paint
    Sending event -paint- to MsgText
    SendDialog: paint

    -----------------------------------
    Sending event -unhandled- to MainWindow
    MainWindow Default: unhandled
    Sending event -unhandled- to SendDialog
    MainWindow Default: unhandled
    Sending event -unhandled- to MsgText
    MainWindow Default: unhandled

    -----------------------------------
    Sending event -close- to MainWindow
    MainWindow: close
    Sending event -close- to SendDialog
    MainWindow: close
    Sending event -close- to MsgText
    MainWindow: close
    """
    mw = MainWindow()
    sd = SendDialog(mw)
    msg = MsgText(sd)

    for e in ('down', 'paint', 'unhandled', 'close'):
        evt = Event(e)
        print('-' * 35)
        print('Sending event -{}- to MainWindow'.format(evt))
        mw.handle(evt)
        print('Sending event -{}- to SendDialog'.format(evt))
        sd.handle(evt)
        print('Sending event -{}- to MsgText'.format(evt))
        msg.handle(evt)
        print()


if __name__ == '__main__':
    main()
