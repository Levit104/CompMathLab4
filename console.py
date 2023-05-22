from validation import valid_file, valid_value, valid_matrix_row


def get_value(description, *valid_params, add_validation=lambda x: True, add_message=''):
    value = input(f'\n{description}: ').strip()

    while not (valid_value(value, *valid_params) and add_validation(value)):
        print(f'Невалидное значение'
              f'{add_message}')
        value = input('Повторите ввод: ').strip()

    return value


def get_matrix_row(description, row_size, *valid_row_value_params):
    row = input(f'\n{description}: ').split()

    while not valid_matrix_row(row, row_size, *valid_row_value_params):
        print('Невалидные значения или размер ряда')
        row = input('Повторите ввод: ').split()

    return [float(val) for val in row]


def get_matrix(matrix_size, description, row_size, *valid_row_value_params):
    matrix = [get_matrix_row(description.format(i + 1), row_size, *valid_row_value_params)
              for i in range(matrix_size)]
    return matrix


def print_dictionary(name, dictionary, value_is_tuple=False, value_tuple_index=1):
    print(f'\n{name}:', end='')
    for key, value in dictionary.items():
        print(f'\n\t{key}. {value[value_tuple_index] if value_is_tuple else value}', end='')
    print()


valid_points_number_params = (8, 12, False)
valid_value_pair_params = (float('-inf'), float('inf'), True)


def get_points_number():
    return int(get_value('Введите кол-во точек (от 8 до 12)',
                         *valid_points_number_params,
                         add_message='\nКол-во точек должно быть от 8 до 12'))


def get_points(points_number):
    return get_matrix(points_number, 'Введите через пробел значения x и y точки {}', 2, *valid_value_pair_params)


def get_file(validate=True):
    path = input('\nВведите путь до файла: ').strip()

    if validate:
        while not valid_file(path):
            print('Файла не существует или он пустой')
            path = input('Повторите ввод: ').strip()

    return path


def get_data_from_console():
    n = get_points_number()
    return n, get_points(n)


def get_data_from_file():
    path = get_file()
    with open(path, 'r') as file:
        data = [line for line in file.read().splitlines() if line != '']
        matrix_size = data.pop(0)

        if not valid_value(matrix_size, *valid_points_number_params):
            print('Невалидное число точек. Убедитесь, что данное значение находится в начале файла')
            return get_data_from_file()

        matrix_size = int(matrix_size)

        if len(data) != matrix_size:
            print('Неверное кол-во строк в файле')
            print('Невалидное число точек. Кол-во точек в файле не совпадает')
            return get_data_from_file()

        matrix = [line.split() for line in data]
        row_size = 2

        if any(not valid_matrix_row(row, row_size, *valid_value_pair_params) for row in matrix):
            print('Невалидные значения в одной или в нескольких строках')
            return get_data_from_file()

        return matrix_size, [[float(val) for val in row] for row in matrix]


CONSOLE = 1
FILE = 2

input_output_modes = {
    CONSOLE: 'Консоль',
    FILE: 'Файл'
}

valid_io_id_params = (CONSOLE, FILE, False)


def print_input_modes():
    print_dictionary('Режимы ввода', input_output_modes)


def print_output_modes():
    print_dictionary('Режимы вывода', input_output_modes)


def get_input_id():
    return int(get_value('Выберите режим ввода', *valid_io_id_params))


def get_output_id():
    return int(get_value('Выберите режим вывода', *valid_io_id_params))


def print_table_to_console(name, table):
    print(f'\n{name}:')
    for row in table:
        for val in row:
            if row == table[0]:
                # print('{:4}'.format(val), end='\t')
                # print(f'{val:=4.5f}', end='\t')
                print(f'{val:>10}\t', end='')
            else:
                print(f'{round(val, 5):>10}\t', end='')
        print()


def print_matrix2(matrix, name):
    print(f'\n{name}:')
    for row in matrix:
        for val in row:
            if val == row[0]:
                print(f'{val}', end='\t')
            else:
                print(f'{val:=8.5f}', end='\t')
        print()


def print_results_to_console(results, errors, best):
    print('\nРезультаты аппроксимации:')

    for error in errors:
        print(error)

    for result in results:
        name, table1, table2 = result
        print(f'\n{name}:')
        for row in table1:
            for val in row:
                if val == row[0]:
                    print(f'{val}', end='\t')
                else:
                    print(f'{val:=8.5f}', end='\t')
            print()

        for val in table2:
            print(val)

    print(best)


def print_results_to_file(results, errors, best):
    path = get_file(validate=False)

    with open(path, 'w', encoding='utf-8') as file:
        file.write('Результаты аппроксимации:\n')

        for error in errors:
            file.write(f'{error}\n')

        for result in results:
            name, table1, table2 = result
            file.write(f'\n{name}:\n')
            for row in table1:
                for val in row:
                    if val == row[0]:
                        file.write(f'{val}\t')
                    else:
                        file.write(f'{val:=8.5f}\t')
                file.write('\n')

            for val in table2:
                file.write(f'{val}\n')

        file.write(f'{best}\n')


get_data_dict = {
    CONSOLE: get_data_from_console,
    FILE: get_data_from_file
}


def get_data(input_mode_id):
    return get_data_dict[input_mode_id]()


print_results_dict = {
    CONSOLE: print_results_to_console,
    FILE: print_results_to_file
}


def print_results(output_mode_id):
    return print_results_dict[output_mode_id]

