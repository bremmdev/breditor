import tkinter as tk
from file import open_file, new_file, save_file, save_file_as


def main():
    window = tk.Tk()
    window.title('Untitled - breditor')

    # Create a topbar
    topbar = tk.Menu(window)
    window.config(menu=topbar)

    # Create a submenu for File
    file_menu = tk.Menu(topbar, tearoff=0)
    topbar.add_cascade(label="File", menu=file_menu)

    file_menu.add_command(
        label="New", command=lambda: new_file(window, edit_text))
    file_menu.add_command(
        label="Open", command=lambda: open_file(window, edit_text))
    file_menu.add_command(
        label="Save", command=lambda: save_file(window, edit_text))
    file_menu.add_command(
        label="Save As", command=lambda: save_file_as(window, edit_text))

    # create a text field
    edit_text = tk.Text(window)
    edit_text.pack(expand=True, fill=tk.BOTH)

    window.mainloop()


if __name__ == "__main__":
    main()
