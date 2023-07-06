class InvalidExpressionError(Exception):
    pass


class CalculatorError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


def any_digit(string: str) -> bool:
    return any(map(str.isdigit, string))


def simplify_operator(operators: str) -> str:
    return "-" if operators.count("-") % 2 == 1 else "+"


def valid_operator(string: str) -> bool:
    return bool(string) and all(map(lambda x: x in "+-", string))


def processed_int(data: str | int) -> int:
    try:
        return int(data)
    except ValueError:
        raise CalculatorError("Invalid expression")


def valid_expression(left, op, right) -> bool:
    return all((processed_int(left), valid_operator(op), processed_int(right)))


class Calculator:
    def __init__(self) -> None:
        self.assignments: dict[str, int] = dict()
        self.answer: int = 0

    @staticmethod
    def processed_int(data: str | int) -> int:
        try:
            return int(data)
        except ValueError:
            raise CalculatorError("Invalid expression")

    @staticmethod
    def valid_identifier(x):
        return x.isalpha()

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
                raise CalculatorError("Invalid expression")
            else:
                if x not in self.assignments:
                    raise CalculatorError(f"Unknown variable {x}")
                elif x.startswith("-"):
                    return -self.assignments[x]
                else:
                    return self.assignments[x]

    def process_assignment(self, line: str):
        key, value = line.replace(" ", "").split("=")
        if self.valid_identifier(key):
            self.assignments[key] = int(value)

    def evaluate_expression(self, line):
        expression = line.split()

        if len(expression) == 1:
            if self.valid_identifier(expression[0]):
                expression[0] = self.processed_operand(expression[0])
            else:
                raise CalculatorError("Invalid identifier")

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

                if simplify_operator(expression.pop(0)) == "-":
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
                    expression[0] = cal.processed_int(expression[0])

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

                cal.evaluate_expression(usr_input)
                print(cal.answer)

        except CalculatorError as err:
            print(err)


def main():
    stage6()


if __name__ == "__main__":
    main()
