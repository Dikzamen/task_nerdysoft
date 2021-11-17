import json
import tkinter as tk
from tkinter.ttk import Button, Entry, Label
from tkinter.filedialog import askopenfilename
from tkinter import LEFT, RIGHT


def contains(word, letters):
    word_dict = {i: word.count(i) for i in set(word)}
    letters_dict = {i: letters.count(i) for i in set(letters)}
    for key, value in letters_dict.items():
        if word_dict.get(key, 0) < value:
            return False
    return True


class Vocabulary:
    def __init__(self, filename):
        self.filename = filename
        self.dataset = set()
        self.read_data()

    def read_data(self):
        with open(self.filename, 'r', encoding='utf8') as file:
            self.dataset = set(json.load(file))

    def update_data(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f)
        self.read_data()
        print('append word', len(self.dataset))

    def append_word(self, word):
        data = list(self.dataset)
        data.append(word)
        print('append word', len(self.dataset))
        self.update_data(data)

    def append_data(self, filename):
        vocabulary = Vocabulary(filename)
        data1, data2 = list(self.dataset), list(vocabulary.dataset)
        data1.extend(data2)
        self.update_data(data1)

    def count_occurrences(self, letters):
        result = []
        for word in self.dataset:
            if contains(word, letters):
                result.append(word)
        return result


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600+0+0')

        self.dictionary_label = Label(self, text='Current vocabulary contains 0 words')
        self.append_button = Button(self, text='Append vocabulary', command=lambda: self.open_file(False))
        self.replace_button = Button(self, text='Replace vocabulary', command=lambda: self.open_file(True))
        self.dictionary_label.pack()
        self.append_button.pack()
        self.replace_button.pack()

        self.label = Label(self, text='Add word to vocabulary')
        self.label.pack()
        self.word_entry = Entry(self)
        self.word_entry.pack()
        self.new_word_button = Button(self, text='Append word to vocabulary', command=self.add_word)
        self.new_word_button.pack()

        self.search_label = Label(self, text='Search for letters')
        self.search_label.pack()
        self.letters_entry = Entry(self)
        self.letters_entry.pack()

        self.search_button = Button(self, text='Start search', command=self.search)
        self.new_word_label = Label(self, text='Current vocabulary contains 0 words')
        self.answer_number = Entry(self)
        self.search_button.pack()
        self.answer_number.pack()

        self.page = 0
        self.vocabulary = None
        self.page_widgets = []

    def destroy_widgets(self):
        for widget in self.page_widgets:
            widget.destroy()

    def add_word(self):
        word = self.word_entry.get()
        if self.vocabulary:
            self.vocabulary.append_word(word)

    def generate_widgets(self, result, page):
        self.destroy_widgets()
        label = Label(self, text='Results')
        label.pack()
        self.page_widgets.append(label)
        for widget in result[page * 10: page * 10 + 10]:
            entry = Entry(self)
            entry.insert(0, widget)
            entry.pack()
            self.page_widgets.append(entry)
        if page > 0:
            button = Button(self, text='<',
                            command=lambda: self.generate_widgets(result, page - 1)
                            )
            button.pack(side=LEFT)
            self.page_widgets.append(button)
        if result[page * 10 + 10:]:
            button = Button(self, text='>',
                            command=lambda: self.generate_widgets(result, page + 1)
                            )
            button.pack(side=RIGHT)
            self.page_widgets.append(button)

    def open_file(self, replace):
        self.update()
        name = askopenfilename()
        vocabulary = Vocabulary(name)
        if replace or self.vocabulary is None:
            self.vocabulary = vocabulary
            self.dictionary_label.config(text=f'Current vocabulary contains {len(self.vocabulary.dataset)} words')
        else:
            self.vocabulary.append_data(name)
            self.dictionary_label.config(text=f'Current vocabulary contains {len(self.vocabulary.dataset)} words')

    def search(self):
        search_text = self.letters_entry.get()
        result = self.vocabulary.count_occurrences(search_text)
        self.answer_number.delete(0, 'end')
        self.answer_number.insert(0, str(len(result)))
        self.generate_widgets(result, 0)


def main():
    window = Application()
    window.mainloop()


if __name__ == '__main__':
    main()
