class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Invalid expression")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


def precedence(operator):
    if operator in ('+', '-'):
        return 1
    elif operator in ('*', '/'):
        return 2
    return 0


def calculate(a, b, operator):
    if operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def tokenize(expression):
    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if char.isdigit() or char == '.':
            number = char
            while i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                i += 1
                number += expression[i]
            tokens.append(number)

        elif char == '-' and (len(tokens) == 0 or tokens[-1] in ['+', '-', '*', '/', '(']):
            number = '-'
            while i + 1 < len(expression) and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                i += 1
                number += expression[i]
            tokens.append(number)

        elif char in '+-*/()':
            tokens.append(char)

        else:
            raise ValueError("Invalid character: " + char)

        i += 1

    return tokens


def apply_top_operator(values, operators):
    operator = operators.pop()
    b = values.pop()
    a = values.pop()
    values.push(calculate(a, b, operator))


def evaluate_expression(expression):
    values = Stack()
    operators = Stack()

    for token in tokenize(expression):

        if token not in ['+', '-', '*', '/', '(', ')']:
            values.push(float(token))

        elif token == '(':
            operators.push(token)

        elif token == ')':
            while not operators.is_empty() and operators.peek() != '(':
                apply_top_operator(values, operators)
            if operators.is_empty():
                raise ValueError("Mismatched parentheses")
            operators.pop()

        else:
            while (not operators.is_empty()
                   and operators.peek() != '('
                   and precedence(operators.peek()) >= precedence(token)):
                apply_top_operator(values, operators)
            operators.push(token)

    while not operators.is_empty():
        if operators.peek() == '(':
            raise ValueError("Mismatched parentheses")
        apply_top_operator(values, operators)

    if values.size() != 1:
        raise ValueError("Invalid expression")

    result = values.pop()

    if result == int(result):
        return str(int(result))
    return str(round(result, 4))


def process_file():
    try:
        with open("input.txt", "r", encoding="utf-8-sig") as input_file:
            lines = input_file.readlines()

        results = []

        for line in lines:
            expression = line.strip()

            if expression == "":
                results.append("")

            elif set(expression) == {'-'} and len(expression) >= 3:
                results.append(expression)

            else:
                try:
                    answer = evaluate_expression(expression)
                    print(expression, "=", answer)
                    results.append(answer)
                except Exception as error:
                    print(expression, "=", "ERROR:", error)
                    results.append("ERROR: " + str(error))

        with open("output.txt", "w") as output_file:
            output_file.write("\n".join(results) + "\n")

        print("\nCalculations completed.")
        print("Results have been saved in output.txt")

    except FileNotFoundError:
        print("ERROR: input.txt was not found.")


if __name__ == "__main__":
    process_file()