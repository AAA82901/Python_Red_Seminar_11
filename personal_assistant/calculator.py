from string import digits


def calculator() -> None:
    exp = input('Введите выражение (без пробелов): ')
    if frozenset(exp) <= (frozenset(digits+'.+-*/%()') | frozenset({'//', '**'})):
        try:
            res: float | int = eval(exp)
        except ZeroDivisionError | SyntaxError:
            print('Ошибка ввода выражения')
        else:
            print('Результат:', res)
    else:
        print('Ошибка ввода выражения')
