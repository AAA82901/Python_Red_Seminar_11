from os.path import exists
from json import load, dump
from csv import reader, writer
from common import get_n_from_user


class Contact:
    instances: list = []

    def __init__(
            self,
            id: int,
            name: str,
            phone: int,
            email: str
    ):
        for attr_name in (
            'id',
            'name',
            'phone',
            'email'
        ):
            setattr(self, attr_name, eval(attr_name))
        self.instances.append(self)


# region Работа с json-файлом
file_name: str = 'contacts.json'


def save_all_in_json() -> None:
    global file_name
    lst_to_dump: list[dict] = [
        {
            attr_name: getattr(c, attr_name)
            for attr_name in (
                'id',
                'name',
                'phone',
                'email'
            )
        }
        for c in Contact.instances
    ]
    with open(file=file_name, mode='w', encoding='utf8') as file:
        dump(lst_to_dump, file)


if exists(file_name):
    with open(file=file_name, encoding='utf8') as file:
        for d in load(file):
            Contact(
                **{
                    attr_name: d[attr_name]
                    for attr_name in (
                        'id',
                        'name',
                        'phone',
                        'email'
                    )
                }
            )
else:
    # создание файла
    with open(file=file_name, mode='w', encoding='utf8') as file:
        file.write('[]')
# endregion


def contacts_management() -> None:
    match command_n := get_n_from_user(
        inp_msg='''\tВыберите действие над контактами:
\t\t1. Добавление нового контакта.
\t\t2. Поиск контакта по имени.
\t\t3. Поиск контакта по телефону.
\t\t4. Редактирование контакта.
\t\t5. Удаление контакта.
\t\t6. Импорт контактов в формате CSV.
\t\t7. Экспорт контактов в формате CSV.
\tВведите номер действия: ''',
        first_n=1,
        last_n=7,
        input_mistake_msg='Ошибка ввода номера действия!'
    ):
        case 1:
            Contact(
                id=(Contact.instances[-1].id + 1) if Contact.instances else 1,
                name=input('\t\t\tВведите имя нового контакта: '),
                phone=int(input('\t\t\tВведите телефонный номер нового контакта (только цифры): ')),
                email=input('\t\t\tВведите email нового контакта: ')
            )
            save_all_in_json()
        case 2 | 3:
            attr_name, attr_name_for_user, attr_name_for_user2 = \
                ('name', 'имя', 'именем') if command_n == 2 else \
                ('phone', 'телефонный номер', 'телефонным номером')

            attr_value: str = input(f'\t\t\tВведите {attr_name_for_user} искомого контакта: ')
            if command_n == 3:
                attr_value = int(attr_value)
            for c in Contact.instances:
                if getattr(c, attr_name) == attr_value:
                    # region Действие над найденным контактом
                    print(
                         '\t\t\t\tНайденный контакт:\n'
                        f'\t\t\t\t\tID: {c.id}\n'
                        f'\t\t\t\t\tимя: {c.name}\n'
                        f'\t\t\t\t\tтелефонный номер: {c.phone}\n'
                        f'\t\t\t\t\temail: {c.email}'
                    )
                    # endregion
                    break
            else:
                print(f'\t\t\tНе найден контакт с {attr_name_for_user2} "{attr_value}".')
        case 4 | 5:
            id_: int = int(input('Введите ID искомого контакта: '))
            for i, c in enumerate(Contact.instances):
                if c.id == id_:
                    # region Действие над найденным контактом
                    match command_n:
                        case 4:
                            c.name: str = input('Введите новое имя контакта: ')
                            c.phone: str = int(input('Введите новый телефонный номер контакта: '))
                            c.email: str = input('Введите новый email контакта: ')
                        case 5:
                            del Contact.instances[i]
                    save_all_in_json()
                    # endregion
                    break
            else:
                print(f'\t\t\tНе найден контакт с ID "{id_}".')
        case 6:
            # region Выбор csv-файла
            csv_file_name: str = input('\t\t\tВыберете имя/путь файла для импорта: ')
            while not exists(csv_file_name):
                print('\t\t\tОшибка. Такого файла нет.')
                csv_file_name: str = input('\t\t\tВыберете имя/путь файла для импорта: ')
            # endregion
            with open(file=csv_file_name, mode='r', encoding='utf8') as csvfile:
                csvreader = reader(csvfile)
                next(csvreader)  # избавляемся от заголовка
                for cur_id, row in enumerate(
                        csvreader,
                        start=(Contact.instances[-1].id + 1) if Contact.instances else 1
                ):
                    Contact(
                        **{'id': cur_id} | {
                            attr_name: row[i]
                            for i, attr_name in enumerate(('name', 'phone', 'email'), start=1)
                        }
                    )
                save_all_in_json()
        case 7:
            lst_to_dump: list = [
                ['id', 'name', 'phone', 'email']
            ] + [
                [getattr(c, attr_name) for attr_name in ('id', 'name', 'phone', 'email')]
                for c in Contact.instances
            ]
            # region Выбор csv-файла
            csv_file_name: str = input('\t\t\tВыберете имя/путь файла для экспорта: ')
            while not csv_file_name:
                print('\t\t\tОшибка. Вы ничего не ввели.')
                csv_file_name: str = input('\t\t\tВыберете имя/путь файла для экспорта: ')
            # endregion
            with open(file=csv_file_name, mode='w', encoding='utf8', newline='') as csvfile:
                writer(csvfile).writerows(lst_to_dump)
