import random
import json


class FlashcardApp:
    def __init__(self):
        self.actions = {
            "add": self.add_card,
            "remove": self.remove_card,
            "import": self.import_cards,
            "export": self.export_cards,
            "ask": self.ask,
            "exit": None,
        }
        self.cards = {}

    def action_menu(self) -> None:
        action_input = input(f"Input the action ({', '.join(self.actions.keys())}):\n")
        if action_input in self.actions:
            while action_input != "exit":
                self.actions[action_input]()
                action_input = input(
                    f"Input the action ({', '.join(self.actions.keys())}):\n"
                )
            else:
                print("Bye bye!")

    def add_card(self):
        term = input("The card:\n")
        while term in self.cards.keys():
            term = input(f'The term "{term}" already exists. Try again:\n')

        defn = input("The definition of the card:\n")
        while defn in self.cards.values():
            defn = input(f'The definition "{defn}" already exists. Try again:\n')

        self.cards[term] = defn

        print(f'The pair ("{term}":"{defn}") has been added.')

    def remove_card(self):
        term = input("Which card:\n")
        try:
            self.cards.pop(term)
        except KeyError:
            print(f"Can't remove {term}: there is no such card.")
        else:
            print("The card has been removed.")

    def import_cards(self):
        file_path = input("File name:\n")
        try:
            with open(file_path, "r") as f:
                cards = json.loads(f.read())
                print(f"{len(cards)} cards have been loaded")
                self.cards.update(cards)
        except FileNotFoundError:
            print("File not found.")

    def export_cards(self):
        file_path = input("File name:\n")
        with open(file_path, "w+") as f:
            json.dump(self.cards, f)
        print(f"{len(self.cards)} cards have been saved")

    def ask(self):
        n = int(input("How many times to ask?\n"))
        for _ in range(n):
            term = random.choice(sorted(self.cards))
            ans = input(f'Print the definition of "{term}"\n')
            if ans == self.cards[term]:
                print("Correct!")
            else:
                response = f'Wrong. The right answer is "{self.cards[term]}".'
                for key, val in self.cards.items():
                    if ans == val:
                        response = f'Wrong. The right answer is "{self.cards[term]}", but your definition is correct for "{key}"'
                print(response)


def main() -> None:
    app = FlashcardApp()
    app.action_menu()


if __name__ == "__main__":
    main()
