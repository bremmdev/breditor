import tkinter as tk


class FindDialog(tk.Toplevel):
    """
    A dialog for finding and optionally replacing text in a text widget.

    Attributes
    ----------
    parent : tk.Tk or tk.Toplevel
        The parent window to which this dialog belongs.
    text_widget : tk.Text
        The text widget in which to find and replace text.
    replace : bool, optional
        Whether to include the replace functionality (default is False).

    Methods
    -------
    create_widgets():
        Creates and packs the widgets for the dialog.
    on_close():
        Removes the 'found' tag from the text widget and destroys the dialog.
    find_all():
        Finds all occurrences of the query in the text widget and highlights them.
    highlight_text(query):
        Highlights all occurrences of the query in the text widget.
    replace_text():
        Replaces all occurrences of the query in the text widget with the replacement text.
    """

    _instance = None  # Class variable to hold the current instance

    def __init__(self, parent, text_widget, replace=False):
        if FindDialog._instance is not None:
            # If an instance already exists, destroy it
            FindDialog._instance.destroy()
            text_widget.tag_remove('found', '1.0', tk.END)
        FindDialog._instance = self  # Update the current instance

        super().__init__(parent)
        self.replace = replace
        title = "Find and Replace" if replace else "Find"
        self.title(title)
        self.text_widget = text_widget
        self.geometry("+%d+%d" %
                      (parent.winfo_rootx() + 80, parent.winfo_rooty() + 80))
        self.resizable(False, False)

        self.create_widgets()

        # Override the default close button behavior
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # create frame to hold the entry and button
        self.frame = tk.Frame(self)
        self.frame.pack(pady=(15, 0), padx=10, fill="x", expand=True)

        self.find_label = tk.Label(self.frame, text="Find:")
        self.find_label.pack(side="left", padx=(0, 5))
        self.find_entry = tk.Entry(
            self.frame, width=15 if self.replace else 30)
        self.find_entry.focus_set()

        self.find_entry.pack(side="left", padx=10, fill="none", expand=False)

        # add another entry for replace
        if self.replace:
            self.replace_label = tk.Label(self.frame, text="Replace:")
            self.replace_label.pack(side="left", padx=0)
            self.replace_entry = tk.Entry(self.frame, width=15)
            self.replace_entry.pack(side="left", padx=10)

        button_text = "Replace" if self.replace else "Find All"
        command = self.replace_text if self.replace else self.find_all
        action_button = tk.Button(
            self.frame, text=button_text, command=command)
        action_button.pack(side="right")

        # checkbox must have a variable to hold the state
        self.match_case_var = tk.BooleanVar()
        self.match_case_check = tk.Checkbutton(
            self, text="Match case", variable=self.match_case_var)
        self.match_case_check .pack(side="left", padx=(10, 0), pady=(0, 15))

    # on close window remove the tag
    def on_close(self):
        self.text_widget.tag_remove('found', '1.0', tk.END)
        self.destroy()

    def search_text(self, query, replace_text=None):
        """Helper method to search and optionally replace text."""
        self.text_widget.tag_remove('found', '1.0', tk.END)
        nocase = 1 if not self.match_case_var.get() else 0
        start = '1.0'
        while True:
            start = self.text_widget.search(
                query, start, stopindex=tk.END, nocase=nocase)
            if not start:
                break
            end = f'{start}+{len(query)}c'
            if replace_text is not None:
                self.text_widget.delete(start, end)
                self.text_widget.insert(start, replace_text)
            else:
                self.text_widget.tag_add('found', start, end)
            self.text_widget.tag_config('found', background='yellow')
            start = end

    def find_all(self):
        """Find all occurrences of the query and highlight them."""
        query = self.find_entry.get()
        if query:
            self.search_text(query)

    def replace_text(self):
        """Replace all occurrences of the query with the replacement text."""
        query = self.find_entry.get()
        replace_text = self.replace_entry.get()
        if query and replace_text:
            self.search_text(query, replace_text)
