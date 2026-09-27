import re
from tabnanny import process_tokens

operators = {
    '(': -1,
    ')': -1,
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 1,
}

def delSc(op, expression):
    for j in range(len(op) - 1, 0, -1):
        if op[j] == '(':
            op.pop(j)
            break
        expression.append(op[j])
        op.pop(j)

def tokenize(expression):
    expression = expression.replace(' ', '')
    tokens = re.findall(r'\d+\.\d*|\d+|[\+\-\*\/\(\)]', expression)
    if tokens[0] == '-':
        if tokens[1] == '(':
            tokens.insert(1, '*')
            tokens[0] = "-1"
        else:
            tokens[1] = tokens[0] + tokens[1]
            tokens.pop(0)
    if tokens[0] == '+':
        tokens = tokens[1:]
    for i in range(len(tokens)-2):
        if tokens[i] == "-":
            tokens[i+1] = tokens[i] + tokens[i+1]
            tokens.pop(i)
        if tokens[i] == "--":
            tokens[i] = "-"
            tokens[i+1] = tokens[i] + tokens[i+1]
    return tokens

def parse(tokens):
    op = ['(']
    expression = []
    for i in range(len(tokens)):
        if tokens[i] == ')':
            delSc(op, expression)
        elif tokens[i] == '(':
            op.append(tokens[i])
        elif tokens[i] in operators:
            if operators[tokens[i]] < operators[op[-1]]:
                for j in range(len(op)-1, 0, -1):
                    if operators[tokens[i]] <= operators[op[-1]]:
                        expression.append(op[-1])
                        op.pop(-1)
                    else:
                        break
                op.append(tokens[i])
            else:
                op.append(tokens[i])
        else:
            expression.append(tokens[i])
    delSc(op, expression)
    return expression

def calculation(expression):
    def multipop(j):
        expression.pop(j - 1)
        expression.pop(j - 2)
    while len(expression) > 1:
        for j in range(len(expression)):
            if expression[j] == '+':
                expression[j] = str(float(expression[j-1]) + float(expression[j-2]))
                multipop(j)
                break
            elif expression[j] == '-':
                expression[j] = str(float(expression[j-1]) - float(expression[j-2]))
                multipop(j)
                break
            elif expression[j] == '*':
                expression[j] = str(float(expression[j-1]) * float(expression[j-2]))
                multipop(j)
                break
            elif expression[j] == '/':
                expression[j] = str(float(expression[j-1]) / float(expression[j-2]))
                multipop(j)
                break
    return expression[0]


token = tokenize("3---90")
parsed  = parse(token)
expression = calculation(parsed)
print(expression)
