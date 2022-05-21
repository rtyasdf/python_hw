import math
import os
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor
from time import perf_counter as pc
from typing import Callable
from functools import wraps
from tqdm import trange


def measure_time(g):
  @wraps(g)
  def wrapper(*args, **kwargs):
    T = pc()
    result = g(*args, **kwargs)
    T = pc() - T
    with open(f"artifacts/{kwargs['file_name']}", 'a') as f:
      f.write(f"{kwargs['n_jobs']} {kwargs['exec_type']} takes {T:.4f} s\n")
    return result

  return wrapper


def integrate_interval(f: Callable[[float], float],
                       a: float, step: float,
                       left_n: int, right_n: int) -> float:
  acc = 0
  a += left_n * step
  for i in range(left_n, right_n):
    acc += f(a) * step
    a += step
  return acc


@measure_time
def integrate(f: Callable[[float], float],
              a: float, b: float,
              PoolExecutor: Executor,
              n_jobs: int = 1, n_iter: int = 1_000, **kwargs) -> float:
  acc = 0
  step = (b - a) / n_iter
  gap = math.ceil(n_iter / n_jobs)
  with PoolExecutor(max_workers=n_jobs, initializer=log_init) as executor:
    subresults = []
    for k in range(n_jobs):
      fut = executor.submit(integrate_interval, f, a, step, gap * k, min(gap * (k + 1), n_iter))
      fut.add_done_callback(log_done(k))
      subresults.append(fut)
    for future in concurrent.futures.as_completed(subresults):
      acc += future.result()
  return acc


def log_init():
  counter = 0

  def inside_fun():
    counter += 1
    print(f"#{counter} initialized")

  return inside_fun


def log_done(n: int):
  def inside_fun(fn):
    print(f"#{n} done")
  return inside_fun


if __name__ == "__main__":
  num_cpus = os.cpu_count()  # 8

  # ThreadPool
  for n in trange(1, num_cpus * 2):
    result = integrate(math.cos, 0, math.pi / 2,
                       ThreadPoolExecutor, n_jobs=n, n_iter=80_000_000,
                       exec_type='thread', file_name='thread_log.txt')

  # ProcessPool
  for n in trange(1, num_cpus * 2):
    result = integrate(math.cos, 0, math.pi / 2,
                       ProcessPoolExecutor, n_jobs=n, n_iter=80_000_000,
                       exec_type='process', file_name='process_log.txt')
