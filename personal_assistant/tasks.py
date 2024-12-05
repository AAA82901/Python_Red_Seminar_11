from datetime import datetime, date
from os.path import exists
from json import load, dump
from csv import reader, writer
from common import get_n_from_user
from prettytable import PrettyTable


class Task:
    instances: list = []
    def __init__(
            self,
            id: int,
            title: str,
            description: str,
            done: bool,
            priority: str,
            due_date: str
    ):
        for attr_name in (
                'id',
                'title',
                'description',
                'done',
                'priority',
                'due_date'
        ):
            setattr(self, attr_name, eval(attr_name))
        self.instances.append(self)

    # region priority
    priority_possible_values: tuple[str, str, str] = ('Высокий', 'Средний', 'Низкий')

    def _get_priority(self) -> str:
        return self.priority_possible_values[self.priority_i]

    def _set_priority(self, new_priority: str) -> None:
        self.priority_i: int = self.priority_possible_values.index(new_priority)

    priority = property(fget=_get_priority, fset=_set_priority)
    #endregion

    # region due_date
    def _get_due_date(self) -> str:
        return self._due_date.strftime('%d-%m-%Y')

    def _set_due_date(self, new_due_date: str) -> None:
        self._due_date: date = datetime.strptime(new_due_date, '%d-%m-%Y').date()

    due_date = property(fget=_get_due_date, fset=_set_due_date)
    #endregion


# region Работа с json-файлом
file_name: str = 'tasks.json'


def save_all_in_json() -> None:
    global file_name
    lst_to_dump: list[dict] = [
        {
            'id': task.id,  # int
            'title': task.title,  # str
            'description': task.description,  # str
            'done': int(task.done),  # int
            'priority': task.priority,  # str
            'due_date': task.due_date  # str
        }
        for task in Task.instances
    ]
    with open(file=file_name, mode='w', encoding='utf8') as file:
        dump(lst_to_dump, file)


if exists(file_name):
    with open(file=file_name, encoding='utf8') as file:
        for d in load(file):
            d['done'] = bool(d['done'])
            Task(
                **{
                    attr_name: d[attr_name]
                    for attr_name in (
                        'id',
                        'title',
                        'description',
                        'done',
                        'priority',
                        'due_date'
                    )
                }
            )
else:
    # создание файла
    with open(file=file_name, mode='w', encoding='utf8') as file:
        file.write('[]')
# endregion


def tasks_management() -> None:
    match (command_n := get_n_from_user(
        inp_msg='''\tВыберите действие над задачами:
\t\t1. Добавление новой задачи.
\t\t2. Просмотр списка задач с отображением статуса, приоритета и срока.
\t\t3. Отметка задачи как выполненной.
\t\t4. Редактирование задачи.
\t\t5. Удаление задачи.
\t\t6. Импорт задач в формате CSV.
\t\t7. Экспорт задач в формате CSV.
\tВведите номер действия: ''',
        first_n=1,
        last_n=7,
        input_mistake_msg='Ошибка ввода номера действия!'
    )):
        case 1:
            Task(
                id=(Task.instances[-1].id + 1) if Task.instances else 1,
                title=input('\t\tВведите название новой задачи: '),
                description=input('\t\tВведите описание новой задачи: '),
                done=bool(int(input('\t\tВведите статус новой задачи (0 - не выполнена; 1 - выполнена): '))),
                priority=input('\t\tВведите приоритет новой задачи («Высокий», «Средний», «Низкий»): '),
                due_date=input('\t\tВведите срок выполнения новой задачи в формате ДД-ММ-ГГГГ: ')
            )
            save_all_in_json()
        case 2:
            if Task.instances:
                tbl = PrettyTable()
                tbl.title = 'Список задач:'
                tbl.field_names = ['ID', 'Название', 'Описание', 'Статус', 'Приоритет', 'Срок выполнения']
                for task in Task.instances:
                    tbl.add_row((
                        task.id,
                        task.title,
                        task.description,
                        ('В' if task.done else 'Не в') + 'ыполнено',
                        task.priority,
                        task.due_date
                    ))
                print(tbl)
            else:
                print('\t\tНет задач.')
        case 3 | 4 | 5:
            input_mistake_msg: str = '\t\t\tВведён неверный id задачи!'
            continue_input: bool = True
            while continue_input:
                task_id: int = get_n_from_user(
                    inp_msg='\t\t\tВведите id задачи: ',
                    first_n=Task.instances[0].id,
                    last_n=Task.instances[-1].id,
                    input_mistake_msg=input_mistake_msg
                )
                for i in range(len(Task.instances)):
                    if Task.instances[i].id == task_id:
                        continue_input: bool = False
                        # region Действие над найденной задачей
                        match command_n:
                            case 3:
                                Task.instances[i].done: bool = True
                            case 4:
                                Task.instances[i].title=input('\t\tВведите новое название задачи: ')
                                Task.instances[i].description=input('\t\tВведите новое описание  задачи: ')
                                Task.instances[i].done=bool(int(input('\t\tВведите новый статус задачи (0 - не выполнена; 1 - выполнена): ')))
                                Task.instances[i].priority=input('\t\tВведите новый приоритет задачи («Высокий», «Средний», «Низкий»): ')
                                Task.instances[i].due_date=input('\t\tВведите новый срок выполнения задачи в формате ДД-ММ-ГГГГ: ')
                            case 5:
                                del Task.instances[i]
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
                for cur_id, row in enumerate(
                        csvreader,
                        start=(Task.instances[-1].id + 1) if Task.instances else 1
                ):
                    Task(
                        id=cur_id,
                        title=row[1],
                        description=row[2],
                        done=bool(row[3]),
                        priority=row[4],
                        due_date=row[5]
                    )
                save_all_in_json()
        case 7:
            lst_to_dump: list = [
                ['id', 'title', 'description', 'done', 'priority', 'due_date']
            ] + [
                [
                    task.id,
                    task.title,
                    task.description,
                    int(task.done),
                    task.priority,
                    task.due_date
                ]
                for task in Task.instances
            ]
            # region Выбор csv-файла
            csv_file_name: str = input('\t\t\tВыберете имя/путь файла для экспорта: ')
            while not csv_file_name:
                print('\t\t\tОшибка. Вы ничего не ввели.')
                csv_file_name: str = input('\t\t\tВыберете имя/путь файла для экспорта: ')
            # endregion
            with open(file=csv_file_name, mode='w', encoding='utf8', newline='') as csvfile:
                writer(csvfile).writerows(lst_to_dump)
