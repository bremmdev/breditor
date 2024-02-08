import tkinter as tk
from file import open_file, new_file, save_file, save_file_as, prompt_save_changes, get_recent_files
from font import make_bold, make_italic, set_heading, configure_styles


def create_interface(window):
    edit_text = tk.Text(window, pady=20, wrap=tk.WORD,
                        bg="ghost white", border=0, font=("Calibri 11"))

    topbar, edit_menu = create_topbar(window, edit_text)
    toolbar = create_toolbar(window, edit_text)

    # pack edit_text after topbar and toolbar for correct position in window
    edit_text.pack(expand=True, fill=tk.BOTH)

    # get buttons from toolbar
    font_buttons = toolbar.winfo_children()[0].winfo_children()
    headings_buttons = toolbar.winfo_children()[1].winfo_children()
    all_buttons = font_buttons + headings_buttons

    # Configure the styles for the text widget
    configure_styles(edit_text)

    # Bind the <<Selection>> event to enable buttons
    edit_text.bind("<<Selection>>",
                   lambda event: on_selection(event, all_buttons, edit_menu))

    # Check if left mouse button is released to check if there is a selection
    edit_text.bind("<ButtonRelease-1>",
                   lambda event: on_button_release(event, all_buttons, edit_menu))

    edit_text.bind("<<Modified>>", lambda event: text_modified.set(True))

    edit_text.bind("<Control-b>", lambda event: make_bold(edit_text))
    edit_text.bind("<Control-i>", lambda event: make_italic(edit_text))

    text_modified = tk.BooleanVar(value=False)
    edit_text.focus_set()

    # Bind the window close event to the on_close_window function to prompt the user to save changes
    window.protocol("WM_DELETE_WINDOW",
                    lambda: on_close_window(window, edit_text))


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
    file_menu.add_cascade(
        label="Open Recent File", menu=tk.Menu(file_menu))
    file_menu.add_separator()
    file_menu.add_command(
        label="Save", command=lambda: save_file(window, edit_text), accelerator="Ctrl+S")
    file_menu.add_command(
        label="Save As", command=lambda: save_file_as(window, edit_text), accelerator="Ctrl+Shift+S")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: on_close_window(window, edit_text))

    # Get the recent files and add them to the recent files menu
    recent_files_menu = window.nametowidget('!menu.!menu.!menu')
    recent_files_menu.configure(
        bg="ghost white", fg="black", font=("Calibri 10"), tearoff=0)

    recent_files = get_recent_files()
    for file_path in recent_files:
        recent_files_menu.add_command(
            label=file_path, command=lambda path=file_path: open_file(window, edit_text, path))

    # Create a submenu for Edit
    edit_menu = tk.Menu(topbar, tearoff=0)
    edit_menu.configure(bg="ghost white", fg="black", font=("Calibri 10"))
    topbar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut", command=lambda: edit_text.event_generate(
        "<<Cut>>"), accelerator="Ctrl+X", state="disabled")
    edit_menu.add_command(label="Copy", command=lambda: edit_text.event_generate(
        "<<Copy>>"), accelerator="Ctrl+C", state="disabled")
    edit_menu.add_command(label="Paste", command=lambda: edit_text.event_generate(
        "<<Paste>>"), accelerator="Ctrl+V")

    # Keyboard accerelator events bindings
    window.bind("<Control-n>", lambda event: new_file(window, edit_text))
    window.bind("<Control-o>", lambda event: open_file(window, edit_text))
    window.bind("<Control-s>", lambda event: save_file(window, edit_text))
    window.bind("<Control-S>", lambda event: save_file_as(window, edit_text))

    return topbar, edit_menu


def create_button(parent, text, font, command):
    button = tk.Button(parent, text=text, width=2, font=font,
                       command=command, bg="ghost white")
    button.config(state="disabled")
    button.pack(side=tk.LEFT)
    return button


def create_toolbar(window, edit_text):
    # Create a toolbar
    toolbar = tk.Frame(window, bg="gray20", height=30, pady=8)
    toolbar.pack(side=tk.TOP, expand=False, fill=tk.X)

    font_options_bar = tk.Frame(toolbar, bg="gray20", padx=8)
    font_options_bar.pack(side=tk.LEFT, expand=False, fill=tk.X)

    headings_options_bar = tk.Frame(toolbar, bg="gray20", padx=8)
    headings_options_bar.pack(side=tk.LEFT, expand=False, fill=tk.X)

    # Create font buttons
    bold_button = create_button(
        font_options_bar, "B", ("Calibri 11 bold"), lambda: make_bold(edit_text))
    italic_button = create_button(
        font_options_bar, "I", ("Calibri 11 italic"), lambda: make_italic(edit_text))

    # Create headings buttons
    h1_button = create_button(headings_options_bar,
                              "H1", ("Calibri 11 bold"), lambda: set_heading(edit_text, "h1"))
    h2_button = create_button(headings_options_bar,
                              "H2", ("Calibri 11 bold"), lambda: set_heading(edit_text, "h2"))
    h3_button = create_button(headings_options_bar,
                              "H3", ("Calibri 11 bold"), lambda: set_heading(edit_text, "h3"))

    return toolbar


def on_selection(event, buttons, edit_menu):
    for b in buttons:
        b.config(state=tk.NORMAL)
    edit_menu.entryconfig("Cut", state="normal")
    edit_menu.entryconfig("Copy", state="normal")


def on_button_release(event, buttons, edit_menu):
    """
    Event handler for the left mouse button release event.

    It checks if there is any text selected in the widget that received the event. If
    there is selected text, it enables the selected buttons. If there is no selected text, it disables
    the provided buttons.
    """

    try:
        event.widget.get("sel.first", "sel.last")
        # If there is selected text, enable buttons
        for b in buttons:
            b.config(state=tk.NORMAL)
            edit_menu.entryconfig("Cut", state="normal")
            edit_menu.entryconfig("Copy", state="normal")
    except tk.TclError:
        # If there is no selected text, disable buttons
        for b in buttons:
            b.config(state=tk.DISABLED)
            edit_menu.entryconfig("Cut", state="disabled")
            edit_menu.entryconfig("Copy", state="disabled")


def on_close_window(window, edit_text):
    if edit_text.edit_modified():
        # Prompt the user to save the file
        chooses_to_save = prompt_save_changes(window, edit_text)
        if chooses_to_save is None:
            return
        else:
            window.destroy()
    else:
        window.destroy()
