import tkinter as tk
from tkinter import filedialog
import json

# Global variable to store the current file's path
current_file_path = None


def open_file(window, edit_text):
    global current_file_path
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        # open the file in binary mode to check if it contains textual data
        if not is_text_file(file_path):
            return

        with open(file_path, 'r') as file:
            file_contents = file.read()

        # check if the file is a json file with text and tags according to the breditor format
        try:
            json_data = json.loads(file_contents)
            format = json_data.get('format', None)
            if format != 'json/breditor':
                raise KeyError("No valid format found")
            file_contents = json_data["contents"]
            tags = json_data["tags"]

        # if the file has no tags, it is a plain text file or a non breditor JSON file
        except (json.JSONDecodeError, KeyError):
            tags = None

        # Delete the current text in the text field
        edit_text.delete(1.0, tk.END)
        edit_text.insert(1.0, file_contents)

        # Apply the tags to the text and configure the tags, if they exist
        if tags:
            for tag in tags:
                edit_text.tag_configure(tag[0], font=(f"Calibri 11 {tag[0]}"))
                edit_text.tag_add(tag[0], tag[1], tag[2])

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

    # collect all the tags applied to the text and their positions
    tags = []
    for tag in edit_text.tag_names():
        if tag != "sel":
            ranges = edit_text.tag_ranges(tag)
            for i in range(0, len(ranges), 2):
                # create a list of tuples with the tag name, start and end position of the tag
                tags.append((tag, str(ranges[i]), str(ranges[i+1])))

    json_data = {
        "format": "json/breditor",
        "contents": data,
        "tags": tags
    }

    with open(file_path, 'w') as f:
        # only write json data if there are tags
        if len(tags) > 0:
            json.dump(json_data, f, indent=4)
        # if there are no tags, write the plain text to the file
        else:
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


def is_text_file(file_path):
    """
    Check if a file contains textual data.

    This function reads the first few bytes of the file and tries to decode them as UTF-8 text, returning either True or False.

    Please note that this method is not foolproof. Some binary files may start with bytes that can be decoded as text,
    and some text files may start with bytes that cannot be decoded as text. However, this method should work for most common cases.
    """
    # open the file in binary mode
    with open(file_path, 'rb') as file:
        # Read the first few bytes of the file
        sample = file.read(100)

    try:
        sample.decode('utf-8')
    except UnicodeDecodeError:
        return False
    return True
