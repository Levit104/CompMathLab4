from matplotlib import pyplot as plt

from approximation import approximations_list
from io_handler import get_data, print_results
from util import linspace, dictionary_find_min, table_to_string

if __name__ == '__main__':
    while True:
        try:
            data = get_data()

            if data is None:
                continue

            x_values, y_values, n = data
            float_format = '.5f'
            result = ''
            dev_dict = {}

            plt.scatter(x_values, y_values, label='Исходные данные')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid()
            plt.title('Аппроксимация функции')

            for approximation in approximations_list:
                try:
                    phi, eps, dev_measure, dev, r = approximation(x_values, y_values, n)

                    table = [['x'] + x_values, ['y'] + y_values, ['ϕ'] + phi, ['ε'] + eps]

                    dev_dict[approximation.name] = dev

                    result += f'\n\n{approximation.name}:' \
                              f'\n{table_to_string(table, headers=[], float_format=float_format, show_index=False)}' \
                              f'\nФункция ϕ(x) = {approximation.function_string(float_format)}' \
                              f'\nМера отклонения S = {dev_measure:{float_format}}' \
                              f'\nСреднеквадратичное отклонение σ = {dev:{float_format}}'

                    if r is not None:
                        result += f'\nКоэффициент корреляции Пирсона r = {r:{float_format}}'

                    x_graph = linspace(min(x_values), max(x_values), 1000)
                    y_graph = [approximation.function(x) for x in x_graph]
                    plt.plot(x_graph, y_graph, label=approximation.name)

                except ValueError as e:
                    result += f'\n{approximation.name} аппроксимация невозможна'

            best_name, best_value = dictionary_find_min(dev_dict)
            result += f'\n\nЛучшая аппроксимация: {best_name}, σ = {best_value:{float_format}}'

            print_results(result)

            plt.legend()
            plt.show()

        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы")
            break
