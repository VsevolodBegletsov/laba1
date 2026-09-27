import re
import argparse

operators = {
    '(': -1,
    ')': -1,
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
    '//': 1,
    '%': 1
}

def validation(expression):
    #Замена пробелов
    expression = expression.replace(' ', '')

    #Приведение знаков к одному типу
    expression = expression.replace(',', '.')
    expression = expression.replace(':', '/')

    #Обработка отрицательных скобок
    if expression[:2] == '-(':
        expression = expression.replace('-(', '-1*(', 1)

    #Проверка на то, что введены минимум два числа
    if len(re.findall(r'\d+[\+\-\*\/\(\)\%]\d+|\d+\.\d+[\+\-\*\/\(\)\%]\d+\.\d+', expression))==0:
        raise ValueError("Введено некорректное математическое выражение или строка пуста")

    #Обработка унарного +
    for i in ['+', '-', '*', '/', '%', '(']:
        expression = expression.replace(i+"+", i)

    # Обработка унарного + в начале строки
    if expression[0] == '+':
        expression = expression[1:]

    #Проверка последнего символа
    if expression[-1] in '.+-*/%(':
        raise ValueError("Недопустимое окончание выражения")

    #Проверка дробных чисел
    if expression[0] == '.':
        raise ValueError("Неверно введено число с плавающей точкой")
    for i in operators:
        if expression.count(i+".")>0:
            raise ValueError("Неверно введено число с плавающей точкой")

    #Проверка количества операторов
    for i in ['+', '-', '/']:
        if expression.count(i*3) > 0:
            raise ValueError("Обнаружено недопустимое кол-во операторов")

    for i in ['*', '%', '.']:
        if expression.count(i*2) > 0:
            raise ValueError("Обнаружено недопустимое кол-во операторов")

    #Проверка количества скобок
    if expression.count('(') != expression.count(')'):
        print(expression.count('('), expression.count(')'))
        raise ValueError("Обнаружено недопустимое кол-во операторов")

    #Проверка на посторонние символы
    for i in expression:
        if i not in "0123456789.+-*/%()":
            raise ValueError("Обнаружены недопустимые значения")
    return expression

def tokenization(expression):
    #Валидация
    expression = validation(expression)
    if expression:
        #Создание массива токенов регулярным выражением
        tokens = re.findall(r'\d+\.\d+|\d+|[\+\-\*\/\(\)\%]', expression)
        for i in range(len(tokens)-2):
            # Формирование токенов с унарным минусом
            for j in ['+', '-', '*', '/', '%', '(']:
                if tokens[i] + tokens[i+1] == j+"-":
                    tokens[i+2] = tokens[i+1] + tokens[i+2]
                    tokens.pop(i+1)
            # Формирование токена целочисленного деления
            if tokens[i] == '/' and tokens[i+1] == '/':
                tokens[i] = '//'
                tokens.pop(i+1)
        return tokens
    return False

def parse(tokens):

    #Функция опустошения стека до определённого значения
    def delSc(op, expression):
        for j in range(len(op) - 1, 0, -1):
            if op[j] == '(':
                op.pop(j)
                break
            expression.append(op[j])
            op.pop(j)

    op = ['(']
    expression = []
    for i in range(len(tokens)):
        # Попадание в стек ")" выкидывает на строку всё, что лежит в стеке до ")"
        if tokens[i] == ')':
            delSc(op, expression)
        # Простое добавление "(" в стек
        elif tokens[i] == '(':
            op.append(tokens[i])
        # Распределение остальных операторов
        elif tokens[i] in operators:
            # Если приоритет оператора меньше предыдущего, лежащего в стеке, всё, что лежит в стеке с большим приоритетом запихивается в строку, иначе оператор просто добавляется в стек
            if operators[tokens[i]] <= operators[op[-1]]:
                for j in range(len(op)-1, 0, -1):
                    if operators[tokens[i]] <= operators[op[-1]]:
                        expression.append(op[-1])
                        op.pop(-1)
                    else:
                        break
                op.append(tokens[i])
            else:
                op.append(tokens[i])
        # Запись чисел в строку
        else:
            expression.append(tokens[i])
    # Опустошение стека
    delSc(op, expression)
    return expression

# Я это если что устно объясню ей-богу
def calculation(expression):
    def multipop(j):
        expression.pop(j - 1)
        expression.pop(j - 2)
    while len(expression) > 1:
        for j in range(len(expression)):
            if expression[j] == '+':
                expression[j] = str(float(expression[j-2]) + float(expression[j-1]))
                multipop(j)
                break
            elif expression[j] == '-':
                expression[j] = str(float(expression[j-2]) - float(expression[j-1]))
                multipop(j)
                break
            elif expression[j] == '*':
                expression[j] = str(float(expression[j-2]) * float(expression[j-1]))
                multipop(j)
                break
            elif expression[j] == '/':
                expression[j] = str(float(expression[j-2]) / float(expression[j-1]))
                multipop(j)
                break
            elif expression[j] == '//':
                expression[j] = str(float(expression[j-2]) // float(expression[j-1]))
                multipop(j)
                break
            elif expression[j] == '%':
                expression[j] = str(float(expression[j-2]) % int(expression[j-1]))
                multipop(j)
                break
    return expression[0]

# Пользуйтесь, батюшка
def evaluate(expression):
    token = tokenization(expression)
    if token:

        parsed = parse(token)
        return calculation(parsed)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="toolkit calc",
        description="Вычислить математическое выражение",
    )
    parser.add_argument(
        "expression",
        type=str,
        help='Математическое выражение, например: "2+2*2"',
    )
    return parser


def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        result = evaluate(args.expression)
    except Exception as e:
        print(f"Ошибка: {e}")
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())