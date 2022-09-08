import math


class Recovery:  # 几种恢复策略：DARA、RIM
    def __init__(self, Nodes):
        self.nodes = Nodes.nodes
        self.Nodes = Nodes

    def DARA(self, x):
        # 一、如果剩余图形为全连接，则结束恢复过程
        if self.Nodes.isAllConnected_except1(x):
            return 0
        # 二、否则进行级联移动
        lost_node = self.nodes[x]
        print("lost node: {}".format(lost_node))
        distance, num = 0, 0
        # 找到最近邻居，最近邻居移动到失联节点处，node2move为当前的移动节点
        node2move = lost_node.NN  # 对于单节点失联，此处NN一定为正常运行的节点
        distance += math.sqrt((lost_node.x - node2move.x) ** 2 + (lost_node.y - node2move.y) ** 2)  # 记录移动距离参数
        num += 1  # 记录移动节点数参数
        node2move.locate(lost_node.x, lost_node.y)  # 移动节点
        while True:
            self.Nodes.config()
            if self.Nodes.isAllConnected_except1(x):  # 如果已是全连接，则结束移动
                break
            else:
                target = node2move  # target记录下次如果需要移动时，节点移动位置
                moved_node_neighbours = node2move.connected_neighbours  # 下一次可能移动的节点们
                if target in moved_node_neighbours:
                    moved_node_neighbours.remove(target)
                print("potential nodes to move in the next round:".format(moved_node_neighbours))
                # 找出正常且距离最近的节点作为移动节点node2move
                dis_min = float('inf')
                for nei in moved_node_neighbours:
                    dis_tmp = math.sqrt((nei.x - target.x) ** 2 + (nei.y - target.y) ** 2)
                    if dis_min > dis_tmp:
                        dis_min = dis_tmp
                        node2move = nei
                print("node to move: {}".format(node2move))
                # 评价参数：distance，num等
                distance += math.sqrt((node2move.x - target.x) ** 2 + (node2move.y - target.y) ** 2)
                num += 1
                node2move.locate(target.x, target.y)  # 节点移动
        return distance, num

    def RIM(self, x):
        distance, num = 0, 0

        return distance, num
