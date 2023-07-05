def any_digit(string: str) -> bool:
    return any(map(str.isdigit, string))


def simplify_operator(operators: str) -> str:
    return "-" if operators.count("-") % 2 == 1 else "+"


def valid_operator(string: str) -> bool:
    return bool(string) and all(map(lambda x: x in "+-", string))


def valid_operand(data: str | int) -> bool:
    return True if type(data) is int else data.lstrip("-").isdigit()


def valid_expression(left, op, right) -> bool:
    return all((valid_operand(left), valid_operator(op), valid_operand(right)))


def stage1():
    num_list = [int(n) for n in input().split()]
    print(sum(num_list))


def stage2():
    while (usr_input := input().strip()) != "/exit":
        if usr_input:
            num_list = map(int, usr_input.split())
            print(sum(num_list))
    print("Bye!")


def stage3():
    while (usr_input := input().strip()) != "/exit":
        if usr_input == "/help":
            print("The program calculates the sum of numbers")
        elif usr_input:
            num_list = map(int, usr_input.split())
            print(sum(num_list))
    print("Bye!")


def stage4():
    while (usr_input := input().strip()) != "/exit":
        if usr_input == "/help":
            print("The program calculates the sum of numbers")
        elif usr_input:
            expression = usr_input.split()
            while len(expression) > 2:
                operand_left = int(expression.pop(0))
                if simplify_operators(expression.pop(0)) == "-":
                    operand_right = -int(expression.pop(0))
                else:
                    operand_right = int(expression.pop(0))
                expression.insert(0, sum((operand_left, operand_right)))
            print(expression.pop())
    print("Bye!")


def stage5():
    while (usr_input := input().strip()) != "/exit":
        if usr_input.startswith("/"):
            if usr_input == "/help":
                print("The program calculates the sum of numbers")
            else:
                print("Unknown command")
        elif usr_input:
            expression = usr_input.split()
            # print(int(expression.pop(0)))

            print(expression[:3])
            # if len(expression) == 1:
                # if not valid_operand(expression[0]):
                    # print("Invalid expression")
            if len(expression) == 2:
                print("Invalid expression")
            while len(expression) > 2:
                # operand_left = expression.pop(0)
                # operator = expression.pop(0)
                # operand_right = expression.pop(0)
                # print(f"{operand_left} {operator} {operand_right}")
                if not valid_expression(*expression[:3]):
                    print("Invalid expression")
                    break
                operand_left = int(expression.pop(0))
                operator = simplify_operator(expression.pop(0))
                operand_right = int(expression.pop(0))
                if operator == "-":
                    operand_right = -operand_right
                expression.insert(0, sum((operand_left, operand_right)))
            print(expression.pop())
    print("Bye!")


def main():
    stage5()
    # print(int("a"))


if __name__ == "__main__":
    main()
