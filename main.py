import json
import random

class Flashcard:
    def __init__(self, question, choices, correct_answer):
        self.question = question
        self.choices = choices
        self.correct_answer = correct_answer
        self.incorrect_attempts = 0
        self.correct_attempts = 0

    def ask_question(self):
        print(self.question)
        for idx, choice in enumerate(self.choices, 1):
            print(f"{idx}. {choice}")

        while True:
            try:
                user_answer = int(input("Your answer (number): "))
                if 1 <= user_answer <= len(self.choices):
                    if self.choices[user_answer - 1] == self.correct_answer:
                        print("Correct!")
                        self.correct_attempts += 1
                    else:
                        print("Incorrect. The correct answer was:", self.correct_answer)
                        self.incorrect_attempts += 1
                    break
                else:
                    print("Please enter a number between 1 and", len(self.choices))
            except ValueError:
                print("Invalid input. Please enter a number.")


    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "correct_answer": self.correct_answer,
            "incorrect_attempts": self.incorrect_attempts,
            "correct_attempts": self.correct_attempts
        }


def select_flashcard(flashcard_bank):
    if not flashcard_bank:
        return None
    # Sort flashcard based on incorrect/correct ratio attempts
    # Flashcards with a higher ratio (more incorrect than correct) are prioritized
    flashcard_bank.sort(key=lambda x: (x.incorrect_attempts + 1) / (x.correct_attempts + 1), reverse=True)
    # Select from the top prioritized flashcards
    return random.choice(flashcard_bank[:max(3, len(flashcard_bank)// 2)])


def add_flashcard():
    question = input('Enter the flashcard question : ')
    choices_input = input('Enter all choices separated by a comma: ')
    choices = [choice.strip() for choice in choices_input.split(',')]

    while True:
        correct_answer = input('Enter the correct answer : ').strip()
        if correct_answer in choices:
            break
        else:
            print('The correct answer must be one of the choices. Please try again.')

    new_flashcard = Flashcard(question, choices, correct_answer)
    return new_flashcard

def load_flashcards_from_file(filename='flashcards.json'):
    try:
        with open(filename, 'r') as file:
            flashcards_data = json.load(file)
            return [Flashcard(**data) for data in flashcards_data]
    except FileNotFoundError:
        return [] 

def save_flashcards_to_file(flashcards, filename='flashcards.json'):
    with open(filename, 'w') as file:
        json.dump([flashcard.to_dict() for flashcard in flashcards], file, indent=4)


def main():
    flashcard_bank = load_flashcards_from_file()

    while True:
        print("\nWizzpy Flashcard App")
        print("1. Add a new flashcard")
        print("2. Review a random flashcard")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            new_flashcard = add_flashcard()
            flashcard_bank.append(new_flashcard)
            save_flashcards_to_file(flashcard_bank)
        elif choice == '2':
            if flashcard_bank:
                random_flashcard = select_flashcard(flashcard_bank)
                if random_flashcard:
                    random_flashcard.ask_question()
                    save_flashcards_to_file(flashcard_bank)
                else:
                    print("You have no flashcard available. Please add some first")

        elif choice == '3':
            print("Thank you for using Wizzpy. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
