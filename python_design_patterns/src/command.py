# -*- coding: utf-8 -*-

# @File         : command.py
# @Project      : src
# @Time         : 2018/12/17 22:54
# @Site         : https://github.com/MaiXiaochai
# @Author       : maixiaochai

import os


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

"""
使用命令模式实现最基本的文件操作工具：
    1）创建一个文件，并随意写入一个字符串；
    2）读取一个文件的内容；
    3）重命名一个文件；
    4）删除一个文件。
    
我们并不从头实现这些工具程序，因为python在os模块中已经提供了良好的实现。我们想做的是在已有实现之上添加一个额外的抽象层，
这样可以当做命令来使用。这样，我们就能获得命令提供的所有优势。
    
相关规划：
    创建文件    ———— 支持撤销
    读取文件    ———— 不支持撤销
    重命名文件  ———— 支持撤销
    删除文件    ———— 不支持撤销
"""

verbose = True


class RenameFile:
    def __init__(self, path_src, path_dest):
        self.src, self.dest = path_src, path_dest

    def execute(self):
        # verbose(冗长的)，全局标记，被激活时（默认是被激活的），能向用户反馈执行的操作。
        if verbose:
            print("[renaming '{}' to '{}']".format(self.src, self.dest))
        os.rename(self.src, self.dest)

    def undo(self):
        if verbose:
            print("[ renaming '{}' back to '{}']".format(self.dest, self.src))
        os.rename(self.dest, self.src)


def delete_file(path):
    """
    不一定要为想要添加的每个命令（之后会涉及很多）都创建一个新类
    :param path:    str     文件路径
    :return:
    """
    if verbose:
        print("[ deleting file '{}']".format(path))
    os.remove(path)


class CreateFile:
    def __init__(self, path, txt='hello world\n'):
        self.path, self.txt = path, txt

    def execute(self):
        if verbose:
            print("[Creating file '{}']".format(self.path))

        with open(self.path, mode='w', encoding='utf8') as out_file:
            out_file.write(self.txt)

    def undo(self):
        delete_file(self.path)


class ReadFile:
    def __init__(self, path):
        self.path = path

    def execute(self):
        if verbose:
            print("[Reading file '{}']".format(self.path))
        with open(self.path, 'r', encoding='utf8') as in_file:
            print(in_file.read(), '')


def main():
    orig_name, new_name = 'file1', 'file2'
    commands = []

    # 批量实例化
    for cmd in CreateFile(orig_name), ReadFile(orig_name), RenameFile(orig_name, new_name):
        commands.append(cmd)

    [c.execute() for c in commands]

    # 询问用户是否撤销，若撤销，则执行commands列表中所有命令的undo(),注意，这里并不是所有命令都有撤销命令
    answer = input('reverse the executed commands? [y/n] ')

    if answer not in 'Yy':
        print("the result is {}".format(new_name))
        exit()

    for c in reversed(commands):
        try:
            c.undo()
        except Exception as e:
            pass


if __name__ == '__main__':
    """
    Out:
    [Creating file 'file1']
    [Reading file 'file1']
    hello world
     
    [renaming 'file1' to 'file2']
    reverse the executed commands? [y/n] y
    [ renaming 'file2' back to 'file1']
    [ deleting file 'file1']
    """
    main()
