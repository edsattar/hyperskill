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
    usr_input1 = "-2 + 4 - 5 + 6"
    usr_input2 = "9 +++ 10 -- 8"
    data = usr_input2.split()
    print(data)
    print(list(map(isnumeric, data))) 


def main():
    stage4()


if __name__ == "__main__":
    main()
