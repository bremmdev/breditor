import tkinter as tk
from file import open_file, new_file, save_file, save_file_as
from font import make_bold, make_italic


def create_interface(window):
    edit_text = tk.Text(window, pady=20, wrap=tk.WORD,
                        bg="ghost white", border=0, font=("Calibri 11"))
    # Bind the <<Selection>> event to fire events on text selection
    create_topbar(window, edit_text)
    create_toolbar(window, edit_text)
    # pack edit_text after topbar and toolbar for correct position in window
    edit_text.pack(expand=True, fill=tk.BOTH)
    edit_text.focus_set()


def create_topbar(window, edit_text):
    # Create a topbar
    topbar = tk.Menu(window)
    window.config(menu=topbar)

    # Create a submenu for File
    file_menu = tk.Menu(topbar, tearoff=0)
    file_menu.configure(bg="ghost white", fg="black", font=("Calibri 10"))
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


def create_toolbar(window, edit_text):
    # Create a toolbar
    toolbar = tk.Frame(window, bg="gray20", height=30, pady=8)
    toolbar.pack(side=tk.TOP, expand=False, fill=tk.X)

    font_options_bar = tk.Frame(toolbar, bg="gray20", padx=8)
    font_options_bar.pack(side=tk.LEFT, expand=False, fill=tk.X)

    # Create font buttons
    bold_button = tk.Button(font_options_bar, text="B", width=2, font=(
        "Calibri 11 bold"), command=lambda: make_bold(edit_text), bg="ghost white")
    bold_button.config(state="disabled")
    bold_button.pack(side=tk.LEFT)

    italic_button = tk.Button(font_options_bar, text="I", width=2, font=(
        "Calibri 11 italic"), command=lambda: make_italic(edit_text),  bg="ghost white")
    italic_button.config(state="disabled")
    italic_button.pack(side=tk.LEFT)

    font_buttons = [bold_button, italic_button]
    
    # Bind the <<Selection>> event to enable buttons
    edit_text.bind("<<Selection>>",
                   lambda event: on_selection(event, font_buttons))

    # Check if left mouse button is released to check if there is a selection
    edit_text.bind("<ButtonRelease-1>",
                   lambda event: on_button_release(event, font_buttons))

    edit_text.bind("<Control-b>", lambda event: make_bold(edit_text))
    edit_text.bind("<Control-i>", lambda event: make_italic(edit_text))


def on_selection(event, font_buttons):
    for b in font_buttons:
        b.config(state=tk.NORMAL)


def on_button_release(event, font_buttons):
    """
    Event handler for the left mouse button release event.

    It checks if there is any text selected in the widget that received the event. If
    there is selected text, it enables the selected buttons. If there is no selected text, it disables
    the provided buttons.
    """

    try:
        selected_text = event.widget.get("sel.first", "sel.last")
        # If there is selected text, enable buttons
        for b in font_buttons:
            b.config(state=tk.NORMAL)
    except tk.TclError:
        # If there is no selected text, disable buttons
        for b in font_buttons:
            b.config(state=tk.DISABLED)
