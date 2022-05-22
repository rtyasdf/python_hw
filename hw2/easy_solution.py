from typing import List, Union


def check_list(elements: List[List[Union[int, str]]]):
  len_0 = len(elements[0])
  if len_0 == 0:
    raise ValueError("empty rows")

  flist = list(filter(lambda l: len(l) != len_0, elements))
  if len(flist) > 0:
    raise ValueError("rows have different length")


def generate_table(elements: List[List[Union[int, str]]]) -> str:
  check_list(elements)

  slash = '\\'
  dslash = 2 * slash

  rows = map(lambda x: map(str, x), elements)
  flatten = map(" & ".join, rows)
  tex_string = f" {dslash}\n{slash}hline\n".join(flatten)

  prefix = f'{slash}' + 'begin{tabular}'
  prefix = prefix + '{|' + 'c|' * len(elements[0]) + '}\n'
  prefix = prefix + f'{slash}hline'
  suffix = f'{dslash}\n{slash}hline\n{slash}' + 'end{tabular}'

  return f'{prefix}\n{tex_string} {suffix}'


if __name__ == '__main__':
  elts = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
  with open('artifacts/easy/table.tex', 'w') as f:
    f.write(generate_table(elts))
