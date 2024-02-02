import os
import random
from datetime import datetime

lengthDigit = 4
maxAttempts = 8
repeatedDigits = 'n'
choiceDigit = 6

class ChoiceWithRange:
    def __init__(self, minValue, maxValue):
        self.min = minValue
        self.max = maxValue

    def get_value(self):
        pass_all = False
        while not pass_all:
            userInput = input('Please enter an integer between %s and %s: ' % (self.min, self.max))
            if userInput.isdigit():
                pass_all = True
                userInput = int(userInput)
                if userInput < self.min or userInput > self.max:
                    pass_all = False
                    print("Input not within specified range.")
            else:
                print("Input is not a digit.")
        return userInput

class Option:
    def __init__(self, *options):
        self.options = options
    
    def get_value(self):
        validResponses = list(self.options)
        invalidInput = True
        while invalidInput:
            userInput = input(f'Please enter one of the following options: {", ".join(validResponses)}: ')
            userInput = userInput.lower()
            invalidInput =  userInput not in validResponses
            if invalidInput:
                print("Invalid input")
        return userInput


def save_record(name, num_digit, range_digit, repeat_digit, game_start_datetime, attempts, win_loss):
    # Get the current date and time
    current_datetime = datetime.now()
    file_path = 'MM_record.txt'
    
    # Open the text file in append mode
    with open(file_path, 'a') as file:
        # Write the user information to the file
        file.write(f"Name: {name}\n")
        file.write(f"Number of Digits to guess: {num_digit}\n")
        file.write(f"Range of Digits to guess: {range_digit}\n")
        if repeat_digit == 'y':
            file.write("Any repeated digit to guess: Yes\n")
        else:
            file.write("Any repeated digit to guess: No\n")
        file.write(f"Attempts: {attempts}\n")
        if win_loss:
            file.write("Result: Win\n")
        else:
            file.write("Result: Loss\n")
        game_start_datetime_str = game_start_datetime.strftime("%Y-%m-%d %H:%M:%S") 

        file.write(f"Game start time: {game_start_datetime_str}\n")
        minutes_elapsed = (current_datetime - game_start_datetime).total_seconds() / 60
        rounded_minutes_elapsed = "{:.2f}".format(minutes_elapsed)
        file.write(f"Time spent for this round (minutes): {rounded_minutes_elapsed}\n")
        file.write("----------\n")
    
    # Display a confirmation message
    print("User record has been saved to 'MM_record.txt'.")

def history():
    # Open the file for reading
    try:
        with open('MM_record.txt', 'r') as file:
            filecontent = file.read()  # Read the data from the file
            # Count the number of lines
            numLines = filecontent.count('\n')
            if numLines >= 9:
                print("The record of the last player: ")
                lines = filecontent.splitlines()
                # Calculate the starting line index
                startLineIndex = numLines - 9 + 1
                # Display the lines
                for i in range(startLineIndex, numLines):
                    print(lines[i])
    except FileNotFoundError:
        return

def generate_target_digits(choiceDigit, lengthDigit, repeatedDigits):
    target_digits = random.sample(range(1, choiceDigit + 1), lengthDigit)  # unique digits; random.sample(Source, length)
    if repeatedDigits == 'y':
        print('repeat is Yes')
        digit_repeats = [lengthDigit] * lengthDigit
        repeated_elements = [digit for digit, repeat in zip(target_digits, digit_repeats) for _ in range(repeat)]
        shuffled_sequence = random.sample(repeated_elements, len(repeated_elements))
        target_digits = shuffled_sequence[:lengthDigit]
    return target_digits

def check_guess_digits(guess_digits, target_digits):
    num_correct_positions = sum(1 for guess, target in zip(guess_digits, target_digits) if guess == target)
    
    num_correct_digits = sum(1 for guess in guess_digits for target in target_digits if guess == target)
    return num_correct_positions, num_correct_digits
    
def play_game():
    play_again = True
    while play_again:
        # Generate random target digits
        target_digits = generate_target_digits(choiceDigit, lengthDigit, repeatedDigits)
        # print(target_digits) # item starts from 0, eg. target_digits[0]
        # Initialize variables
        attempts = 0
        bingo = False
        messages = '(1:correct position ; 0:correct digit) \n'
        game_start_datetime = datetime.now()

        print('Game starts. Enjoy it!')
        print('----------------------------------------')

        while attempts < maxAttempts and not bingo:
            attempts += 1
            guess_digits = [0] * lengthDigit  # Preallocate an array of size 1xlengthDigit with zeros
            entry_ok = False

            while not entry_ok:
                input_msg = f'Enter {lengthDigit} digits chosen from 1 to {choiceDigit} without spaces: '
                user_input = input(input_msg)

                # First Check: if the number of entered characters matches the array size
                if len(user_input) != len(guess_digits):
                    print('Error: Number of entered digits is not correct.')
                    continue

                # Second Check: if entered characters are digits
                if not user_input.isdigit():
                    print('Error: Entered characters are not digits.')
                    continue

                # Third Check: entered digits are within choiceDigit
                if any(int(digit) == 0 or int(digit) > choiceDigit for digit in user_input):
                    print('Error: Entered characters are not within range.')
                    continue

                entry_ok = True

            # Save to guess_digits when all inputs are correct
            guess_digits = [int(digit) for digit in user_input]

            # Check guess_digits against target_digits
            num_correct_positions, num_correct_digits = check_guess_digits(guess_digits, target_digits)

            # Create the content (final_string) to display for a particular attempt
            final_string = f'Attempt {attempts} :  {" ".join(map(str, guess_digits))}  |  {"1 " * num_correct_positions}{"0 " * (num_correct_digits-num_correct_positions)}'
            messages = messages + final_string +'\n'

            # Clear the screen and print all memorized messages again
            os.system('cls')   # clear the command window
            print(messages)

            # Check if the game is won
            if num_correct_positions == lengthDigit:
                bingo = True

        # Game result
        if bingo:
            print('Congratulations! You find the target digits.')
        else:
            print('Sorry, you cannot find the target digits within allowed attempts.')
            print(f'The target digits are: {target_digits}')

        # Ask if the user wants to save the game result
        print('Do you want save game result? (y/n): ')
        user_choice1 = Option('y','n')
        if user_choice1.get_value() == 'y':
            save_record(name, lengthDigit, choiceDigit, repeatedDigits, game_start_datetime, attempts, bingo)
            
        # Ask if the user wants to play again
        print('Do you want to play again? (y/n): ')
        user_choice2 = Option('y','n')

        # Check the user's choice
        if user_choice2.get_value() == 'n':
            play_again = False
            print('Thank you for playing!')

# Testing functions
os.system('cls')   # clear the command window
#Set up game default parameters

name = input('Please enter your name: ')   # Ask the user to enter their name
# Display a greeting with the entered name
print(f"Hello, {name}!")
print('Welcome to Text-Based Mastermind!')
history()
print('You are playing Mastermind with 4 unique digits ranging from 1 to 6 and having 8 attempts.')
print('Do you want to change the default configuration of the game? (y/n)')

user_choice3 = Option('y','n')
if user_choice3.get_value() == 'y':
    # Ask user to choose the game parameters
    print('Please choose the number of digits to guess (4 - 6) : ')
    config1 = ChoiceWithRange(4, 6)
    lengthDigit = config1.get_value()
    print(f'Length of digits: {lengthDigit}')

    print('Please choose the range of digits to guess, starting from 1 (6 - 9) : ')
    config2 = ChoiceWithRange(6, 9)
    choiceDigit = config2.get_value()
    print(f'Range of digits: 1 - {choiceDigit}')

    print('Please choose the maximum attempts you want to try (8 - 20) : ')
    config3 = ChoiceWithRange(8, 20)
    maxAttempts = config3.get_value()
    print(f'Maximum Attempts: {maxAttempts}')
    
    user_choice4 = Option('y','n')
    print('Digits to guess contains repeated digits? (y/n) ')
    repeatedDigits = user_choice4.get_value()
    print(f'Digits to guess may contain repeated digits: {repeatedDigits}')

play_game()
