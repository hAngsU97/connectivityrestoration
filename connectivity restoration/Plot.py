import numpy as np
import matplotlib.pyplot as plt


class Plot:
    def __init__(self, distribute, r):
        self.nodes = distribute.nodes
        self.width = distribute.width
        self.length = distribute.length
        self.r = r

    def draw(self):
        fig, ax = plt.subplots()
        np.random.seed()

        # 点的形状和颜色
        rx, ry = 1., 1.
        area = rx * ry * np.pi * 20
        colors1 = '#DC143C'
        colors2 = '#00CED1'

        # 坐标轴配置
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        # ax.axis([-self.length * 0.12, self.length * 1.12, -self.width * 0.12, self.width * 1.12])
        ax.grid(linewidth=0.5, color="black", alpha=0.16)

        # 布点
        connected_p = []
        lost_p = []
        for node in self.nodes:
            if not node.loss:
                connected_p.append([node.x, node.y])
            else:
                lost_p.append([node.x, node.y])

        a = np.array(connected_p)
        b = np.array(lost_p)

        if len(connected_p) > 0:
            plt.scatter(a[:, 0].T, a[:, 1].T, s=area, c=colors2, alpha=0.4, label="Operating")
        if len(lost_p) > 0:
            plt.scatter(b[:, 0].T, b[:, 1].T, s=area, c=colors1, alpha=0.4, label="Down")

        plt.legend()

        # 连线
        for p in self.nodes:
            for q in p.connected_neighbours:
                if ((p.x - q.x) ** 2 + (p.y - q.y) ** 2) < self.r ** 2:
                    ax.plot([p.x, q.x], [p.y, q.y], color="#87CEEB")

        plt.show()
