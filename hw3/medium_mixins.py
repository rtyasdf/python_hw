from typing import List


class FileWriter:
  def write(self, filename: str):
    with open(filename, 'w') as f:
      for row in self.data:
        f.write(" ".join(map(str, row)) + '\n')


class TypeHolder:
  @property
  def print_type(self):
    return self._print_type

  @print_type.setter
  def print_type(self, new_type):
    self._print_type = new_type


class PrettyPrint2D:
  def __str__(self):
    output_str = str()
    for row in self.data:
      for element in row:
        if self._print_type == 'int':
          output_str = f"{output_str}{element:3d} "
        elif self._print_type == 'float':
          output_str = f"{output_str}{element:.2f} "
        else:
          output_str = f"{output_str}{element} "
      output_str = output_str + '\n'
    return output_str[:-1]
