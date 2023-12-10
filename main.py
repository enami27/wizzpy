import json

## flashcard structure
    ## question
   ## mcq answers
## store flashcard
## user interface
    ## create a new flashcard with answers
    ## get a random flashcard questions
        ## keep track of negative/positive answers



class Flashcard:
    def __init__(self, question, choices, correct_answer):
        self.question = question
        self.choices = choices
        self.correct_answer = correct_answer

    def ask_question(self):
        print(self.question)
        for idx, choice in enumerate(self.choice,1):
            print(f"{idx}. {choice}")
        user_answer = int(input("Your answer (number): "))
        if self.choices[user_answer - 1] == self.correct_answer:
            print("Correct")
        else:
            print("Incorrect, the correct answer was: ", self.correct_answer)

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
        
        def to_dict(self):
            return {
                "question": self.question,
                "choices": self.choices,
                "correct_answer": self.correct_answer
            }



def save_flashcards_to_file(flashcards, filename='flashcards.json'):
    with open(filename, 'w') as file:
        ## convert each flashcard to a dictionary 
        json.dump([flashcard.to_dict() for flashcard in flashcards], file, indent=4)

def load_flashcards_from_file(filename='flashcards.json'):
    try:
        with open(filename, 'r') as file:
            flashcards_data = json.load(file)
            return [Flashcard(**data) for data in flashcards_data]
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist
