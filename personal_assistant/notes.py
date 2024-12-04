from datetime import datetime
from os.path import exists
from json import load, dump
from csv import reader, writer
from common import get_n_from_user
from prettytable import PrettyTable


class Note:
    instances: list = []
    def __init__(
            self,
            id: int,
            title: str,
            content: str,
            timestamp: datetime
    ):
        for attr_name in ('id', 'title', 'content', 'timestamp'):
            setattr(self, attr_name, eval(attr_name))
        self.instances.append(self)

    def _get_timestamp_str(self) -> str:
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    timestamp_str = property(fget=_get_timestamp_str)

    def update(self, new_title: str, new_content: str) -> None:
        self.title: str = new_title
        self.content: str = new_content
        self.timestamp = datetime.now()


# region Работа с файлом
file_name: str = 'notes.json'


def save_all_in_json() -> None:
    global file_name
    lst_to_dump: list[dict] = [
        {
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'timestamp': note.timestamp_str
        }
        for note in Note.instances
    ]
    with open(file=file_name, mode='w', encoding='utf8') as file:
        dump(lst_to_dump, file)


if exists(file_name):
    with open(file=file_name, encoding='utf8') as file:
        for d in load(file):
            d['timestamp'] = datetime.strptime(d['timestamp'], '%Y-%m-%d %H:%M:%S')
            Note(
                **{
                    attr_name: d[attr_name]
                    for attr_name in ('id', 'title', 'content', 'timestamp')
                }
            )
else:
    # создание файла
    with open(file=file_name, mode='w', encoding='utf8') as file:
        file.write('[]')
# endregion


def notes_management() -> None:
    match (command_n := get_n_from_user(
        inp_msg='''\tВыберите действие над заметками:
\t\t1. Создание новой заметки.
\t\t2. Просмотр списка заметок.
\t\t3. Просмотр подробностей заметки.
\t\t4. Редактирование заметки.
\t\t5. Удаление заметки.
\t\t6. Импорт заметок в формате CSV.
\t\t7. Экспорт заметок в формате CSV.
\tВведите номер действия: ''',
        first_n=1,
        last_n=7,
        input_mistake_msg='Ошибка ввода номера действия!'
    )):
        case 1:
            Note(
                id=(Note.instances[-1].id + 1) if Note.instances else 1,
                title=input('\t\t\tВведите название новой заметки: '),
                content=input('\t\t\tВведите новую заметку: '),
                timestamp=datetime.now()
            )
            save_all_in_json()
        case 2:
            if Note.instances:
                tbl = PrettyTable()
                tbl.title = 'Список заметок:'
                tbl.field_names = ['ID', 'Название', 'Заметка', 'Дата и время создания/последнего изменения']
                for note in Note.instances:
                    tbl.add_row((note.id, note.title, note.content, note.timestamp_str))
                print(tbl)
            else:
                print('Нет заметок.')
        case 3 | 4 | 5:
            input_mistake_msg: str = '\t\t\tВведён неверный id заметки!'
            continue_input: bool = True
            while continue_input:
                note_id: int = get_n_from_user(
                    inp_msg='\t\t\tВведите id заметки: ',
                    first_n=Note.instances[0].id,
                    last_n=Note.instances[-1].id,
                    input_mistake_msg=input_mistake_msg
                )
                for i in range(len(Note.instances)):
                    if Note.instances[i].id == note_id:
                        continue_input: bool = False
                        # region Действие над найденной заметкой
                        match command_n:
                            case 3:
                                print(
                                     '\t\t\t\tПодробности заметки:\n'
                                    f'\t\t\t\t\tНазвание: {Note.instances[i].title}\n'
                                    f'\t\t\t\t\tЗаметка: {Note.instances[i].content}\n'
                                    f'\t\t\t\t\tДата и время создания/последнего изменения: {Note.instances[i].content}'
                                )
                            case 4:
                                Note.instances[i].update(
                                    new_title=input('\t\t\tВведите название новой заметки: '),
                                    new_content=input('\t\t\tВведите новую заметку: ')
                                )
                                save_all_in_json()
                            case 5:
                                del Note.instances[i]
                                save_all_in_json()
                        # endregion
                        break
                else:
                    print(input_mistake_msg)
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
                cur_id = (Note.instances[-1].id + 1) if Note.instances else 1
                for row in csvreader:
                    Note(
                        id=cur_id,
                        title=row[1],
                        content=row[2],
                        timestamp=datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                    )
                save_all_in_json()
        case 7:
            lst_to_dump: list = [
                ['id', 'title', 'content', 'timestamp']
            ] + [
                [getattr(note, attr_name) for attr_name in ('id', 'title', 'content', 'timestamp_str')]
                for note in Note.instances
            ]
            # region Выбор csv-файла
            csv_file_name: str = input('\t\t\tВыберете имя/путь файла для экспорта: ')
            while not csv_file_name:
                print('\t\t\tОшибка. Вы ничего не ввели.')
                csv_file_name: str = input('\t\t\tВыберете имя/путь файла для экспорта: ')
            # endregion
            with open(file=csv_file_name, mode='w', encoding='utf8', newline='') as csvfile:
                writer(csvfile, ).writerows(lst_to_dump)
