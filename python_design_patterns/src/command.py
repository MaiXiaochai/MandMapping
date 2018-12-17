# -*- coding: utf-8 -*-

# @File         : command.py
# @Project      : src
# @Time         : 2018/12/17 22:54
# @Site         : https://github.com/MaiXiaochai
# @Author       : maixiaochai


"""
命令设计模式（command）:帮助我们将一个操作（撤销、重做、复制、粘贴等）封装成一个对象。
简而言之，这意味着创建一个类，包括实现该操作所需要的所有逻辑和方法。
优点：
    1）我们不需要直接执行一个命令。命令可以按照希望执行。
    2）调用命令的对象与知道如何执行命令的对象解耦。调用者无需知道命令的任何实现细节。
    3）如果有意义，可以把多个命令组织起来，这样调用者能够按照顺序执行它们。（在实行一个多层撤销命令时，这是很有用的）

比如，当我们去餐馆吃饭时候，服务员用来记录的账单就是命令模式的一个例子。

命令模式能完成的：
    1）杀手级特性：撤销操作；
    2）GUI按钮和菜单项；
    3）其他操作，剪切、复制、粘贴、重做和文本大写；
    4）事务型行为和日志记录，这对于为变更而记录一份持久化日志是很重要的。操作系统用它来从系统崩溃中恢复，
        关系型数据库用它来实现事务，文件系统用它来实现快照，而安装程序（向导程序）用它来恢复取消的安装。
    5）宏：一个动作序列，可在任意时间点按照要求进行录制和执行。编辑器Emacs和Vim都支持宏。
"""
