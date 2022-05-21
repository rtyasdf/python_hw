from multiprocessing import Process
from threading import Thread
from time import perf_counter as pc
from tqdm import trange
from typing import List, Union, Tuple


def fib_n(n: int):
  a, b = 0, 1
  for _ in range(n):
    a, b = b, a + b
  return a


def start_join(pt_list: List[Union[Process, Thread]]):
  for p in pt_list:
    p.start()

  for p in pt_list:
    p.join()


def report(cls, n: int, k: int, filename: str, exec_type: str) -> Tuple[int, float]:
  log = []
  for j in trange(1, k + 1):
    T = pc()

    # Run function `n` times, but on `j` processes/threads
    for i in range(0, k, j):
      start_join([cls(target=fib_n, args=(n, )) for _ in range(j)])
    start_join([cls(target=fib_n, args=(n, )) for _ in range(k - i)])

    T = pc() - T
    log.append((j, T))
    with open(filename, 'a') as f:
      f.write(f"{j:01} {exec_type} -- {T:.4f} s\n")

  return min(log, key=lambda t: t[1])


if __name__ == "__main__":
  big_n = 400_000
  num_of_runs = 10

  s_time = pc()
  for _ in range(num_of_runs):
    fib_n(big_n)
  s_time = pc() - s_time
  print(f"synchronized : {s_time:.4f} s")

  # Test range of threads and processes
  num_of_threads, thread_time = report(Thread, big_n, num_of_runs, 'artifacts/thread_log.txt', 'threads')
  num_of_proc, proc_time = report(Process, big_n, num_of_runs, 'artifacts/mp_log.txt', 'processes')

  # Report time on best configuration
  with open('artifacts/final_log.txt', 'a') as f:
    f.write(f'{num_of_threads} threads : {thread_time:.4f} s\n')
    f.write(f'{num_of_proc} processes : {proc_time:.4f} s\n')
    f.write(f'synchronized : {s_time:.4f} s\n')
