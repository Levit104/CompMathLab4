import math

from util import gauss_method, make_log, swap_list_values


class Approximation:
    name: str
    degree: int
    linear: bool
    coeffs: list[float]

    def __init__(self, name: str, degree: int, linear: bool = False):
        self.name = name
        self.degree = degree
        self.linear = linear
        self.coeffs = []

    def __call__(self,
                 x: list[float],
                 y: list[float],
                 n: int) -> tuple[list[float], list[float], float, float, float | None]:
        self.approximate(x, y, n)
        return self.calculate_results(x, y, n)

    def calculate_results(self,
                          x: list[float],
                          y: list[float],
                          n: int) -> tuple[list[float], list[float], float, float, float | None]:
        phi: list[float] = [self.function(x[i]) for i in range(n)]
        eps: list[float] = [phi[i] - y[i] for i in range(n)]
        dev_measure: float = sum(eps[i] ** 2 for i in range(n))
        dev: float = math.sqrt(dev_measure / n)
        r: float | None = self.calculate_correlation_coefficient(x, y, n) if self.linear else None
        return phi, eps, dev_measure, dev, r

    def approximate(self, x: list[float], y: list[float], n: int) -> None:
        pass

    def function(self, x: float) -> float:
        pass

    def function_string(self, float_format: str) -> str:
        pass

    @staticmethod
    def least_squares(x: list[float], y: list[float], n: int, m: int) -> tuple[list[list[float]], list[float]]:
        matrix: list[list[float]] = []
        const_terms: list[float] = []

        for row_num in range(m + 1):
            row: list[float] = []
            for col_num in range(m + 1):
                sum_val: float = sum(x[i] ** (row_num + col_num) for i in range(n))
                row.append(sum_val)
            matrix.append(row)

        for col_num in range(m + 1):
            sum_val: float = sum(y[i] * x[i] ** col_num for i in range(n))
            const_terms.append(sum_val)

        return matrix, const_terms

    @staticmethod
    def calculate_correlation_coefficient(x: list[float], y: list[float], n: int) -> float:
        x_mean: float = sum(x) / n
        y_mean: float = sum(y) / n
        temp_sum1: float = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        temp_sum2: float = sum((x[i] - x_mean) ** 2 for i in range(n))
        temp_sum3: float = sum((y[i] - y_mean) ** 2 for i in range(n))
        return temp_sum1 / math.sqrt(temp_sum2 * temp_sum3)


class PolynomApproximation(Approximation):
    def approximate(self, x, y, n):
        matrix, const_terms = self.least_squares(x, y, n, self.degree)
        self.coeffs = gauss_method(matrix, const_terms, self.degree + 1)

    def function(self, x):
        return sum([a_i * (x ** i) for i, a_i in enumerate(self.coeffs)])

    def function_string(self, float_format):
        s = ''
        for i, coeff in enumerate(self.coeffs):
            if i == 0:
                s += f'{coeff:{float_format}} + '
            elif i == 1:
                s += f'({coeff:{float_format}} * x) + '
            else:
                s += f'({coeff:{float_format}} * x^{i}) + '
        return s[:-3]


class PowApproximation(Approximation):
    def approximate(self, x, y, n):
        matrix, const_terms = self.least_squares(make_log(x), make_log(y), n, self.degree)
        self.coeffs = gauss_method(matrix, const_terms, self.degree + 1)
        self.coeffs[0] = math.exp(self.coeffs[0])

    def function(self, x):
        return self.coeffs[0] * x ** self.coeffs[1]

    def function_string(self, float_format):
        return f'{self.coeffs[0]:{float_format}} * x^({self.coeffs[1]:{float_format}})'


class ExpApproximation(Approximation):
    def approximate(self, x, y, n):
        matrix, const_terms = self.least_squares(x, make_log(y), n, self.degree)
        self.coeffs = gauss_method(matrix, const_terms, self.degree + 1)
        self.coeffs[0] = math.exp(self.coeffs[0])

    def function(self, x):
        return self.coeffs[0] * math.exp(self.coeffs[1] * x)

    def function_string(self, float_format):
        return f'{self.coeffs[0]:{float_format}} * e^({self.coeffs[1]:{float_format}} * x)'


class LogApproximation(Approximation):
    def approximate(self, x, y, n):
        matrix, const_terms = self.least_squares(make_log(x), y, n, self.degree)
        self.coeffs = gauss_method(matrix, const_terms, self.degree + 1)
        swap_list_values(self.coeffs, 0, 1)

    def function(self, x):
        return self.coeffs[0] * math.log(x) + self.coeffs[1]

    def function_string(self, float_format):
        return f'{self.coeffs[0]:{float_format}} * ln(x) + {self.coeffs[1]:{float_format}}'


approximations_list: list[Approximation] = [
    PolynomApproximation('Линейная', 1, True),
    PolynomApproximation('Квадратичная', 2),
    PolynomApproximation('Кубическая', 3),
    PowApproximation('Степенная', 1),
    ExpApproximation('Экспоненциальная', 1),
    LogApproximation('Логарифмическая', 1)
]
