import random
import os
a = random.randint(1, 10)
b = int(input("Enter a number: "))
if a == b:
    print("You win!")
else:
    os.remove("tp.py")
    print("You lose!")

# This is a simple game where you have to guess a number between 1 and 10.
# If you guess the number correctly, you win the game.  If you guess the
# number incorrectly, the program will delete itself.
# This is an example of a self-destructing program.