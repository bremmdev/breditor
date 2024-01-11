def make_bold(edit_text):
    # get the selected text
    selected_text = edit_text.get("sel.first", "sel.last")
    if not selected_text:
        return

    # get the current tags
    current_tags = edit_text.tag_names("sel.first")

    # if the selected text is already bold, remove the tag
    if "bold" in current_tags:
        edit_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        edit_text.tag_add("bold", "sel.first", "sel.last")
        new_tags = edit_text.tag_names("sel.first")
        edit_text.tag_configure("bold", font=("Calibri", "11", " ".join(
            [t if t != 'sel' else '' for t in new_tags])))


def make_italic(edit_text):
    selected_text = edit_text.get("sel.first", "sel.last")
    if not selected_text:
        return

    current_tags = edit_text.tag_names("sel.first")

    # if the selected text is already bold, remove the tag
    if "italic" in current_tags:
        edit_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        edit_text.tag_add("italic", "sel.first", "sel.last")
        new_tags = edit_text.tag_names("sel.first")
        edit_text.tag_configure("italic", font=(
            "Calibri", "11", " ".join([t if t != 'sel' else '' for t in new_tags])))
    # prevent the default windows binding for ctrl + i
    return "break"
