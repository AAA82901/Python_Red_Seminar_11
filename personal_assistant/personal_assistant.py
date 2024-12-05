from common import get_n_from_user
from notes import notes_management
from tasks import tasks_management
from contacts import contacts_management
from calculator import calculator


print('Добро пожаловать в Персональный помощник!\n\n')


def input_command() -> int:
    return get_n_from_user(
        inp_msg='''Выберите действие:
\t1. Управление заметками
\t2. Управление задачами
\t3. Управление контактами
\t4. Управление финансовыми записями
\t5. Калькулятор
\t6. Выход
Введите номер действия: ''',
        first_n=1,
        last_n=6,
        input_mistake_msg='Ошибка ввода номера действия!'
    )


command_n: int = input_command()
while command_n != 6:
    match command_n:
        case 1:
            notes_management()
        case 2:
            tasks_management()
        case 3:
            contacts_management()
        case 4:
            pass
        case 5:
            calculator()
    print()
    command_n: int = input_command()
