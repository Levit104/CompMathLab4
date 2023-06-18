import math
from typing import Any
from tabulate import tabulate


def gauss_method(matrix: list[list[float]], const_terms: list[float], n: int) -> list[float]:
    for i in range(n):
        # Поиск максимального элемента
        max_element: float = abs(matrix[i][i])
        max_row: int = i
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
    x: list[float] = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (const_terms[i] - sum(matrix[i][j] * x[j] for j in range(i + 1, n))) / matrix[i][i]

    return x


def has_duplicates(lst: list[Any]) -> bool:
    return len(lst) != len(set(lst))


def linspace(a: float, b: float, n: int) -> list[float]:
    delta: float = (b - a) / (n - 1)
    return [a + i * delta for i in range(n)]


def sort_by_column(table: list[list[Any]], col: int) -> None:
    table.sort(key=lambda x: x[col])


def make_log(values: list[float]) -> list[float]:
    return [math.log(val) for val in values]


def swap_list_values(lst: list[Any], pos1: int, pos2: int) -> None:
    lst[pos1], lst[pos2] = lst[pos2], lst[pos1]


def transpose(table: list[list[Any]]) -> list[list[Any]]:
    return [list(row) for row in zip(*table)]


def dictionary_find_min(dictionary: dict[Any, Any]) -> tuple[Any, Any]:
    min_key: Any = min(dictionary, key=dictionary.get)
    min_value: Any = dictionary[min_key]
    return min_key, min_value


def table_to_string(data: list[Any],
                    headers: list[Any],
                    table_format: str = 'fancy_grid',
                    float_format: str = '.5f',
                    align: str = 'decimal',
                    show_index: bool = True) -> str:
    table: str = tabulate(data,
                          headers=headers,
                          tablefmt=table_format,
                          floatfmt=float_format,
                          numalign=align,
                          showindex=show_index)
    return table
