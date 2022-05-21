import codecs
import time
from time import gmtime, strftime
from multiprocessing import Process, Queue


def a_task(q: Queue, p: Queue):
  while True:
    time.sleep(5)
    if not q.empty():
      str_from_host = q.get()
      p.put(str_from_host.lower())


def b_task(p: Queue, r: Queue):
  while True:
    if not p.empty():
      str_from_a = p.get()
      r.put((codecs.encode(str_from_a, 'rot_13'), get_time()))


def get_time():
  return strftime("%H:%M:%S", gmtime())


if __name__ == "__main__":
  host_a_queue = Queue()
  a_b_queue = Queue()
  b_host_queue = Queue()

  a_proc = Process(target=a_task, args=(host_a_queue, a_b_queue))
  b_proc = Process(target=b_task, args=(a_b_queue, b_host_queue))

  a_proc.start()
  b_proc.start()

  while True:
    output_message = input("enter: ")
    host_a_queue.put(output_message)
    with open('log_file.txt', 'a') as f:
      f.write(f'{get_time()} send message "{output_message}"\n')

    while not b_host_queue.empty():
      input_message, clock_time = b_host_queue.get()
      print(input_message)
      with open('artifacts/log_file.txt', 'a') as f:
        f.write(f'{clock_time} message "{input_message}" was send through Queue\n')

  a.join()
  b.join()
