import re
import ast
import inspect
import astunparse
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from typing import List, Tuple, Union
from easy_task import fib_n
from wrappers import Interval, FakeNode, NodeInfo


class ASTWrapper:
  def __init__(self):
    self.terminal_counter = 0
    self.terminals = defaultdict(int)
    self.cumulative_terminals = defaultdict(int)
    self.fake_info = NodeInfo(-1, 2, Interval(1, -1))
    self.clear()

  def clear(self):
    self.head = -1
    self.edges = []
    self.node_labels = {}
    self.positions = {}
    self.colors = {}

  def construct(self, root: ast.AST):
    """
    Collect terminal vertex statistics and
    copying each edge from real AST.
    """
    # Count terminals (that's useful for drawing)
    gc.count_terminals((root.body[0], None), -1)
    self.clear()

    # DFS on graph
    root_info = NodeInfo(-1, 10, Interval(-8, 8))  # just constants
    nodes = [(root.body[0], root_info)]
    while nodes:
      node, info = nodes.pop()
      nodes.extend(self.flatten(node, info))

  def flatten(self, node: Union[ast.AST, FakeNode], info: NodeInfo) -> List:
    """
    For node of AST returns it's childrens,
    while also wrapping all node connections for further drawing.
    """
    self.head += 1
    if info.parent_id >= 0:
      self.edges.append((info.parent_id, self.head))

    # Define position of node on plot
    # (different behavior if vertex terminal/non-terminal)
    self.positions[self.head] = (info.middle_point(), info.level)
    if self.terminals[self.head]:
      new_right = - self.cumulative_terminals[self.head]
      new_left = new_right - self.terminals[self.head]
      self.positions[self.head] = (new_right - self.terminals[self.head] / 2, info.level)
      info.interval = Interval(new_left, new_right)

    # Wrapping some AST node classes
    method_name = re.sub("([A-Z])", "_\g<1>", node.__class__.__name__)
    method = getattr(self, method_name.lower())
    return method(node, info)

  def create_child_info(self, info: NodeInfo, neighbors: int, index: int) -> NodeInfo:
    """
    Define some properties of child node based on info of parent.
    """
    gap = (info.interval.right - info.interval.left) / neighbors
    new_left = info.interval.left + gap * index
    new_right = new_left + gap
    return NodeInfo(self.head, info.level - 1, Interval(new_left, new_right))

  def count_terminals(self, node_info: NodeInfo, key: int) -> int:
    """
    Recursively counting how many terminal vertices alredy visited,
    and how many descendants of vertex are terminal.
    """
    childrens = self.flatten(node_info[0], self.fake_info)
    if len(childrens):
      self.cumulative_terminals[key + 1] = self.terminal_counter
      result = 0
      for child in reversed(childrens):
        result += self.count_terminals(child, self.head)
      self.terminals[key + 1] = result
      return result
    else:
      self.terminal_counter += 1
      return 1

  def draw(self):
    """
    AST drawing.
    """
    # Build graph and draw it
    G = nx.Graph()
    G.add_edges_from(self.edges)
    colors = [0] * len(self.colors)
    for i, c in self.colors.items():
      colors[i] = c
    nx.draw(G, pos=self.positions, node_color=colors)

    # Pool every label up a little bit and draw them
    label_position = {i : (x, y + 0.15) for i, (x, y) in self.positions.items()}
    nx.draw_networkx_labels(G, label_position, font_weight='bold', labels=self.node_labels)
    plt.show()

  def _assign(self, node: ast.AST, info: NodeInfo) -> List[Tuple[ast.AST, NodeInfo]]:
    self.node_labels[self.head] = '='
    self.colors[self.head] = '#20dd20'
    return [(node.targets[0], self.create_child_info(info, 2, 0)),
            (node.value, self.create_child_info(info, 2, 1))]

  def _aug_assign(self, node: ast.AST, info: NodeInfo) -> List[Tuple[ast.AST, NodeInfo]]:
    self.node_labels[self.head] = astunparse.unparse(node)
    self.colors[self.head] = '#20dd20'
    return [(node.target, self.create_child_info(info, 2, 0)),
            (node.value, self.create_child_info(info, 2, 1))]

  def _bin_op(self, node: ast.AST, info: NodeInfo) -> List[Tuple[ast.AST, NodeInfo]]:
    self.node_labels[self.head] = astunparse.unparse(node)
    self.colors[self.head] = '#20dd20'
    return [(node.left, self.create_child_info(info, 2, 0)),
            (node.right, self.create_child_info(info, 2, 1))]

  def _name(self, node: ast.AST, info: NodeInfo) -> List:
    self.node_labels[self.head] = str(node.id)
    self.colors[self.head] = '#eedd20'
    return []

  def _constant(self, node: ast.AST, info: NodeInfo) -> List:
    self.node_labels[self.head] = str(node.value)
    self.colors[self.head] = '#aa22cc'
    return []

  def _list(self, node: ast.AST, info: NodeInfo) -> List:
    self.node_labels[self.head] = astunparse.unparse(node)
    self.colors[self.head] = '#eeaaaa'
    return []

  def _return(self, node: ast.AST, info: NodeInfo) -> List:
    self.node_labels[self.head] = 'return'
    self.colors[self.head] = '#dd2020'
    return [(node.value, self.create_child_info(info, 1, 0))]

  def _call(self, node: ast.AST, info: NodeInfo) -> List:
    self.node_labels[self.head] = astunparse.unparse(node)
    self.colors[self.head] = '#eeaaaa'
    return []

  def _expr(self, node: ast.AST, info: NodeInfo) -> List:
    self.node_labels[self.head] = astunparse.unparse(node)
    self.colors[self.head] = '#eeaaaa'
    return []

  def _for(self, node: ast.AST, info: NodeInfo) -> List[Tuple[FakeNode, NodeInfo]]:
    self.node_labels[self.head] = 'for'
    self.colors[self.head] = '#bbbbdd'
    return [(FakeNode([node.target, node.iter], ''), self.create_child_info(info, 2, 0)),
            (FakeNode(node.body, 'body'), self.create_child_info(info, 2, 1))]

  def _function_def(self, node: ast.AST, info: NodeInfo) -> List[Tuple[ast.AST, NodeInfo]]:
    self.node_labels[self.head] = f'function {node.name}'
    self.colors[self.head] = '#88aa20'
    return [(body_node, self.create_child_info(info, len(node.body), i)) for i, body_node in enumerate(node.body)]

  def _fake_node(self, node: FakeNode, info: NodeInfo) -> List[Tuple[ast.AST, NodeInfo]]:
    self.node_labels[self.head] = node.name
    self.colors[self.head] = '#1f78b4'
    return [(body_node, self.create_child_info(info, len(node.body), i)) for i, body_node in enumerate(node.body)]


if __name__ == "__main__":
  root = ast.parse(inspect.getsource(fib_n))

  gc = ASTWrapper()
  gc.construct(root)
  gc.draw()
