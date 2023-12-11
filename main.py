import json
import random

class Flashcard:
    def __init__(self, question, choices, correct_answer):
        self.question = question
        self.choices = choices
        self.correct_answer = correct_answer
        self.incorrect_attempts = 0  # Keep track of incorrect attemps so that this flashcard shows up more often 

    def ask_question(self):
        print(self.question)
        for idx, choice in enumerate(self.choices, 1):
            print(f"{idx}. {choice}")
        user_answer = int(input("Your answer (number): "))
        if self.choices[user_answer - 1] == self.correct_answer:
            print("Correct!")
        else:
            print("Incorrect. The correct answer was:", self.correct_answer)
            self.incorrect_attempts += 1  # Increase the incorrect attempt count

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "correct_answer": self.correct_answer,
            "incorrect_attempts": self.incorrect_attempts
        }


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
                # Sort flashcards by incorrect attempts in descending order, so that it can prioritize which flashcard to display 
                flashcard_bank.sort(key = lambda x: x.incorrect_attempts, reverse=True)
                # Prioritize the flashcards with the most incorrect attempts
                random_flashcard = random.choice(flashcard_bank[:max(3, len(flashcard_bank)//2)])
                random_flashcard.ask_question()

                continue_review = input("Do you want to review another flashcard? (yes/no): ").lower()
                if continue_review != 'yes':
                    continue  # Go back to the main menu
            else:
                print("No flashcards available. Please add some first.")
        elif choice == '3':
            print("Thank you for using Wizzpy. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
