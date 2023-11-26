from ac.autocorrect import is_correct, get_similar

def load_config():
    with open("demo_config", "r") as f:
        config = f.read()
    return config

config = load_config()
# showallsimilarities="True"
showallsimilarities = config.split("showallsimilarities=\"")[1].split("\"")[0]

def demo():
    while True:
        word = input("Enter a word: ")
        if is_correct(word):
            print("Correct!")
        else:
            print("Incorrect!")
            similar = get_similar(word, 0.5, chunks=20, upto=5)
            if similar == None:
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