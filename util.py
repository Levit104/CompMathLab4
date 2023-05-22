import math


def cramer_method_2x2(matrix, const_terms):
    det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det1 = const_terms[0] * matrix[1][1] - const_terms[1] * matrix[0][1]
    det2 = const_terms[1] * matrix[0][0] - const_terms[0] * matrix[1][0]

    return [det1 / det, det2 / det]


def gauss_method(matrix, const_terms, n):
    for i in range(n):
        # Поиск максимального элемента
        max_element = abs(matrix[i][i])
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > max_element:
                max_element, max_row = abs(matrix[j][i]), j

        # Перестановка строк, если максимальный элемент найден не на главной диагонали
        if max_row != i:
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            const_terms[i], const_terms[max_row] = const_terms[max_row], const_terms[i]

        # Приведение матрицы к треугольному виду
        for k in range(i + 1, n):
            c = -matrix[k][i] / matrix[i][i]

            for j in range(n):
                matrix[k][j] += c * matrix[i][j]

            const_terms[k] += c * const_terms[i]

    # Обратный ход, нахождение неизвестных
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (const_terms[i] - sum(matrix[i][j] * x[j] for j in range(i + 1, n))) / matrix[i][i]

    return x


def make_log(values):
    return [math.log(val) for val in values]


def swap_list_values(lst, pos1, pos2):
    lst[pos1], lst[pos2] = lst[pos2], lst[pos1]


def has_duplicates(lst):
    return len(lst) != len(set(lst))
