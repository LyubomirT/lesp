from lesp import get_similar
import random

# A list of words to choose from
words = ["apple", "banana", "orange", "grape", "melon", "cherry", "lemon", "lime", "pear", "peach"]

# Pick a random word
word = random.choice(words)

# Get three similar words with a similarity rate of 0.4
similar_words = get_similar(word, similarity_rate=0.4, upto=3)

# Add the original word to the list
similar_words.append(word)

# Shuffle the list
random.shuffle(similar_words)

# Print the list
print("Which of these words is not like the others?")
for i, w in enumerate(similar_words):
    print(f"{i + 1}. {w}")

# Get the user's answer
answer = int(input("Enter your answer: "))

# Check if the answer is correct
if similar_words[answer - 1] == word:
    print("Correct!")
else:
    print(f"Wrong! The correct answer is {word}.")
