import random
from dataclasses import dataclass


@dataclass
class Node:
    row: int
    col: int
    accessible: int  # 1 表示通，0 表示不通


class Grid:
    """指定大小的网格，每个节点按百分比随机设为通。"""

    def __init__(self, rows: int, cols: int, percent: float):
        if not 0 <= percent <= 100:
            raise ValueError("percent 必须在 0 到 100 之间")

        self.rows = rows
        self.cols = cols
        self.percent = percent
        self.nodes = [
            [
                Node(row, col, 1 if random.random() * 100 < percent else 0)
                for col in range(cols)
            ]
            for row in range(rows)
        ]

    def node(self, row: int, col: int) -> Node:
        return self.nodes[row][col]

    def visitable(self, row: int, col: int) -> list[Node]:
        """返回下方、左侧、右侧相邻且可通的节点。"""
        result = []
        for dr, dc in ((1, 0), (0, -1), (0, 1)):
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                neighbor = self.nodes[r][c]
                if neighbor.accessible == 1:
                    result.append(neighbor)
        return result


def main():
    grid = Grid(800, 800, 60)
    accessible = sum(node.accessible for row in grid.nodes for node in row)
    total = grid.rows * grid.cols
    print(f"网格: {grid.rows}x{grid.cols}, N={grid.percent}%")
    print(f"实际可通比例: {accessible / total:.2%}")

    node = grid.node(0, 0)
    print(f"节点 ({node.row}, {node.col}) accessible={node.accessible}")
    print("可访问的邻居:", [(n.row, n.col) for n in grid.visitable(0, 0)])


if __name__ == "__main__":
    main()
