import json
import random

class Flashcard:
    # class constructor
    def __init__(self, question, choices, correct_answer, incorrect_attempts=0, correct_attempts=0):
        self.question = question
        self.choices = choices
        self.correct_answer = correct_answer
        self.incorrect_attempts = incorrect_attempts
        self.correct_attempts = correct_attempts

    # display question chen playing
    def ask_question(self):
        print(self.question)
        for idx, choice in enumerate(self.choices, 1):
            print(f"{idx}. {choice}")

        while True:
            try:
                # retrieve user choice and check if correct answer or not
                user_answer = int(input("Enter your answer (number): "))
                if 1 <= user_answer <= len(self.choices):
                    if self.choices[user_answer - 1] == self.correct_answer:
                        print("Correct!")
                        self.correct_attempts += 1
                    else:
                        print("Incorrect. The correct answer was:", self.correct_answer)
                        self.incorrect_attempts += 1
                    break
                # handle invalid input
                else:
                    print("Please enter a number between 1 and", len(self.choices))
            except ValueError:
                print("Invalid input. Please enter a number.")


    # convert flashcard into dictionary format for json storing
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "correct_answer": self.correct_answer,
            "incorrect_attempts": self.incorrect_attempts,
            "correct_attempts": self.correct_attempts
        }

# list all flashcards in the flashcard bank
def list_flashcards(flashcard_bank):
    for index, flashcard in enumerate(flashcard_bank, start=1):
        print(f"{index}. {flashcard.question}")

# edit flashcard
def edit_flashcard(flashcard):
    print("Current question: ", flashcard.question)
    # get new question input from the user
    new_question = input("Enter the new question (press enter if you want to keep the current)")
    if new_question:
        flashcard.question = new_question

    print("Current choices : ", ','.join(flashcard.choices))
    # get new choices input from the user
    new_choices = input("Enter the new answer choices, separated by a comma (press enter to keep the current choices) : ")
    if new_choices:
        flashcard.choices = [choice.strip() for choice in new_choices.split(',')]

    print("Current correct answer: ", flashcard.correct_answer)
    # get new correct answer input from the user
    new_answer = input("Enter the new correct answer (press enter to keep the current answer): ")
    if new_answer:
        flashcard.correct_answer = new_answer

# delete flashcard
def delete_flashcard(flashcard_bank, index):
    del flashcard_bank[index]

# let the user pick the flashcard
def choose_flashcard(flashcard_bank):
    list_flashcards(flashcard_bank)
    try:
        flashcard_index = int(input("Enter the number of the flashcard you'd like to play :"))
        if 0 <= flashcard_index < len(flashcard_bank):
            flashcard_bank[flashcard_index].ask_question()
            save_flashcards_to_file(flashcard_bank)
        else:
            print("Invalid index. Please enter a valid number.")
    except ValueError:
        print("Please enter a valid number")

# select flashcard based on incorrect to correct attempts ratio
def select_flashcard(flashcard_bank):
    # don't return anything if the flashcard bank is empty
    if not flashcard_bank:
        return None
    # calculate each flashcards incorrect attempts to correct attempt ratio and sort the flashcard bank accordingly (flashcards with the most incorrect attempts have the highest priority in the display of questions when the user is playing)
    flashcard_bank.sort(key=lambda x: (x.incorrect_attempts + 1) / (x.correct_attempts + 1), reverse=True)
    # return the chosen flashcard
    return random.choice(flashcard_bank[:max(3, len(flashcard_bank)// 2)])

# add a new flashcard in the bank
def add_flashcard():
    question = input('Enter the flashcard question : ')
    choices_input = input('Enter all choices separated by a comma: ')
    choices = [choice.strip() for choice in choices_input.split(',')]

    # separate each answers 
    while True:
        correct_answer = input('Enter the correct answer : ').strip()
        if correct_answer in choices:
            break
        else:
            print('The correct answer must be one of the choices. Please try again.')
    # create the new flashcard
    new_flashcard = Flashcard(question, choices, correct_answer)
    return new_flashcard

# load all flashcards from json file (if there are flashcards stored)
def load_flashcards_from_file(filename='flashcards.json'):
    try:
        with open(filename, 'r') as file:
            flashcards_data = json.load(file)
            return [Flashcard(**data) for data in flashcards_data]
    except FileNotFoundError:
        return [] 
    
# helper function to save the newly created/edited flashcards into the bank
def save_flashcards_to_file(flashcards, filename='flashcards.json'):
    with open(filename, 'w') as file:
        json.dump([flashcard.to_dict() for flashcard in flashcards], file, indent=4)


def main():
    # load flashcards
    flashcard_bank = load_flashcards_from_file()

    # display menu
    while True:
        print("\nWizzpy Flashcard App")
        print("1. Add a new flashcard")
        print("2. Review a flashcard")
        print("3. View all flashcards")
        print("4. Edit a  flashcard")
        print("5. Delete a flashcard")
        print("6. Quit")

        # retrieve user choice
        choice = input("Enter your choice: ")

        # allow user to add a new flashcard
        if choice == '1':
            new_flashcard = add_flashcard()
            flashcard_bank.append(new_flashcard)
            save_flashcards_to_file(flashcard_bank)

        # review flashcards
        elif choice == '2':
            # display submenu 
            if flashcard_bank:
                print("\n Review flashcards")
                print("\n 1. Review a random flashcard")
                print("\n 2. Pick a flashcard to review")
                review_choice = input("Enter yur choice (number) : ")

                if review_choice == '1':
                    # select a random flashcard
                    random_flashcard = select_flashcard(flashcard_bank)
                    if random_flashcard:
                        random_flashcard.ask_question()
                        save_flashcards_to_file(flashcard_bank)
                    else:
                        print("You have no flashcard available. Please add some first")

                elif review_choice == '2':
                    # let the user pock a flashcard
                    choose_flashcard(flashcard_bank)

                else:
                    print("Invalid choice. Please pick 1 or 2")

            else:
                print("You currently have no flashcards available ! Please add some first.")

        # visualize all flashcards in the bank
        elif choice == '3':
            list_flashcards(flashcard_bank)

        # allow user to edit any flashcard
        elif choice == '4':
            list_flashcards(flashcard_bank)
            try:
                flashcard_index = int(input("Enter the number of the flashcard you would like to edit: ")) - 1
                if 0 <= flashcard_index < len(flashcard_bank):
                    edit_flashcard(flashcard_bank[flashcard_index])
                    save_flashcards_to_file(flashcard_bank)
                else:
                    print("Invalid index. Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")

        # allow user to delete any flashcard
        elif choice == '5':
            list_flashcards(flashcard_bank)
            try:
                flashcard_index = int(input("Enter the number of the flashcard you would like to delete: ")) - 1
                if 0 <= flashcard_index < len(flashcard_bank):
                    delete_flashcard(flashcard_bank, flashcard_index)
                    save_flashcards_to_file(flashcard_bank)
                else:
                    print("Invalid index. Please enter a valid number.")
            except ValueError:
                print("Please enter a valid number.")

        
        elif choice == '6':
            print("Thank you for using Wizzpy. Goodbye!")
            break

        # handle invalid choice
        else:
            print("Invalid choice. Please enter a valid choice")

if __name__ == "__main__":
    main()
