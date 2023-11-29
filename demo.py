from lesp.autocorrect import Proofreader

def load_config():
    try:
        with open("demo_config", "r") as f:
            config = f.read()
        return config
    except FileNotFoundError:
        raise FileNotFoundError("demo_config not found!")

try:
    config = load_config()
except FileNotFoundError as error:
    print(error)
    exit()

# showallsimilarities="True"
showallsimilarities = config.split("showallsimilarities=\"")[1].split("\"")[0]

def demo():
    wordlist_path = "small_wordlist.txt"  # Update with the actual path to your wordlist. Or use the pre-installed small wordlist.
    proofreader = Proofreader(wordlist_path)

    while True:
        word = input("Enter a word: ")
        if proofreader.is_correct(word):
            print("Correct!")
        else:
            print("Incorrect!")
            similar = proofreader.get_similar(word, 0.5, chunks=20, upto=5)
            if similar is None:
                print("No similar words found.")
            elif showallsimilarities == "True":
                print("Did you mean any of the following?")
                for w in similar:
                    print("\"" + w + "\"")
            else:
                similar = similar[0]
                print("Did you mean \"" + similar + "\"?")
        print()

if __name__ == "__main__":
    demo()
