import os
import csv
import argparse as ap
from os import path
import tkinter as tk

# app = ImageSorter('./crops/','./champions', './labels.csv', master=root)
parser = ap.ArgumentParser(description = 'Label image data')
parser.add_argument('--in', type=str, dest = 'input_path', default = './crops/', help = "path to grab images")
parser.add_argument('--out', type=str, dest = 'output_path', default = './labels.csv', help = "path to output labels")
parser.add_argument('--opt', type=str, dest = 'options_path', default = './champions', help = "file list possible labels, separated by newline")

# input_path = directory from which to ingest examples
# options_path = file of categories to choose from, each on newline
# output_path = csv mapping from image names to categories
class ImageSorter(tk.Frame):
    def __init__(self, input_path, options_path, output_path, master=None):
        super().__init__(master)
        self.pack()
        # self.create_widgets()
        self.input_path = input_path
        self.output_path = output_path

        # set up button frame
        self.frame = tk.Frame(self.master)
        self.frame.pack(side="right")

        # set up image
        images = os.listdir(input_path)
        self.images = filter(lambda image: image.endswith('.png'), images)
        self.img_label = tk.Label(self)
        self.iterate_image()
        self.img_label.pack(side="left")

        # set up button
        self.next_button = tk.Button(self.frame)
        self.next_button["text"] = "next"
        self.next_button["command"] = self.iterate_image
        self.next_button.pack(side="top")

        # set up category entry ui
        f = open(options_path)
        self.categories = [line.rstrip('\n') for line in f]
        self.labels = {}
        self.var = tk.StringVar()
        # self.var.trace("w", self.on_entry_changed)
        self.entry = tk.Entry(self.frame, textvariable=self.var)
        self.entry.bind('<Return>', self.on_submit)
        self.entry.bind('<Tab>', self.complete)
        self.entry.pack()
        self.dialog_text = tk.StringVar()
        self.dialog_text.set("enter text")
        self.dialog = tk.Label(self.frame, textvariable=self.dialog_text, fg="black")
        self.dialog.pack()

        # setup quit
        self.quit = tk.Button(self.frame, text="QUIT", fg="red",
                              command=self.exit_picker)
        self.quit.pack(side="bottom")

    # record categories
    def exit_picker(self):
        with open(self.output_path, 'a', newline='') as csvfile:
            catwriter = csv.writer(csvfile, delimiter=',')
            for img, cat in self.labels.items():
                catwriter.writerow([img,cat])
        self.master.destroy()

    def complete(self, event=None):
        matches = list(filter(lambda cat: cat.startswith(self.var.get()), self.categories))
        num_matches = len(matches)
        if num_matches > 1:
            self.dialog.configure(fg="red")
            self.dialog_text.set('more than one match')
        elif num_matches == 0:
            self.dialog.configure(fg="red")
            self.dialog_text.set('no matches')
        else:
            self.var.set(matches[0])
        return "break"

    def on_submit(self, event):
        if self.var.get() in self.categories:
            self.labels[self.image_name] = self.var.get()
            self.var.set('')
            self.iterate_image()
        else:
            self.dialog.configure(fg="red")
            self.dialog_text.set('valid inputs: ' + ' '.join(self.categories))
            # self.dialog_text.set("invalid input, see categories file")


    def iterate_image(self):
        try:
            img = next(self.images)
            self.img_label.image = tk.PhotoImage(file=path.join(self.input_path, img))
            self.img_label.config(image=self.img_label.image)
            self.image_name = img
        except StopIteration:
            self.exit_picker()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
root.geometry("500x500")
# app = ImageSorter('./crops/','./champions', './labels.csv', master=root)
args = parser.parse_args()
app = ImageSorter(args.input_path, args.options_path, args.output_path, master=root)
app.mainloop()