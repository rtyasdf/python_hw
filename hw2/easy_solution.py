import numpy as np
import copy
from typing import List


class Matrix:
  def __init__(self, data):
    if isinstance(data, np.ndarray):
      data = data.tolist()

    if not isinstance(data, list):
      raise TypeError("Matrix class expects 2-D list or numpy.ndarray as input")

    if len(data) == 0:
      raise ValueError("Provided data list is empty")

    for row in data:
      if not isinstance(row, list):
        raise TypeError("Matrix class expects 2-D list or numpy.ndarray as input")

    row_len = [len(row) for row in data]
    if len(set(row_len)) > 1:
      raise ValueError("Not all rows are same length")
    if min(row_len) == 0:
      raise ValueError("Empty rows")

    self.data = copy.deepcopy(data)
    self.size = (len(data), row_len[0])

  def __add__(self, other):
    if not isinstance(other, Matrix):
      other = Matrix(other)
    if other.size != self.size:
      raise ValueError(f"dimension mismatch {other_matrix.size} != {self.size}")

    new_data = []
    for row_self, row_other in zip(self.data, other.data):
      new_data.append([x + y for x, y in zip(row_self, row_other)])

    return Matrix(new_data)

  def __mul__(self, other):
    if not isinstance(other, Matrix):
      other = Matrix(other)
    if other.size != self.size:
      raise ValueError(f"dimension mismatch {other_matrix.size} != {self.size}")

    new_data = []
    for row_self, row_other in zip(self.data, other.data):
      new_data.append([x * y for x, y in zip(row_self, row_other)])

    return Matrix(new_data)

  def __matmul__(self, other):
    if not isinstance(other, Matrix):
      other = Matrix(other)
    if self.size[1] != other.size[0]:
      raise ValueError(f"dimension mismatch {self.size[1]} != {other.size[0]}")

    t_other = other.transpose()
    new_data = []
    for row in self.data:
      new_data.append([])
      for other_row in t_other.data:
        new_data[-1].append(sum(x * y for x, y in zip(row, other_row)))

    return Matrix(new_data)

  def transpose(self):
    new_data = [list() for _ in range(self.size[1])]
    for row in self.data:
      for i, element in enumerate(row):
        new_data[i].append(element)

    return Matrix(new_data)


def write_list_to_file(filename: str, data: List):
   with open(filename, 'w') as f:
     for row in data:
       f.write(" ".join(map(str, row)) + '\n')


if __name__ == "__main__":
  np.random.seed(0)

  test_data_1 = np.random.randint(0, 10, (10, 10))
  matrix_1 = Matrix(test_data_1)

  test_data_2 = np.random.randint(0, 10, (10, 10))
  matrix_2 = Matrix(test_data_2)

  matricies = {}
  matricies['+'] = matrix_1 + matrix_2
  matricies['_mult'] = matrix_1 * matrix_2
  matricies['@'] = matrix_1 @ matrix_2

  assert matricies['+'].data == (test_data_1 + test_data_2).tolist(), "sum is broken"
  assert matricies['_mult'].data == (test_data_1 * test_data_2).tolist(), "multiplication is broken"
  assert matricies['@'].data == (test_data_1 @ test_data_2).tolist(), "matmul is broken"

  for k, v in matricies.items():
    write_list_to_file(f'artifacts/easy/matrix{k}.txt', v.data)
