import tkinter as tk
from tkinter import filedialog

# Global variable to store the current file's path
current_file_path = None


def open_file(window, edit_text):
    global current_file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            file_contents = file.read()

        # Delete the current text in the text field
        edit_text.delete(1.0, tk.END)
        edit_text.insert(1.0, file_contents)
        # Set the cursor to the start of the text field
        edit_text.mark_set("insert", "1.0")

        current_file_path = file_path
        file_name = file_path.split('/')[-1]
        window.title(f"{file_name} - breditor")


def new_file(window, edit_text):
    global current_file_path
    current_file_path = None
    edit_text.delete(1.0, tk.END)
    window.title('Untitled - breditor')


def write_to_file(window, edit_text, file_path):
    data = edit_text.get("1.0", tk.END)
    with open(file_path, 'w') as f:
        f.write(data)
    file_name = file_path.split('/')[-1]
    window.title(f"{file_name} - breditor")


def save_file(window, edit_text):
    global current_file_path
    if current_file_path is not None:
        write_to_file(window, edit_text, current_file_path)
    else:
        save_file_as(window, edit_text)


def save_file_as(window, edit_text):
    global current_file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
                                             ("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        current_file_path = file_path
        write_to_file(window, edit_text, file_path)
