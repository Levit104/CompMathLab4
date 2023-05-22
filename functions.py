import math


class Function:
    def __init__(self, name, degree):
        self.__name = name
        self.__degree = degree
        self.__coeffs = []

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def degree(self):
        return self.__degree

    @degree.setter
    def degree(self, degree):
        self.__degree = degree

    @property
    def coeffs(self):
        return self.__coeffs

    @coeffs.setter
    def coeffs(self, coeffs):
        self.__coeffs = coeffs

    def __call__(self, x):
        return 0.0

    def round_coeffs(self, to):
        self.__coeffs = [round(c, to) for c in self.__coeffs]


class PolynomFunction(Function):
    def __call__(self, x):
        return sum([a_i * (x ** i) for i, a_i in enumerate(self.coeffs)])

    def __str__(self):
        s = ''
        for i, coeff in enumerate(self.coeffs):
            if i == 0:
                s += f'{coeff} + '
            elif i == 1:
                s += f'({coeff} * x) + '
            else:
                s += f'({coeff} * x^{i}) + '
        return s[:-3]


class PowFunction(Function):
    def __call__(self, x):
        return self.coeffs[0] * x ** self.coeffs[1]

    def __str__(self):
        return f'{self.coeffs[0]} * x^({self.coeffs[1]})'


class ExpFunction(Function):
    def __call__(self, x):
        return self.coeffs[0] * math.exp(self.coeffs[1] * x)

    def __str__(self):
        return f'{self.coeffs[0]} * e^({self.coeffs[1]} * x)'


class LogFunction(Function):
    def __call__(self, x):
        return self.coeffs[0] * math.log(x) + self.coeffs[1]

    def __str__(self):
        return f'{self.coeffs[0]} * ln(x) + {self.coeffs[1]}'


functions_list = [
    PolynomFunction('Линейная', 1),
    PolynomFunction('Квадратичная', 2),
    PolynomFunction('Кубическая', 3),
    PowFunction('Степенная', 1),
    ExpFunction('Экспоненциальная', 1),
    LogFunction('Логарифмическая', 1)
]
