print('Добро пожаловать в Персональный помощник!')
welcome_msg: str = '''Выберите действие:
\t1. Управление заметками
\t2. Управление задачами
\t3. Управление контактами
\t4. Управление финансовыми записями
\t5. Калькулятор
\t6. Выход
Введите номер действия: '''


def get_command_n_from_user() -> int:
    inp = input(welcome_msg)
    while not inp.isdigit() or (inp := int(inp)) < 1 or 6 < inp:
        print('Ошибка ввода номера действия!')
        inp = input(welcome_msg)
    return inp


command_n: int = get_command_n_from_user()
while command_n != 6:
    print('Выбранное действие:', command_n)
    command_n: int = get_command_n_from_user()
