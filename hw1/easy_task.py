from typing import List


def fib_n(n: int) -> List:
  a = 0
  b = 1
  L = [a]
  for _ in range(n - 1):
    b += a
    a = b - a
    L.append(a)
  return L


if __name__ == "__main__":
  assert fib_n(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
