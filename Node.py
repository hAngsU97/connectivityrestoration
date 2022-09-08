import math
import numpy as np


class Node:
    def __init__(self, id, x=0, y=0, r=100):
        self.id = 0
        self.x = x
        self.y = y
        self.r = r
        self.loss = False
        self.rim_rank = 0
        self.rim_neighbour_position = []
        self.rim_inform_flag = False
        self.rim_finished = False
        self.neighbours = []
        self.NN = None
        self.connected_neighbours = []
        self.last_neighbours = []
        self.connected_NN = None
        self.degree = 0

    def findNeighbours(self, nodes):
        self.neighbours = []
        for node in nodes:
            if not (node.x == self.x and node.y == self.y):
                if (node.x - self.x) ** 2 + (node.y - self.y) ** 2 <= self.r ** 2:
                    self.neighbours.append(node)

    def findConnectedNeighbours(self, nodes):
        self.connected_neighbours = []
        if not self.loss:  # 丢失节点没有相连接的邻居
            for node in self.neighbours:
                if not node.loss:
                    self.connected_neighbours.append(node)

    def findNN(self):  # 找到物理上的最近邻居
        dis_min = float('inf')
        for nei in self.neighbours:
            dis_tmp = math.sqrt((nei.x - self.x) ** 2 + (nei.y - self.y) ** 2)
            if dis_min > dis_tmp:
                dis_min = dis_tmp
                self.NN = nei
        return self.NN, dis_min

    def findConnectedNN(self):  # 找到相连的最近邻居
        dis_min = float('inf')
        for nei in self.connected_neighbours:
            dis_tmp = math.sqrt((nei.x - self.x) ** 2 + (nei.y - self.y) ** 2)
            if dis_min > dis_tmp:
                dis_min = dis_tmp
                self.connected_NN = nei
        return self.connected_NN, dis_min

    def calculate_degree(self):
        self.degree = len(self.neighbours)

    def locate(self, x, y):
        self.x = x
        self.y = y

    def rim(self):
        if self.rim_finished:
            return 0
        distance, destination = 0, (0,0)
        if self.rim_rank == 1:
            distance, destination = self.FirstRankMove()   # 第一级别移动，及最靠近失联节点的节点移动到距失联处r/2的地方
        elif self.rim_rank > 1:     # 后续移动
            distance, destination = self.RestRankMove()  # 准备移动，计算方向
        if distance > 0:    # 判断是否移动
            self.rim_inform(destination)  # 告诉后续节点需要移动
        self.rim_finished = True  # 移动结束标记
        return distance

    def rim_inform(self,destination):   # 需要移动时通知其他节点
        if not self.rim_inform_flag:
            for node in self.connected_neighbours:
                if node.rim_rank == 0 or node.rim_rank > self.rim_rank + 1: # 简化通知信息，若发送的通知等级高于已经收到的通知，则直接省略
                    node.rim_rank = self.rim_rank + 1
                    node.rim_neighbour_position.append((destination, self.rim_rank,self.id))
            self.rim_inform_flag = True

    def FirstRankMove(self):
        dis_tmp = math.sqrt((self.rim_neighbour_position[0][0] - self.x) ** 2 + (self.rim_neighbour_position[0][1]
                                                                                 - self.y) ** 2) - self.r / 2
        theta = math.atan((self.rim_neighbour_position[0][1] - self.y) /
                          (self.rim_neighbour_position[0][0] - self.x))
        if dis_tmp > 0:
            self.locate(self.x + dis_tmp * math.cos(theta), self.y + dis_tmp * math.sin(theta))  # 移动节点
        destination = (self.x + dis_tmp * math.cos(theta),self.y + dis_tmp * math.sin(theta))
        return dis_tmp,destination  # 记录移动距离参数

    def RestRankMove(self):  # 移动前的准备，计算移动方向
        def rank(element):
            return element[2]
        theta, num, distance, destination = 0, 0, 0, (0, 0)
        self.rim_neighbour_position.sort(key=rank)
        rank = self.rim_neighbour_position[1]
        for pos in self.rim_neighbour_position:  # 记录通知节点的方向
            if pos[1] <= rank:  # 只计算最高优先级的通知
                theta += math.atan((pos[0][1] - self.y) / (pos[0][0] - self.x))
                num += 1
            else:
                break
        self.locate()
        return distance, destination


class Nodes:
    def __init__(self, num=10):
        self.nodes = [Node(i) for i in range(num)]

    def config(self):
        for node in self.nodes:
            node.findNeighbours(self.nodes)
            node.findConnectedNeighbours(self.nodes)
            node.findNN()
            node.findConnectedNN()

    def parameters_calculate(self):
        for node in self.nodes:
            node.calculate_degree()

    def isAllConnected(self):
        matrix = [[0] * len(self.nodes) for _ in range(len(self.nodes))]
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if self.nodes[j] in self.nodes[i].connected_neighbours:
                    matrix[i][j] = 1
        matrix = np.array(matrix)
        # print(matrix)
        value = matrix
        sum = matrix
        for i in range(1, len(self.nodes)):
            value = np.matmul(value, matrix)
            sum += value
        reachability_matrix = sum != 0
        final = reachability_matrix.astype(int)
        # print(final)
        return final

    def isAllConnected_except1(self, loss):
        # 输入连接关系
        matrix = [[0] * (len(self.nodes)) for _ in range(len(self.nodes))]
        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if self.nodes[j] in self.nodes[i].connected_neighbours:
                    matrix[i][j] = 1
        # 数组转化为np中的矩阵
        matrix = np.array(matrix)
        # print(matrix)
        # 删除矩阵中的空行，忽略已经失联的一个节点
        matrix = np.delete(matrix, loss, axis=0)
        matrix = np.delete(matrix, loss, axis=1)
        # print(matrix)
        # 计算连接矩阵的高次和
        value = matrix
        sum = matrix
        for i in range(1, len(self.nodes)):
            value = np.matmul(value, matrix)
            sum += value
        # 矩阵数字过大转化为布尔型
        reachability_matrix = sum != 0
        # 用astype函数转化为int型
        final = reachability_matrix.astype(int)
        # print(final)
        return True if 0 not in final else False
