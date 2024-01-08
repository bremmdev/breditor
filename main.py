import tkinter as tk
from widgets import create_topbar


def main():
    window = tk.Tk()
    window.title('Untitled - breditor')

    # create a text field
    edit_text = tk.Text(window)
    edit_text.pack(expand=True, fill=tk.BOTH)

    create_topbar(window, edit_text)

    window.mainloop()


if __name__ == "__main__":
    main()
