def set_style(edit_text, font_style):
    current_tags = get_current_tags(edit_text)

    # remove the heading tag if it exists
    heading_tag = [tag for tag in current_tags if "heading" in tag]
    if heading_tag:
        edit_text.tag_remove(heading_tag[0], "sel.first", "sel.last")

    if (edit_text.edit_modified() == False):
        edit_text.edit_modified(True)

    # if there are no bold, italic or bold italic tags, add the tag
    style_tags = ["bold", "italic", "bold italic"]
    has_style_tag = any(tag in current_tags for tag in style_tags)
    if not has_style_tag:
        edit_text.tag_add(font_style, "sel.first", "sel.last")
        return

    # text is already bold and italic, remove correct tag
    if "bold italic" in current_tags:
        new_style = "bold" if font_style == "italic" else "italic"
        edit_text.tag_remove("bold italic", "sel.first", "sel.last")
        edit_text.tag_add(new_style, "sel.first", "sel.last")
        return

    if font_style in current_tags:
        edit_text.tag_remove(font_style, "sel.first", "sel.last")
    else:
        style_to_remove = "bold" if font_style == "italic" else "italic"
        edit_text.tag_remove(style_to_remove, "sel.first", "sel.last")
        edit_text.tag_add("bold italic", "sel.first", "sel.last")


def get_current_tags(edit_text):
    # get the selected text
    selected_text = edit_text.get("sel.first", "sel.last")
    if not selected_text:
        return []

    # check if there are any tags applied to the selected text
    current_tags = [tag for tag in edit_text.tag_names(
        "sel.first") if tag != "sel"]

    return current_tags


def make_bold(edit_text):
    set_style(edit_text, "bold")
    # prevent the default windows binding
    return "break"


def make_italic(edit_text):
    set_style(edit_text, "italic")
    # prevent the default windows binding for ctrl + i
    return "break"


def set_heading(edit_text, heading):
    current_tags = get_current_tags(edit_text)

    # if it is the same heading, remove all tags
    if f"heading-{heading}" in current_tags:
        edit_text.tag_remove(f"heading-{heading}", "sel.first", "sel.last")
        return

    # remove all tags before adding the new one
    if current_tags:
        for tag in current_tags:
            edit_text.tag_remove(tag, "sel.first", "sel.last")

    edit_text.tag_add(f"heading-{heading}", "sel.first", "sel.last")
    if (edit_text.edit_modified() == False):
        edit_text.edit_modified(True)


def configure_styles(edit_text):
    """
    Configure the styles for the given Text widget. Called on initialisation of the application.

    This function creates and configures the "bold", "italic", "bold italic", and heading tags for the given Text widget.
    """
    # Create the bold, italic and bold italic tags
    style_tags = ["bold", "italic", "bold italic"]
    for tag in style_tags:
        edit_text.tag_configure(tag, font=(f"Calibri 11 {tag}"))

    # Create the heading tags
    heading_to_font = {
        "h1": "Calibri 24 bold",
        "h2": "Calibri 20 bold",
        "h3": "Calibri 16 bold"
    }
    for heading, font in heading_to_font.items():
        edit_text.tag_configure(f"heading-{heading}", font=font)
