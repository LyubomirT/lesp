from main import is_correct, get_similar

def demo():
    while True:
        word = input("Enter a word: ")
        if is_correct(word):
            print("Correct!")
        else:
            print("Incorrect!")
            similar = get_similar(word, 0.7, chunks=500)
            if similar == None:
                print("No similar words found.")
            else:
                similar = similar[0]
                print("Did you mean \"" + similar + "\"?")
        print()

if __name__ == "__main__":
    demo()