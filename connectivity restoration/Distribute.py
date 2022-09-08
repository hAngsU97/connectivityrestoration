import math
import random


class Distribute:   # 功能：几种初始分布、随机丢失节点、覆盖率测试
    def __init__(self, Nodes, width, length):
        self.nodes = Nodes.nodes
        self.width = width
        self.length = length

    def random_dis(self):  # 完全随机分布初始拓扑
        for node in self.nodes:
            x = random.randint(0, self.length)
            y = random.randint(0, self.width)
            node.locate(x, y)

    def connect_dis(self):  # 全连接初始拓扑
        # 第一个节点随即布置
        x = random.randint(0, self.length)
        y = random.randint(0, self.width)
        # 对之后的每一个节点，在前一个节点基础上增加一个小于r的距离进行部署
        for node in self.nodes:
            node.locate(x, y)
            r = random.uniform(node.r * 0.6, node.r)
            theta = random.uniform(0, 2 * math.pi)
            x_tmp = x + r * math.cos(theta)
            y_tmp = y + r * math.sin(theta)
            if self.length >= x_tmp >= 0:
                x = x_tmp
            elif x_tmp > self.length:
                x = self.length
            else:
                x = 0

            if self.width >= y_tmp >= 0:
                y = y_tmp
            elif y_tmp > self.width:
                y = self.width
            else:
                y = 0

    def VF_dis(self):  # 虚拟力分布初始拓扑
        r = self.nodes[0].r
        for _ in range(50):
            for node in self.nodes:
                fx, fy = 0, 0
                for nei in node.neighbours:
                    dx = node.x - nei.x
                    dy = node.y - nei.y
                    if abs(dx) < r * 0.2:
                        fx += 0.2 * dx
                    elif dx > r * 0.8:
                        fx -= 0.05 * dx
                    if abs(dy) < r * 0.2:
                        fy += 0.2 * dy
                    elif dx > r * 0.8:
                        fy -= 0.05 * dy
                node.x += fx
                node.y += fy

    def certain_dis(self):  # 人为规定的初始分布，简单，用于测试
        x, y = 0, 0
        for i in range(len(self.nodes)):
            self.nodes[i].locate(x, y)
            x += 60
            y += 20
        return 0

    def coverage(self):  # 测试覆盖率
        count = 0
        # 对每个格点测试是否有一个正常节点能够覆盖
        for x in range(self.width):
            for y in range(self.length):
                for node in self.nodes:
                    if node.loss:  # 对丢失节点直接跳过
                        continue
                    if (node.x - x) ** 2 + (node.y - y) ** 2 < node.r ** 2:
                        count += 1
                        break
        return count / (self.width * self.length)

    def loss1node(self):  # 丢失一个节点
        x = random.randint(0, len(self.nodes) - 1)
        self.nodes[x].loss = True
        print("Node {}'s Neighbour(s) : {}".format(x, self.nodes[x].neighbours))
        print("Node {} is lost: {}".format(x, self.nodes[x].loss))
        return x

    def loss2node(self):    # 丢失两个节点
        x1 = random.randint(0, len(self.nodes))
        x2 = random.randint(0, len(self.nodes))
        if x1 != x2:
            self.nodes[x1].loss = True
            self.nodes[x2].loss = True
        else:
            self.nodes[x1].loss = True
            self.nodes[(x1 + 1) % len(self.nodes)].loss = True
