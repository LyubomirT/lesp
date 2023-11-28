#from lesp import is_correct
from lesp.autocorrect import is_correct, get_similar
import random

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
if guess.lower() == word:
    print("Correct!")
else:
    print(f"Incorrect. The correct word was '{word}'.")
