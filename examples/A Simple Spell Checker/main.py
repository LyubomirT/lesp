from lesp.autocorrect import Proofreader

# Create an instance of the Proofreader class
proofreader = Proofreader()

# Read a text file and check for spelling errors
with open("text.txt", "r") as f:
    text = f.read()

# Split the text into words
words = text.split()

# Loop through the words and check if they are correct
for word in words:
    # Remove punctuation and make lowercase
    word = word.strip(".,").lower()
    # Check if the word is correct
    if not proofreader.is_correct(word):
        # Get a suggestion for the word
        suggestion = proofreader.get_similar(word, similarity_rate=0.5, upto=1)
        # Print the word and the suggestion
        print(f"{word} -> {', '.join(suggestion)}" if suggestion else f"{word} -> No suggestions")
