import tkinter as tk
from interface import create_interface


def main():
    window = tk.Tk()
    window.title('Untitled - breditor')
    window.minsize(500, 500)
    create_interface(window)
    window.mainloop()


if __name__ == "__main__":
    main()
