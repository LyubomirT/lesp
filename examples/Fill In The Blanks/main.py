#from lesp import is_correct
from lesp.autocorrect import is_correct, get_similar
import random

# Load words from wordlist file
with open("wordlist.txt", "r") as f:
    words = [word.strip() for word in f.readlines()]
random_word = random.choice(words)

# Create a word with blanks
word_with_blanks = ""
for i, letter in enumerate(random_word):
    if i % 2 == 0:
        word_with_blanks += letter
    else:
        word_with_blanks += "_"

print("Fill in the blanks:", word_with_blanks)

# User input
user_input = input("Your guess: ")

# Check spelling
if user_input.lower() == random_word:
    print("Correct!")
else:
    print(f"Incorrect. The correct word is '{random_word}'.")