#from lesp import Proofreader
from lesp.autocorrect import Proofreader
import random

# Initialize the Proofreader instance
proofreader = Proofreader()

# Load words from wordlist file
with open("wordlist.txt", "r") as f:
    words = [word.strip() for word in f.readlines()]

# Pick a random word and scramble it
word = random.choice(words)
scrambled = ''.join(random.sample(word, len(word)))
print("Unscramble this word:", scrambled)

# User guesses
guess = input("Your guess: ")

# Check if guess is correct
if proofreader.is_correct(guess):
    print("Correct!")
else:
    print(f"Incorrect. The correct word was '{word}'.")
