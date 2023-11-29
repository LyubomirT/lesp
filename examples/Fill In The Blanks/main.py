from lesp.autocorrect import Proofreader
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

# Use the Proofreader class for spelling checking
proofreader = Proofreader()

# Check spelling
if proofreader.is_correct(user_input):
    print("Correct!")
else:
    # Get similar words
    similar_words = proofreader.get_similar(user_input, similarity_rate=0.7, chunks=4, upto=3)

    if similar_words:
        print(f"Incorrect. The correct word is '{random_word}'. Did you mean one of these: {', '.join(similar_words)}?")
    else:
        print(f"Incorrect. The correct word is '{random_word}'.")
