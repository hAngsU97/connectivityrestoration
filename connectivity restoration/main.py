from Node import *
from Distribute import *
from Plot import *
from Recovery import *

if __name__ == '__main__':
    # 实验条件设置
    n, r = 12, 100
    width, length = 350, 350

    # 开始！
    nodes = Nodes(n)
    distribute = Distribute(nodes, width, length)
    plot = Plot(distribute, r)

    # 初始分布
    # distribute.random_dis()
    distribute.connect_dis()
    # distribute.certain_dis()
    coverage_before = distribute.coverage()
    print("coverage_before: {}".format(coverage_before))
    nodes.config()
    plot.draw()

    # 虚拟力初始分布
    # distribute.VF_dis()
    # nodes.config()
    # plot.draw()

    # 单点失联
    recovery = Recovery(nodes)
    x = distribute.loss1node()
    nodes.config()
    plot.draw()
    connect = nodes.isAllConnected_except1(x)
    print(connect)

    # 恢复策略
    distance, num = 0, 0
    res_DARA = recovery.DARA(x)
    if res_DARA != 0:
        distance, num = res_DARA[0], res_DARA[1]
    print("distance: {}, num: {}".format(distance, num))
    coverage_after = distribute.coverage()
    print("coverage_after: {}".format(coverage_after))
    nodes.config()
    plot.draw()
