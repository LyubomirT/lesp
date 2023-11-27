def bulkexpansion_wordlist(wordlist, words):
    if isinstance(words, str):
        # If a single word is provided, add it to the wordlist
        if words.isalpha():
            wordlist.append(words)
        else:
            raise ValueError(f"Invalid input: '{words}' is not a valid word.")
    elif isinstance(words, (list, tuple)):
        # If a list or tuple is provided, extend the wordlist with its elements
        for word in words:
            if isinstance(word, str) and word.isalpha():
                wordlist.append(word)
            else:
                raise ValueError(f"Invalid input: '{word}' is not a valid word.")
    else:
        # Handle other types if needed
        raise TypeError("Invalid input type. Please provide a string, list, or tuple of alphabetic words.")

    return wordlist

# Example usage:
wordlist = [] 
# Can link worldlist from the config file if needed

# Adding individual words
wordlist = bulkexpansion_wordlist(wordlist, "apple")
# This will raise a ValueError
wordlist = bulkexpansion_wordlist(wordlist, "123")

# Adding a list of words
word_list = ["orange", "grape", "kiwi"]
wordlist = bulkexpansion_wordlist(wordlist, word_list)

# Adding a tuple of words
word_tuple = ("melon", "pear", "pineapple", 456)
# This will raise a ValueError
# wordlist = bulkexpansion_wordlist(wordlist, word_tuple)

# Get the expanded wordlist
print(wordlist)
