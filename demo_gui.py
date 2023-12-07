import tkinter as tk
from tkinter import scrolledtext, messagebox, StringVar, OptionMenu

from lesp.autocorrect import Proofreader

class CorrectionPopup:
    def __init__(self, master, word, options, replace_callback):
        self.master = master
        self.word = word
        self.options = options
        self.replace_callback = replace_callback

        self.popup = tk.Toplevel(master)
        self.popup.title(f"Replace '{word}'")

        self.correction_var = StringVar()
        self.correction_var.set(options[0])

        correction_menu = OptionMenu(self.popup, self.correction_var, *options)
        correction_menu.pack(padx=5, pady=5)

        replace_button = tk.Button(self.popup, text="Replace", command=self.replace_word)
        replace_button.pack(padx=5, pady=5)

        dismiss_button = tk.Button(self.popup, text="Dismiss", command=self.dismiss_popup)
        dismiss_button.pack(padx=5, pady=5)

    def replace_word(self):
        new_word = self.correction_var.get()
        self.replace_callback(self.word, new_word)
        self.dismiss_popup()

    def dismiss_popup(self):
        self.popup.destroy()

class SpellCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LESP Spell Checker")
        self.root.geometry("600x400")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, width=50, font=("Helvetica", 12))
        self.text_area.pack(pady=10)

        self.check_button = tk.Button(self.root, text="Check Text", command=self.check_text)
        self.check_button.pack(pady=10)

        self.proofreader = Proofreader(wordlist_path="small_wordlist.txt")

    def check_text(self):
        self.clear_highlight()
        text_content = self.text_area.get("1.0", tk.END)
        incorrect_words = self.get_incorrect_words(text_content)

        if not incorrect_words:
            messagebox.showinfo("Spell Checker", "No spelling errors found!")
        else:
            self.highlight_incorrect_words(incorrect_words)

    def get_incorrect_words(self, text):
        words = text.split()
        incorrect_words = []

        for word in words:
            cleaned_word = self.proofreader.remove_special(word.lower())
            if not self.proofreader.is_correct(cleaned_word):
                incorrect_words.append(cleaned_word)

        return set(incorrect_words)

    def highlight_incorrect_words(self, incorrect_words):
        for word in incorrect_words:
            start_index = "1.0"
            while True:
                start_index = self.text_area.search(word, start_index, tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                self.text_area.tag_add("highlight", start_index, end_index)
                start_index = end_index

                similar_words = self.proofreader.get_similar(word, similarity_rate=0.3)
                correction_options = CorrectionPopup(self.root, word, similar_words, self.replace_word)

                # Make the popup bigger
                correction_options.popup.geometry("300x150")
                correction_options.popup.focus_force()
                self.root.wait_window(correction_options.popup)

    def replace_word(self, old_word, new_word):
        start_index = "1.0"
        while True:
            start_index = self.text_area.search(old_word, start_index, tk.END)
            if not start_index:
                break
            end_index = f"{start_index}+{len(old_word)}c"
            self.text_area.replace(start_index, end_index, new_word)
            start_index = end_index

    def clear_highlight(self):
        self.text_area.tag_remove("highlight", "1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpellCheckerApp(root)
    root.mainloop()
