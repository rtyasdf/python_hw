from dataclasses import dataclass
from collections import namedtuple
from typing import List
import ast


Interval = namedtuple('Interval', 'left right')


@dataclass
class FakeNode:
  body: List[ast.AST]
  name: str


@dataclass
class NodeInfo:
  parent_id: int
  level: int
  interval: Interval

  def middle_point(self):
    return (self.interval.left + self.interval.right) / 2
