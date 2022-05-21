import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin
from medium_mixins import FileWriter, TypeHolder, PrettyPrint2D


class Matrix(NDArrayOperatorsMixin, PrettyPrint2D, FileWriter, TypeHolder):
  def __init__(self, data, ptype=None):
    self.data = np.asarray(data)
    self._print_type = ptype if ptype else 'float'

  def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
    for x in inputs:
      if not isinstance(x, Matrix):
        return NotImplemented

    input_data = tuple(x.data for x in inputs)
    int_types = tuple(filter(lambda x: x.print_type == 'int', inputs))
    result = getattr(ufunc, method)(*input_data, **kwargs)
    return Matrix(result, 'int' if len(int_types) else 'float')


if __name__ == "__main__":
  np.random.seed(0)

  test_data_1 = np.random.randint(0, 10, (10, 10))
  matrix_1 = Matrix(test_data_1.tolist(), 'int')

  test_data_2 = np.random.randint(0, 10, (10, 10))
  matrix_2 = Matrix(test_data_2.tolist(), 'int')

  matricies = {}
  matricies['+'] = matrix_1 + matrix_2
  matricies['_mult'] = matrix_1 * matrix_2
  matricies['@'] = matrix_1 @ matrix_2

  for k, v in matricies.items():
    v.write(f'artifacts/medium/matrix{k}.txt')
