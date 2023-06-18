import os
from typing import Any, Callable

from util import sort_by_column, transpose, has_duplicates


def get_data() -> tuple[list[float], list[float], int] | None:
    print('\nЧтобы выйти из программы введите exit на любом этапе')

    input_id: int
    points_number: int
    points: list[list[float]]
    x_values: list[float]
    y_values: list[float]

    print_dictionary('Режимы ввода', input_output_modes)
    input_id = int(get_value('Выберите режим ввода', CONSOLE, FILE, False))
    points_number, points = get_data_dict[input_id]()
    sort_by_column(points, col=0)

    x_values, y_values = transpose(points)

    if has_duplicates(x_values):
        print('\nЗначения X должны быть уникальными')
        return

    return x_values, y_values, points_number


def print_results(results_sting: str) -> None:
    print_dictionary('Режимы вывода', input_output_modes)
    output_id: int = int(get_value('Выберите режим вывода', CONSOLE, FILE, False))
    print_results_dict[output_id](results_sting)


# -----------------------------------------------------------------------------------------
def get_data_from_console() -> tuple[int, list[list[float]]]:
    n: int = int(get_value('Введите кол-во точек (от 8 до 12)',
                           min_value=8,
                           max_value=12,
                           strict=False,
                           invalid_message='Кол-во точек должно быть от 8 до 12'))
    points: list[list[float]] = get_table(column_size=n,
                                          row_size=2,
                                          description='Введите через пробел значения x и y точки {}')
    return n, points


def get_data_from_file() -> tuple[int, list[list[float]]]:
    path: str = get_file()
    with open(path, 'r', encoding='utf-8') as file:
        data: list[str] = [line for line in file.read().splitlines() if line != '']
        table_size: str = data.pop(0)

        if not valid_value(table_size, min_value=8, max_value=12, strict=False):
            print('\nНевалидное число точек. Убедитесь, что данное значение находится в начале файла')
            return get_data_from_file()

        table_size: int = int(table_size)

        if len(data) != table_size:
            print('\nНеверное кол-во строк в файле')
            return get_data_from_file()

        table: list[list[str]] = [line.split() for line in data]

        if any(not valid_row(row, row_size=2) for row in table):
            print('Невалидные значения в одной или в нескольких строках')
            return get_data_from_file()

        return table_size, [[float(val) for val in row] for row in table]


def print_results_to_console(results_sting: str) -> None:
    print(f'\nРезультаты аппроксимации: {results_sting}')


def print_results_to_file(results_sting: str) -> None:
    path: str = get_file(validate=False)

    with open(path, 'w', encoding='utf-8') as file:
        file.write(f'\nРезультаты аппроксимации: {results_sting}\n')


CONSOLE: int = 1
FILE: int = 2

input_output_modes: dict[int, str] = {
    CONSOLE: 'Консоль',
    FILE: 'Файл'
}

get_data_dict: dict[int, Callable[[], tuple[int, list[list[float]]]]] = {
    CONSOLE: get_data_from_console,
    FILE: get_data_from_file
}

print_results_dict: dict[int, Callable[[str], None]] = {
    CONSOLE: print_results_to_console,
    FILE: print_results_to_file
}


# -----------------------------------------------------------------------------------------
def print_dictionary(name: str, dictionary: dict[Any, Any]) -> None:
    print(f'\n{name}:', end='')
    for key, value in dictionary.items():
        print(f'\n\t{key}. {value}', end='')
    print()


def get_value(description: str = 'Введите значение',
              min_value: float = float('-inf'),
              max_value: float = float('inf'),
              strict: bool = True,
              invalid_message: str = 'Невалидное значение') -> float:
    value: str = input(f'\n{description}: ').strip().replace(',', '.')

    while not valid_value(value, min_value, max_value, strict):
        print(invalid_message)
        value = input('Повторите ввод: ').strip().replace(',', '.')

    return float(value)


def get_row(row_size: int,
            description: str = 'Введите значения ряда',
            min_value: float = float('-inf'),
            max_value: float = float('inf'),
            strict: bool = True,
            invalid_message: str = 'Невалидные значения или размер ряда') -> list[float]:
    row: list[str] = input(f'\n{description}: ').replace(',', '.').split()

    while not valid_row(row, row_size, min_value, max_value, strict):
        print(invalid_message)
        row = input('Повторите ввод: ').replace(',', '.').split()

    return [float(val) for val in row]


def get_table(column_size: int,
              row_size: int,
              description: str = 'Введите значения ряда',
              min_value: float = float('-inf'),
              max_value: float = float('inf'),
              strict: bool = True,
              invalid_message: str = 'Невалидные значения или размер ряда') -> list[list[float]]:
    table: list[list[float]] = [
        get_row(row_size, description.format(i + 1), min_value, max_value, strict, invalid_message)
        for i in range(column_size)]
    return table


def get_file(validate: bool = True) -> str:
    path: str = input('\nВведите путь до файла: ').strip()

    if validate:
        while not valid_file(path):
            print('Файла не существует или он пустой')
            path = input('Повторите ввод: ').strip()

    return path


# -----------------------------------------------------------------------------------------
def valid_value(value: str,
                min_value: float = float('-inf'),
                max_value: float = float('inf'),
                strict: bool = True) -> bool:
    if value == 'exit':
        raise KeyboardInterrupt
    try:
        if strict:
            return min_value < float(value) < max_value
        else:
            return min_value <= float(value) <= max_value
    except ValueError:
        return False


def valid_row(row: list[str],
              row_size: int,
              min_value: float = float('-inf'),
              max_value: float = float('inf'),
              strict: bool = True) -> bool:
    if len(row) != row_size:
        return False
    return all(valid_value(val, min_value, max_value, strict) for val in row)


def valid_file(path: str) -> bool:
    return os.path.isfile(path) and os.path.getsize(path) > 0
