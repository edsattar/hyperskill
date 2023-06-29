import argparse
import logging
import sys
import random
import json
import io


class FlashcardApp:
    def __init__(self, import_file_path=None, export_file_path=None):
        self.import_file_path = import_file_path
        self.export_file_path = export_file_path
        self.actions = {
            "add": self.add_card,
            "remove": self.remove_card,
            "import": self.import_cards,
            "export": self.export_cards,
            "ask": self.ask,
            "exit": None,
            "log": self.save_log,
            "hardest card": self.hardest_card,
            "reset stats": self.reset_stats,
        }
        self.log = io.StringIO()
        self.cards = {}
        self.errors = {}

        formatter = logging.Formatter("%(message)s")
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        ih = logging.StreamHandler(self.log)
        ih.setLevel(logging.DEBUG)
        ih.setFormatter(formatter)
        # self.logger.addHandler(ch)
        # self.logger.addHandler(ih)

        trackers = ch, ih
        logging.basicConfig(handlers=trackers)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        if self.import_file_path is not None:
            self.import_cards(self.import_file_path)

    def action_menu(self) -> None:
        action_input = self.log_input(
            f"Input the action ({', '.join(self.actions.keys())}):"
        )
        while action_input != "exit":
            try:
                self.actions[action_input]()
            except KeyError:
                self.logger.error(f'"{action_input}" is not a valid action')
            action_input = self.log_input(
                f"Input the action ({', '.join(self.actions.keys())}):"
            )
        else:
            if self.export_file_path is not None:
                self.export_cards(self.export_file_path)
            self.logger.info("Bye bye!")
            self.log.close()

    def add_card(self):
        term = self.log_input("The card:")
        while term in self.cards.keys():
            term = self.log_input(f'The term "{term}" already exists. Try again:')

        defn = self.log_input("The definition of the card:")
        while defn in self.cards.values():
            defn = self.log_input(f'The definition "{defn}" already exists. Try again:')

        self.cards[term] = defn

        # self.logger.info(f'The pair ("{term}":"{defn}") has been added.')
        print(f'The pair ("{term}":"{defn}") has been added.')
        print(f'The pair ("{term}":"{defn}") has been added.', file=self.log)

    def remove_card(self):
        term = self.log_input("Which card:")
        if term not in self.cards.keys():
            self.logger.info(f"Can't remove {term}: there is no such card.")
            print(f"Can't remove {term}: there is no such card.", file=self.log)
        else:
            self.cards.pop(term)
            self.logger.info("The card has been removed.")
            print("The card has been removed.", file=self.log)

    def import_cards(self, file_path=None):
        if file_path is None:
            file_path = self.log_input("File name:")

        try:
            with open(file_path, "r") as f:
                cards = json.loads(f.read())
                self.logger.info(f"{len(cards)} cards have been loaded")
                self.cards.update(cards)
        except FileNotFoundError:
            self.logger.info("File not found.")

    def export_cards(self, file_path=None):
        if file_path is None:
            file_path = self.log_input("File name:")
        n = len(self.cards)
        with open(file_path, "w+") as f:
            json.dump(self.cards, f)
        self.logger.info(f"{n} cards have been saved")
        print(f"{n} cards have been saved", file=self.log)

    def ask(self):
        if len(self.cards) == 0:
            self.logger.warning("No cards added yet")
            return

        n = int(self.log_input("How many times to ask?"))
        for _ in range(n):
            term = random.choice(sorted(self.cards))
            ans = self.log_input(f'Print the definition of "{term}"')
            if ans == self.cards[term]:
                self.logger.info("Correct!")
            else:
                if term in self.errors:
                    self.errors[term] += 1
                else:
                    self.errors[term] = 1
                response = f'Wrong. The right answer is "{self.cards[term]}".'
                for key, val in self.cards.items():
                    if ans == val:
                        response = f'Wrong. The right answer is "{self.cards[term]}", but your definition is correct for "{key}"'
                self.logger.info(response)
                print(response, file=self.log)

    def log_input(self, message):
        print(message)
        print(message, file=self.log)
        # self.logger.info(message)
        user_input = input()
        # self.logger.debug(user_input)
        self.log.write(user_input + "\n")

        return user_input

    def save_log(self) -> None:
        file_path = self.log_input("File name:")
        with open(file_path, "w+") as f:
            f.write(self.log.getvalue())
        self.logger.info("The log has been saved.")

    def reset_stats(self) -> None:
        self.errors.clear()
        self.logger.info("Card statistics have been reset.")

    def hardest_card(self) -> None:
        # print(self.errors)
        max_error = 1
        hardest_cards: list[str] = []
        delimiter = '", "'
        for key, val in self.errors.items():
            if val > max_error:
                hardest_cards = [key]
                max_error = val
            elif val == max_error:
                hardest_cards.append(key)

        if len(hardest_cards) > 1:
            self.logger.info(
                f'The hardest cards are "{delimiter.join(hardest_cards)}". You have {max_error} errors answering them.'
            )
        elif len(hardest_cards) == 1:
            self.logger.info(
                f'The hardest card is "{hardest_cards[0]}". You have {max_error} errors answering it.'
            )
        else:
            self.logger.info("There are no cards with errors.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Flashcard app")
    parser.add_argument("-i", "--import_from", type=str, help="import file path")
    parser.add_argument("-e", "--export_to", type=str, help="export file path")
    parser.add_argument("-l", "--log", type=str, help="log file path")
    args = parser.parse_args()
    app = FlashcardApp(args.import_from, args.export_to)
    app.action_menu()


if __name__ == "__main__":
    main()
