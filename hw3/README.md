## Medium

Matrix class here based on 4 mixins: 

* `NDArrayOperatorsMixin` -- for arithmetic operations
* `FileWriter` -- only for writing data to file 
* `TypeHolder` -- for keeping property `print_type`, which correspond to style of printing in `PrettyPrint2D`
* `PrettyPrint2D` -- for `__str__` method

## Hard

Hash function -- weighted sum over all matrix, weight computed based on position of element (weight is 2 in some power).

Main class here based on `Matrix` class from `easy_solution` and mixin, which implemets hash.
Also take look on `cache_test`: while first matrix multiplication taken approx. 4 seconds, evey further multiplication of same matrices takes on average less than 0.04 seconds.

As expected, there is a collision in hashes of `A @ B` and `C @ D`, so to compute real value of `C @ B` instead `C @ (B + E) - C` is computed, where `E` -- identity matrix.
