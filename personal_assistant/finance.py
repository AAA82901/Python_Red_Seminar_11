from datetime import datetime, date
from json import load, dump
from csv import reader, writer
from os.path import exists
from prettytable import PrettyTable
from common import get_n_from_user


class FinRec:
    instances: list = []
    def __init__(
            self,
            id: int,
            amount: float,
            category: str,
            date: str,
            description: str
    ):
        for attr_name in (
            'id',
            'amount',
            'category',
            'date',
            'description'
        ):
            setattr(self, attr_name, eval(attr_name))
        self.instances.append(self)

    # region date
    def _get_date(self) -> str:
        return self._date.strftime('%d-%m-%Y')

    def _set_date(self, new_date: str) -> None:
        self._date: date = datetime.strptime(new_date, '%d-%m-%Y').date()

    date = property(fget=_get_date, fset=_set_date)
    #endregion


# region Работа с json-файлом
file_name: str = 'finance.json'


def save_all_in_json() -> None:
    global file_name
    lst_to_dump: list[dict] = [
        {
            attr_name: getattr(fr, attr_name)
            for attr_name in (
                'id',
                'amount',
                'category',
                'date',
                'description'
            )
        }
        for fr in FinRec.instances
    ]
    with open(file=file_name, mode='w', encoding='utf8') as file:
        dump(lst_to_dump, file)


if exists(file_name):
    with open(file=file_name, encoding='utf8') as file:
        for d in load(file):
            d['amount'] = float(d['amount'])
            FinRec(
                **{
                    attr_name: d[attr_name]
                    for attr_name in (
                        'id',
                        'amount',
                        'category',
                        'date',
                        'description'
                    )
                }
            )
else:
    # создание файла
    with open(file=file_name, mode='w', encoding='utf8') as file:
        file.write('[]')
# endregion


def finance_managemnet() -> None:
    match (command_n := get_n_from_user(
        inp_msg='''\tВыберите действие над финансовыми записями:
\t\t1. Добавление новой финансовой записи (доход > 0 или расход < 0).
\t\t2. Просмотр всех записей с возможностью фильтрации по дате или категории.
\t\t3. Генерация отчётов о финансовой активности за определённый период.
\t\t4. Импорт финансовых записей в формате CSV.
\t\t5. Экспорт финансовых записей в формате CSV.
\tВведите номер действия: ''',
        first_n=1,
        last_n=7,
        input_mistake_msg='Ошибка ввода номера действия!'
    )):
        case 1:
            FinRec(
                id=(FinRec.instances[-1].id + 1) if FinRec.instances else 1,
                amount=float(input('\t\tВведите сумму операции: ')),
                category=input('\t\tВведите категорию: '),
                date=input('\t\tВведите дату операции в формате ДД-ММ-ГГГГ: '),
                description=input('\t\tВведите описание операции: ')
            )
            save_all_in_json()
        case 2 | 3:
            our_fr_seq = FinRec.instances
            if command_n == 2:
                date_ = input('\t\tВведите дату, если хотите отфильтровать по дате, иначе пустую строку: ')
                category = input('\t\tВведите категорию, если хотите отфильтровать по категории, иначе пустую строку: ')
                if date_:
                    date_ = datetime.strptime(date_, '%d-%m-%Y').date()
                    our_fr_seq = filter(lambda fr: fr._date == date_, our_fr_seq)
                if category:
                    our_fr_seq = filter(lambda fr: fr.category == category, our_fr_seq)
            else:
                date1, date2 = (datetime.strptime(input(f'\t\tВведите {w}ую дату: '), '%d-%m-%Y').date() for w in ('перв', 'втор'))
                our_fr_seq = filter(lambda fr: date1 <= fr._date <= date2, our_fr_seq)
            our_fr_seq = tuple(our_fr_seq)
            if our_fr_seq:
                if FinRec.instances:
                    tbl = PrettyTable()
                    tbl.title = 'Список финансовых записей:'
                    tbl.field_names = ['ID', 'Сумма', 'Категория', 'Дата', 'Описание']
                    for fr in our_fr_seq:
                        tbl.add_row((
                            fr.id,
                            fr.amount,
                            fr.category,
                            fr.date,
                            fr.description
                        ))
                    print(tbl)
                else:
                    print('\t\tНет финансовых записей.')
            else:
                print('\t\tНет финансовых записей.')
        case 4:
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
                        start=(FinRec.instances[-1].id + 1) if FinRec.instances else 1
                ):
                    FinRec(
                        id=cur_id,
                        amount=row[1],
                        category=row[2],
                        date=row[3],
                        description=row[4]
                    )
                save_all_in_json()
        case 5:
            lst_to_dump: list = [
                ['id', 'amount', 'category', 'date', 'description']
            ] + [
                [
                    getattr(fr, attr_name)
                    for attr_name in ('id', 'amount', 'category', 'date', 'description')
                ]
                for fr in FinRec.instances
            ]
            # region Выбор csv-файла
            csv_file_name: str = input('\t\t\tВыберете имя/путь файла для экспорта: ')
            while not csv_file_name:
                print('\t\t\tОшибка. Вы ничего не ввели.')
                csv_file_name: str = input('\t\t\tВыберете имя/путь файла для экспорта: ')
            # endregion
            with open(file=csv_file_name, mode='w', encoding='utf8', newline='') as csvfile:
                writer(csvfile).writerows(lst_to_dump)
