import random
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from tqdm import tqdm


@dataclass
class Node:
    row: int
    col: int
    accessible: int  # 1 表示通，0 表示不通
    visited: int = 0  # 1 表示已访问，0 表示未访问


class Grid:
    """指定大小的网格，随机选择固定数量的节点设为通。"""

    def __init__(self, rows: int, cols: int, percent: float):
        if not 0 <= percent <= 100:
            raise ValueError("percent 必须在 0 到 100 之间")

        self.rows = rows
        self.cols = cols
        self.percent = percent

        # generate exact number of accessible nodes based on the percentage
        total = rows * cols
        # 四舍五入到整数个节点；位置随机，但通节点的数量和比例固定。
        self.open_count = round(total * percent / 100)
        cells = [1] * self.open_count + [0] * (total - self.open_count)
        random.shuffle(cells)  # in-place shuffle to randomize the cells

        self.nodes = [
            [Node(row, col, cells[row * cols + col]) for col in range(cols)]
            for row in range(rows)
        ]

    def node(self, row: int, col: int) -> Node:
        return self.nodes[row][col]

    def visitable(self, row: int, col: int) -> list[Node]:
        """返回上下左右相邻且可通的节点。"""
        result = []
        for dr, dc in ((1, 0), (-1, 0), (0, -1), (0, 1)):
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                neighbor = self.nodes[r][c]
                if neighbor.accessible == 1:
                    result.append(neighbor)
        return result


def grid_visit_test(grid: Grid) -> bool:
    """从第一行的可通节点出发遍历，返回能否到达最后一行。"""
    visited: set[tuple[int, int]] = set()  # 只记录可通节点
    stack: list[Node] = []

    # TODO: 逻辑可复用简化

    # 重置访问状态，保证同一网格可重复调用
    for row in grid.nodes:
        for node in row:
            node.visited = 0

    # 第一行的可通节点作为起点
    for col in range(grid.cols):
        node = grid.node(0, col)
        if node.accessible == 1:
            node.visited = 1
            visited.add((node.row, node.col))
            stack.append(node)

    # 一直遍历到稳定状态（可通节点要么已访问，要么被隔断）
    while stack:
        node = stack.pop()
        for neighbor in grid.visitable(node.row, node.col):
            if neighbor.visited == 0:
                neighbor.visited = 1
                visited.add((neighbor.row, neighbor.col))
                stack.append(neighbor)

    return any(row == grid.rows - 1 for row, _ in visited)


def batch_grid_visit_test(rows: int, cols: int, percent: float, count: int) -> float:
    """测试指定网格参数下，在 count 个网格中有多少比例的网格可以从第一行到达最后一行。"""
    grids = []
    success_count = 0
    for _ in tqdm(range(count)):  # 进度条
        grid = Grid(rows, cols, percent)
        grids.append(grid)
        if grid_visit_test(grid):
            success_count += 1
    return success_count / count


def visualize(grid: Grid):
    """用 matplotlib 显示网格。"""
    states = np.zeros((grid.rows, grid.cols), dtype=np.uint8)
    for row in range(grid.rows):
        for col in range(grid.cols):
            node = grid.nodes[row][col]
            if node.accessible == 1:
                states[row, col] = 1 if node.visited == 0 else 2

    # 0 黑、1 灰、2 橙黄
    cmap = ListedColormap(["black", "gray", "#FFA500"])
    plt.figure(figsize=(8, 8))
    plt.imshow(states, cmap=cmap, vmin=0, vmax=2, interpolation="nearest")
    plt.axis("off")
    plt.show()


def main():
    # grid = Grid(80, 80, 30)
    # total = grid.rows * grid.cols
    # print(f"网格: {grid.rows}x{grid.cols}, N={grid.percent}%")
    # print(f"可通节点: {grid.open_count}/{total} ({grid.open_count / total:.2%})")

    # node = grid.node(0, 0)
    # print(f"节点 ({node.row}, {node.col}) accessible={node.accessible}")
    # print("可访问的邻居:", [(n.row, n.col) for n in grid.visitable(0, 0)])

    # reached = grid_visit_test(grid)
    # print(f"是否到达最后一行: {reached}")

    # visualize(grid)

    success_rate = batch_grid_visit_test(80, 80, 30, 1000)
    print(f"成功比例: {success_rate:.2%}")


if __name__ == "__main__":
    main()
