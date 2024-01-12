def set_style(edit_text, font_style):
    # get the selected text
    selected_text = edit_text.get("sel.first", "sel.last")
    if not selected_text:
        return "break"

    # check if there are any tags applied to the selected text
    current_tags = [tag for tag in edit_text.tag_names(
        "sel.first") if tag != "sel"]

    # if there are no tags applied, apply the selected tag
    if not current_tags:
        add_tag(edit_text, font_style)
        return

    # text is already bold and italic, remove correct tag
    if "bold italic" in current_tags:
        new_style = "bold" if font_style == "italic" else "italic"
        edit_text.tag_remove("bold italic", "sel.first", "sel.last")
        add_tag(edit_text, new_style)
        return

    if font_style in current_tags:
        edit_text.tag_remove(font_style, "sel.first", "sel.last")
    else:
        style_to_remove = "bold" if font_style == "italic" else "italic"
        edit_text.tag_remove(style_to_remove, "sel.first", "sel.last")
        add_tag(edit_text, "bold italic")


def add_tag(edit_text, style):
    edit_text.tag_add(style, "sel.first", "sel.last")
    edit_text.tag_configure(style, font=(f"Calibri 11 {style}"))


def make_bold(edit_text):
    set_style(edit_text, "bold")
    # prevent the default windows binding
    return "break"


def make_italic(edit_text):
    set_style(edit_text, "italic")
    # prevent the default windows binding for ctrl + i
    return "break"
