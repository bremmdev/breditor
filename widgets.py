import tkinter as tk
from file import open_file, new_file, save_file, save_file_as


def create_topbar(window, edit_text):
   # Create a topbar
    topbar = tk.Menu(window)
    window.config(menu=topbar)

    # Create a submenu for File
    file_menu = tk.Menu(topbar, tearoff=0)
    topbar.add_cascade(label="File", menu=file_menu)

    file_menu.add_command(
        label="New", command=lambda: new_file(window, edit_text), accelerator="Ctrl+N")
    file_menu.add_command(
        label="Open", command=lambda: open_file(window, edit_text), accelerator="Ctrl+O")
    file_menu.add_command(
        label="Save", command=lambda: save_file(window, edit_text), accelerator="Ctrl+S")
    file_menu.add_command(
        label="Save As", command=lambda: save_file_as(window, edit_text), accelerator="Ctrl+Shift+S")

    window.bind("<Control-n>", lambda event: new_file(window, edit_text))
    window.bind("<Control-o>", lambda event: open_file(window, edit_text))
    window.bind("<Control-s>", lambda event: save_file(window, edit_text))
    window.bind("<Control-S>", lambda event: save_file_as(window, edit_text))
