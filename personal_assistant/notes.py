from datetime import datetime
from common import get_n_from_user
from prettytable import PrettyTable


class Note:
    instances: list = []
    def __init__(
            self,
            title: str,
            content: str

    ):
        for attr_name in ('title', 'content'):
            setattr(self, attr_name, eval(attr_name))
        self.timestamp = datetime.now()
        self.id: int = (self.instances[-1].id + 1) if self.instances else 1
        self.instances.append(self)

    def _get_timestamp_str(self) -> str:
        return self.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    timestamp_str = property(fget=_get_timestamp_str)

    def update(self, new_title: str, new_content: str) -> None:
        self.title: str = new_title
        self.content: str = new_content
        self.timestamp = datetime.now()


def notes_management() -> None:
    match (command_n := get_n_from_user(
        inp_msg='''\tВыберите действие над заметками:
\t\t1. Создание новой заметки.
\t\t2. Просмотр списка заметок.
\t\t3. Просмотр подробностей заметки.
\t\t4. Редактирование заметки.
\t\t5. Удаление заметки.
\t\t6. Импорт и экспорт заметок в формате CSV.
\tВведите номер действия: ''',
        first_n=1,
        last_n=6,
        input_mistake_msg='Ошибка ввода номера действия!'
    )):
        case 1:
            Note(
                title=input('\t\t\tВведите название новой заметки: '),
                content=input('\t\t\tВведите новую заметку: ')
            )
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
                            case 5:
                                del Note.instances[i]
                        # endregion
                        break
                else:
                    print(input_mistake_msg)
        case 6:
            pass
