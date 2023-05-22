from solver import print_show_results
from approximation import approximate
from functions import functions_list
from console import print_input_modes, print_output_modes, get_input_id, get_output_id, get_data


if __name__ == '__main__':
    while True:
        try:
            print('\nЧтобы выйти из программы введите exit на любом этапе')

            print_input_modes()
            input_id = get_input_id()

            points_number, points = get_data(input_id)

            print_show_results(points, points_number)

        except (EOFError, KeyboardInterrupt):
            print("\nВыход из программы")
            break
