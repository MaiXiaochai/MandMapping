# -*- coding: utf-8 -*-

# @File         : facade.py
# @Project      : src
# @Time         : 2018/11/1 22:25
# @Site :       : https://github.com/MaiXiaochai
# @Author       : maixiaochai

from enum import Enum
from abc import ABCMeta, abstractmethod

"""
外观模式(Facade)：在已有复杂系统之上实现的一个抽象层。是对内部系统的一个封装。
作用：     隐藏系统内部的复杂性，通过一个接口向客户端暴露必要的部分。
使用时机： 为一个复杂系统提供单个简单的入口点。
使用效果： 客户端通过简单地调用一个方法/函数就能使用一个系统。


生活中的例子：

1）当你致电一个银行或者公司，通常是先被连线到客服部门，
    客服职员在你和业务部门（结算、技术支持、一般援助等）及帮你解决具体问题的职员之间充当一个外观角色。

2）汽车或者摩托车的启动钥匙视为一个外观。外观是激活一个系统的便捷方式，系统的内部则非常复杂。
    其它可以通过一个简单按钮就能激活的复杂电子设备，同样可以如此看待。
"""


# --------------------------------------------------------------------------------------------
"""
其实这段我也不是很懂，abc模块和abstractmethod修饰器第一次接触。
这里用一个系统(如Linux系统等)的运行过程为例来讲解的外观模式。

我们从Server接口开始实现，使用一个Enum类型变量来描述一个服务进程的不同状态，
使用abc模块来禁止对Server接口的直接进行初始化，并强制子类实现关键的boot()和kill()方法。
这里假设每个服务进程的启动、关闭及重启都相应地需要不同的动作。注意一下几点：
    1）我们需要使用metaclass关键字来继承ABCMeta。
    2）使用@abstractmethod修饰器来声明Server的所有子类都应（强制性地）实现那些方法。
"""


State = Enum('State', 'new running sleeping restart zombie')


class Server(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return self.name

    @abstractmethod
    def boot(self):
        pass

    @abstractmethod
    def kill(self, restart=True):
        pass


"""
一个模块化的操作系统可以有很多有意思的服务进程，包括文件服务进程、进程服务进程、身份验证进程、网络服务进程和图形/窗口服务进程等。
下面的例子包含两个存个服务进程（FileServer和ProcessServer）,除了Server接口要求实现的方法之外，每个服务进程还可以有自己特定的方法。
如，FileServer有一个create_file()方法用于创建文件，ProcessServer有一个create_process()方法用于创建进程。
"""


class FileServer(Server):
    def __init__(self):
        """
        初始化文件服务进程要求的操作
        """
        self.name = 'FileServer'
        self.state = State.new

    def boot(self):
        """
        启动文件服务进程要求的操作
        :return:
        """
        print('booting the {}'.format(self))
        self.state = State.running

    def kill(self, restart=True):
        """
        终止文件服务进程要求的操作
        """
        print('Killing {}'.format(self))
        self.state = State.restart if restart else State.zombie

    def create_file(self, user, name, permissions):
        """
        检查访问权限的有效性和用户权限等
        """
        print("trying to crate the file '{}' for user '{}' with permissions {}".format(name, user, permissions))


class ProcessServer(Server):
    def __init__(self):
        """
        初始化进程服务进程要求的操作
        """

        self.name = 'ProcessServer'
        self.state = State.new

    def boot(self):
        """
        启动进程服务进程要求的操作
        """
        print('booting the {}'.format(self))
        self.state = State.running

    def kill(self, restart=True):
        """
        终止进程服务要求的操作
        """
        print('Killing {}'.format(self))
        self.state = State.restart if restart else State.zombie

    def create_process(self, user, name):
        """
        检查用户权限和生成PID等
        """
        print("trying to create the process '{}' for user {}".format(name, user))


class OperatingSystem:
    """
    该类是一个外观。
    __init__中创建所有需要的服务进程实例。
    start()方法是系统的入口点，供客户端代码使用。如果需要，可以添加更多的包装方法作为服务的访问点，
    比如包装方法create_file()和create_process()。

    从客户端的角度来看，所有服务都是由OperatingSystem类提供的。客户端并不应该被不必要的细节所干扰。
    比如，服务进程的存在和每个服务进程的责任。
    """
    def __init__(self):
        self.fs = FileServer()
        self.ps = ProcessServer()

    def start(self):
        [i.boot() for i in (self.fs, self.ps)]

    def create_file(self, user, name, permissions):
        return self.fs.create_file(user, name, permissions)

    def create_process(self, user, name):
        return self.ps.create_process(user, name)


def main():
    """
    Out:
    booting the FileServer
    booting the ProcessServer
    trying to crate the file 'hello' for user 'foo' with permissions -rw-r-r
    trying to create the process 'ls /tmp' for user bar
    """
    os = OperatingSystem()
    os.start()
    os.create_file('foo', 'hello', '-rw-r-r')
    os.create_process('bar', 'ls /tmp')


if __name__ == "__main__":
    main()
