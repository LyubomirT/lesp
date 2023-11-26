# Import the get_similarity_score function from the lesp module
from lesp import get_similarity_score

# Import tkinter for creating a graphical user interface
import tkinter as tk

# Create a window
window = tk.Tk()
window.title("Word Similarity App")

# Create a label for the first word
label1 = tk.Label(window, text="Enter the first word:")
label1.pack()

# Create an entry for the first word
entry1 = tk.Entry(window)
entry1.pack()

# Create a label for the second word
label2 = tk.Label(window, text="Enter the second word:")
label2.pack()

# Create an entry for the second word
entry2 = tk.Entry(window)
entry2.pack()

# Create a button for calculating the similarity score
button = tk.Button(window, text="Calculate")

# Define a function for calculating the similarity score
def calculate():
    # Get the words from the entries
    word1 = entry1.get()
    word2 = entry2.get()
    # Calculate the similarity score
    score = get_similarity_score(word1, word2)
    # Display the similarity score
    result.config(text=f"The similarity score is {score:.2f}")

# Bind the function to the button
button.config(command=calculate)
button.pack()

# Create a label for displaying the similarity score
result = tk.Label(window, text="")
result.pack()

# Start the main loop of the window
window.mainloop()
