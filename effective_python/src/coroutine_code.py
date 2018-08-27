# -*- coding: utf-8 -*-


def minimize():
    """
    每次输入数据后，返回历史输入中最小的值。
    """
    # 该yield后没有跟随其它内容，表示把外界传来的首个值当做目前的最小值。
    # 此后，生成器会屡次执行while循环中的那条yield语句，以便将当前统计到的最小值高速外界。
    current = yield
    while True:
        value = yield current
        current = min(value, current)
    

if __name__ == '__main__':
    lis = [10, 4, 22, -1]
    it = minimize()

    # 在send方法前调用一次next()，以便将生成器表达式推进到第一条yield表达式那里。
    next(it)
    for i in lis:
        print("input: {} | out: {}".format(i, it.send(i)))


# out:
# input: 10 | out: 10
# input: 4 | out: 4
# input: 22 | out: 4
# input: -1 | out: -1