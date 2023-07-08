from collections import deque


class CalculatorError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Calculator:
    def __init__(self) -> None:
        self.assignments: dict[str, int] = dict()
        self.answer: int = 0
        self.ops: set[str] = {"+", "-", "*", "/", "^"}
        self.paren: set[str] = {"(", ")"}

    def validated_assignment(self, x: str) -> int:
        try:
            return int(x)
        except ValueError:
            if not x.lstrip("-").isalpha():
                raise CalculatorError("Invalid assignment")
            else:
                if x not in self.assignments:
                    raise CalculatorError(f"Unknown variable {x}")
                elif x.startswith("-"):
                    return -self.assignments[x]
                else:
                    return self.assignments[x]

    @staticmethod
    def validated_identifier(x: str) -> str:
        if x.isalpha():
            return x
        else:
            raise CalculatorError("Invalid identifier")

    @staticmethod
    def valid_operator(string: str) -> bool:
        return bool(string) and all(map(lambda x: x in "+-", string))

    def simplified_operator(self, operator: str) -> str:
        if not self.valid_operator(operator):
            raise CalculatorError("Invalid expression")
        return "-" if operator.count("-") % 2 == 1 else "+"

    def processed_operand(self, x: str) -> int:
        try:
            return int(x)
        except ValueError:
            if not x.lstrip("-").isalpha():
                raise CalculatorError(f"Invalid expression {x}")
            else:
                if x not in self.assignments:
                    raise CalculatorError(f"Unknown variable {x}")
                elif x.startswith("-"):
                    return -self.assignments[x]
                else:
                    return self.assignments[x]

    def process_assignment(self, line: str):
        operands = line.replace(" ", "").split("=")
        if len(operands) > 2:
            raise CalculatorError("Invalid assignment")
        key, value = line.replace(" ", "").split("=")
        self.assignments[self.validated_identifier(key)] = self.validated_assignment(
            value
        )

    def evaluate_add_sub(self, line):
        expression = line.split()

        if len(expression) == 1:
            expression[0] = self.processed_operand(
                self.validated_identifier(expression[0])
            )

        elif len(expression) == 2:
            expression.insert(0, "0")

        while len(expression) > 2:
            operand_left = self.processed_operand(expression.pop(0))
            operator = self.simplified_operator(expression.pop(0))
            operand_right = self.processed_operand(expression.pop(0))

            if operator == "-":
                operand_right = -operand_right
            expression.insert(0, sum((operand_left, operand_right)))

        self.answer = int(expression.pop())

    def tokenize(self, line):
        line = line.replace(" ", "")
        tokens = deque()
        loop = True
        while loop:
            loop = False
            for ch in line:
                if ch in "+-*/^()":
                    a, b = line.split(ch, 1)
                    if a:
                        tokens.append(a)
                        tokens.append(ch)
                    else:
                        if ch == '-':
                            if not tokens:
                                continue
                            elif tokens[-1] == '-':
                                tokens.pop()
                                tokens.append('+')
                            elif tokens[-1] == '+':
                                tokens.pop()
                                tokens.append('-')
                            else:
                                continue
                        elif ch == '+':
                            pass
                        elif ch == '(':
                            tokens.append(ch)
                        elif ch == ')' and tokens and tokens[-1] == ')':
                            tokens.append(ch)
                        else:
                            raise CalculatorError("Invalid expression - invalid operator")
                    line = b
                    loop = True
                    break
        else:
            if line:
                tokens.append(line)
        return tokens

    def infix_to_postfix(self, line):
        priority = {"+": 0, "-": 0, "*": 1, "/": 1, "^": 2}
        result = deque()
        stack = deque()
        expression = self.tokenize(line)
        print(expression)
        for e in expression:
            if e in "+-*/^()":
                if e == "(":
                    stack.append(e)
                    continue
                # elif e == "-" and stack and stack[-1] == '(':
                #     result.append(1)
                #     stack.append("*")
                #     continue
                elif e == ")":
                    try:
                        while stack[-1] != "(":
                            result.append(stack.pop())
                        else:
                            stack.pop()
                        continue
                    except IndexError:
                        raise CalculatorError("Invalid expression - unmatched ')'")
                while stack and stack[-1] != "(" and priority[e] <= priority[stack[-1]]:
                    result.append(stack.pop())
                stack.append(e)
            else:
                result.append(self.processed_operand(e))
        if "(" in stack:
            raise CalculatorError("Invalid expression - unclosed '('")
        while stack:
            result.append(stack.pop())
        return result

    def evaluate_expression(self, line):
        operation = {"+": lambda a, b: a + b,
                     "-": lambda a, b: a - b,
                     "*": lambda a, b: a * b,
                     "/": lambda a, b: a // b,
                     "^": lambda a, b: a ** b}
        stack = deque()
        postfix = self.infix_to_postfix(line)
        print(postfix)
        while postfix:
            x = postfix.popleft()
            if x in operation:
                # b assigned fisrt as values get
                # extracted in reversed order with pop()
                b = stack.pop()
                a = stack.pop()
                stack.append(operation[x](a, b))
            else:
                stack.append(x)
            print(postfix)
            print(stack)
        self.answer = stack[0]


def stage1():
    num_list = [int(n) for n in input().split()]
    print(sum(num_list))


def stage2():
    while True:
        usr_input = input().strip()

        if usr_input == "/exit":
            print("Bye!")
            exit()

        if usr_input:
            num_list = map(int, usr_input.split())
            print(sum(num_list))


def stage3():
    while True:
        usr_input = input().strip()

        if usr_input == "/exit":
            print("Bye!")
            exit()

        elif usr_input == "/help":
            print("The program calculates the sum of numbers")

        elif usr_input:
            num_list = map(int, usr_input.split())
            print(sum(num_list))


def stage4():
    while True:
        usr_input = input().strip()

        if usr_input == "/exit":
            print("Bye!")
            exit()

        elif usr_input == "/help":
            print("The program calculates the sum of numbers")

        elif usr_input:
            expression = usr_input.split()

            while len(expression) > 2:
                operand_left = int(expression.pop(0))
                operator = "-" if expression.pop(0).count("-") % 2 == 1 else "+"
                if operator == "-":
                    operand_right = -int(expression.pop(0))

                else:
                    operand_right = int(expression.pop(0))

                expression.insert(0, sum((operand_left, operand_right)))

            print(int(expression.pop()))


def stage5():
    cal = Calculator()
    while True:
        usr_input = input().strip()

        try:
            if usr_input == "/exit":
                print("Bye!")
                exit()

            elif usr_input == "/help":
                print("The program calculates the sum of numbers")

            elif usr_input.startswith("/"):
                print("Unknown command")

            elif usr_input:
                expression = usr_input.split()

                if len(expression) == 1:
                    try:
                        expression[0] = int(expression[0])
                    except ValueError:
                        raise CalculatorError("Invalid expression")

                if len(expression) == 2:
                    expression.insert(0, "0")

                while len(expression) > 2:
                    operand_left = cal.processed_int(expression.pop(0))
                    operator = cal.simplified_operator(expression.pop(0))
                    operand_right = cal.processed_int(expression.pop(0))

                    if operator == "-":
                        operand_right = -operand_right
                    expression.insert(0, sum((operand_left, operand_right)))

                print(int(expression.pop()))

        except CalculatorError as err:
            print(err)


def stage6():
    cal = Calculator()
    while True:
        usr_input = input().strip()
        try:
            if usr_input == "/exit":
                print("Bye!")
                exit()
            elif usr_input == "/help":
                print("The program calculates the sum of numbers")
            elif usr_input.startswith("/"):
                print("Unknown command")
            elif usr_input:
                if "=" in usr_input:
                    cal.process_assignment(usr_input)
                    continue

                cal.evaluate_add_sub(usr_input)
                print(cal.answer)

        except CalculatorError as err:
            print(err)


def stage7():
    cal = Calculator()
    while True:
        usr_input = input().strip()
        try:
            if usr_input == "/exit":
                print("Bye!")
                exit()
            elif usr_input == "/help":
                print("The program calculates the sum of numbers")
            elif usr_input.startswith("/"):
                print("Unknown command")
            elif usr_input:
                if "=" in usr_input:
                    cal.process_assignment(usr_input)
                    continue

                cal.evaluate_expression(usr_input)
                print(cal.answer)

        except CalculatorError as err:
            print(err)


def main():
    stage7()


if __name__ == "__main__":
    main()
