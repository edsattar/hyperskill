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


def valid_operand(data: str | int) -> bool:
    try:
        int(data)
    except ValueError:
        return False
    return True


def valid_expression(left, op, right) -> bool:
    return all((valid_operand(left), valid_operator(op), valid_operand(right)))


class Calculator:
    def __init__(self):
        self.assignments = dict()

    def valid_operand(self, data: str | int) -> bool:
        try:
            int(data)
        except ValueError:
            return False
        return True

    def process_operand(self, x):
        try:
            return int(x)
        except ValueError:
            if not x.lstrip("-").isalpha():
                raise CalculatorError
            else:
                if x.startswith("-"):
                    return -self.assignments[x]
                else:
                    return self.assignments[x]


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
                    if not valid_operand(expression[0]):
                        raise InvalidExpressionError

                if len(expression) == 2:
                    expression.insert(0, "0")

                while len(expression) > 2:
                    if not valid_expression(*expression[:3]):
                        raise InvalidExpressionError

                    operand_left = int(expression.pop(0))
                    operator = simplify_operator(expression.pop(0))
                    operand_right = int(expression.pop(0))

                    if operator == "-":
                        operand_right = -operand_right
                    expression.insert(0, sum((operand_left, operand_right)))

                print(int(expression.pop()))

        except InvalidExpressionError:
            print("Invalid expression")


def stage6():
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
                    # def assignment
                    assignments = {}
                    print("assign")
                    key, value = usr_input.replace(" ", "").split("=")
                    if not key.isalpha():
                        print("Invalid identifier")
                        continue

                    assignments[key] = value

                    print(assignments)

                    continue

                expression = usr_input.split()

                if len(expression) == 1:
                    if not valid_operand(expression[0]):
                        raise InvalidExpressionError

                if len(expression) == 2:
                    expression.insert(0, "0")

                while len(expression) > 2:
                    if not valid_expression(*expression[:3]):
                        raise InvalidExpressionError

                    operand_left = int(expression.pop(0))
                    operator = simplify_operator(expression.pop(0))
                    operand_right = int(expression.pop(0))

                    if operator == "-":
                        operand_right = -operand_right
                    expression.insert(0, sum((operand_left, operand_right)))

                print(int(expression.pop()))

        except InvalidExpressionError:
            print("Invalid expression")


def main():
    stage6()


if __name__ == "__main__":
    main()
