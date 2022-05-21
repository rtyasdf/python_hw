from functools import wraps
from easy_solution import Matrix, write_list_to_file
import numpy as np
from time import perf_counter as pc


def cache_wrapper(f):
  cache_table = {}  # unlimited size for simplicity

  @wraps(f)
  def wrap_fn(*args):
    key = tuple(map(hash, args))
    if key in cache_table:
      return cache_table[key]
    result = f(*args)
    cache_table[key] = result
    return result

  return wrap_fn


class HashMixin:
  def __hash__(self):
    final_hash = 0
    for i, row in enumerate(self.data):
      for j, element in enumerate(row):
        final_hash += hash(element) << ((i + j) % 10)
      final_hash &= ((1 << 31) - 1)
    return final_hash


class HashedMatrix(Matrix, HashMixin):
  @cache_wrapper
  def __matmul__(self, other):
    return HashedMatrix(super().__matmul__(other).data)

  def __mul__(self, other):
    if isinstance(other, float) or isinstance(other, int):
      new_data = []
      for row_self in self.data:
        new_data.append([other * x for x in row_self])
    else:
      new_data = super().__mul__(other).data
    return HashedMatrix(new_data)

  def __add__(self, other):
    return HashedMatrix(super().__add__(other).data)

  def __sub__(self, other):
    return self + other * (-1)


def cache_test():
  print("Caching test:")
  np.random.seed(0)
  test_data_1 = np.random.randint(0, 10, (400, 400))
  matrix_1 = HashedMatrix(test_data_1)

  test_data_2 = np.random.randint(0, 10, (400, 400))
  matrix_2 = HashedMatrix(test_data_2)

  T = pc()
  matrix_1 @ matrix_2
  print(f"time on 1 multiplication : {pc() - T:.3f}")

  T = pc()
  for _ in range(10):
    matrix_1 @ matrix_2
  print(f"time on 10 same multipications : {pc() - T:.3f}")


if __name__ == "__main__":
  cache_test()

  # Collisions
  A = HashedMatrix([[1, 0, 4], [0, 7, 5], [9, -1, 2]])
  C = HashedMatrix([[-3, -2, 6], [8, -5, 9], [-3, 0, 4]])
  B = HashedMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
  E = HashedMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

  matricies = {}
  matricies['A'] = A
  matricies['B'] = B
  matricies['C'] = C
  matricies['AB'] = A @ B
  matricies['CD'] = C @ (B + E) - C

  hashes = {}
  hashes['AB'] = hash(A @ B)
  hashes['fake_CD'] = hash(C @ B)
  hashes['real_CD'] = hash(C @ (B + E) - C)

  for k, v in matricies.items():
    write_list_to_file(f'artifacts/hard/matrix{k}.txt', v.data)

  with open('artifacts/hard/hash.txt', 'w') as f:
    for k, v in hashes.items():
      f.write(f'{k} : {v}\n')
