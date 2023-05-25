import matplotlib.pyplot as plt

from approximation import approximate
from functions import functions_list
from console import print_output_modes, get_output_id, print_results
from util import has_duplicates


def get_xy(points):
    x_values = []
    y_values = []
    for row in points:
        x_values.append(row[0])
        y_values.append(row[1])
    return x_values, y_values


def draw_initial_data(x, y):
    plt.scatter(x, y, label='Исходные данные')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid()
    plt.title('Аппроксимация функции')


def show_one(x, y, phi, name):
    draw_initial_data(x, y, )
    plt.plot(x, phi, label=name, color='red')
    plt.legend()
    plt.show()


def linspace(a, b, n):
    delta = (b - a) / (n - 1)
    return [a + i * delta for i in range(n)]


def print_show_results(points, points_number):
    x_values, y_values = get_xy(points)

    if has_duplicates(x_values):
        print('\nЗначения X должны быть уникальными. Повторите ввод')
        return

    print_output_modes()
    output_id = get_output_id()

    results = []
    errors = ['']

    best_value = float('inf')
    best_name = ''

    draw_initial_data(x_values, y_values)

    for function in functions_list:
        try:
            table1, table2, phi, dev = approximate(x_values, y_values, points_number, function)

            results.append((function.name, table1, table2))

            # show_one(x, y, phi, function.name)
            # plt.plot(x_values, phi, label=function.name)
            x_graph = linspace(min(x_values), max(x_values), 1000)
            y_graph = [function(x) for x in x_graph]
            plt.plot(x_graph, y_graph, label=function.name)

            if dev < best_value:
                best_value = dev
                best_name = function.name

        except ValueError:
            errors.append(f'{function.name} аппроксимация невозможна')

    best = f'\nЛучшая аппроксимация: {best_name}, σ = {round(best_value, 5)}'

    print_results(output_id)(results, errors, best)

    plt.legend()
    plt.show()
