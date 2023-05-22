import math

from functions import Function
from util import gauss_method, make_log, swap_list_values


def least_squares(x, y, n, m):
    matrix = []
    const_terms = []

    for row_num in range(m + 1):
        row = []
        for col_num in range(m + 1):
            sum_val = sum(x[i] ** (row_num + col_num) for i in range(n))
            row.append(sum_val)

            sum_val = sum(y[i] * x[i] ** col_num for i in range(n))
            const_terms.append(sum_val)

        matrix.append(row)

    return matrix, const_terms


def calculate_correlation_coefficient(x, y, n):
    x_mean = sum(x) / n
    y_mean = sum(y) / n

    temp_sum1 = 0
    temp_sum2 = 0
    temp_sum3 = 0
    for i in range(n):
        temp_sum1 += (x[i] - x_mean) * (y[i] - y_mean)
        temp_sum2 += (x[i] - x_mean) ** 2
        temp_sum3 += (y[i] - y_mean) ** 2

    return temp_sum1 / math.sqrt(temp_sum2 * temp_sum3)


def approximate(x, y, n, function: Function):
    if function.name in 'Степенная':
        matrix, const_terms = least_squares(make_log(x), make_log(y), n, function.degree)
    elif function.name in 'Экспоненциальная':
        matrix, const_terms = least_squares(x, make_log(y), n, function.degree)
    elif function.name in 'Логарифмическая':
        matrix, const_terms = least_squares(make_log(x), y, n, function.degree)
    else:
        matrix, const_terms = least_squares(x, y, n, function.degree)

    function.coeffs = gauss_method(matrix, const_terms, function.degree + 1)

    if function.name in ['Степенная', 'Экспоненциальная']:
        function.coeffs[0] = math.exp(function.coeffs[0])

    if function.name in 'Логарифмическая':
        swap_list_values(function.coeffs, 0, 1)

    phi = [function(x[i]) for i in range(n)]

    eps = [phi[i] - y[i] for i in range(n)]
    deviation_measure = sum(eps_i ** 2 for eps_i in eps)
    standard_deviation = math.sqrt(deviation_measure / n)

    table1 = [['x'] + x, ['y'] + y, ['ϕ'] + phi, ['ε'] + eps]

    function.round_coeffs(to=5)
    table2 = [f'Функция ϕ(x) = {function}',
              f'Мера отклонения S = {round(deviation_measure, 5)}',
              f'Среднеквадратичное отклонение σ = {round(standard_deviation, 5)}']

    if 'Линейная' in function.name:
        r = calculate_correlation_coefficient(x, y, n)
        table2.append(f'Коэффициент корреляции Пирсона r = {round(r, 5)}')

    return table1, table2, phi, standard_deviation
