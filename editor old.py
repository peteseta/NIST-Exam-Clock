
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1520x760")
window.configure(bg = "#FFFFFF")


editor_canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 760,
    width = 1520,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

editor_canvas.place(x = 0, y = 0)

# ----------------------------

# add/remove section modification buttons
add_section_button = Button(
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    text="Add"
)

add_section_button.place(
    x=522.0,
    y=277.0,
    width=100.0,
    height=47.0
)

remove_section_button = Button(
    text="Remove",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)

remove_section_button.place(
    x=630.0,
    y=277.0,
    width=100.0,
    height=47.0
)

# section object
section_bg = editor_canvas.create_rectangle(
    522.0,
    96.0,
    1122.0,
    266.0,
    fill="#F5F5F5",
    outline=""
)

section_number = editor_canvas.create_text(
    542.0,
    116.0,
    anchor="nw",
    text="1",
    fill="#121212",
    font=("RobotoRoman Bold", 32 * -1)
)

separator_line = editor_canvas.create_rectangle(
    569.0,
    120.0,
    574.0,
    237.0,
    fill="#EEEEEE",
    outline=""
)

editor_canvas.create_text(
    593.0,
    122.0,
    anchor="nw",
    text="Section Name:",
    fill="#121212",
    font=("RobotoRoman Bold", 32 * -1)
)

section_name_entry = Entry(
    bd=0,
    bg="#EEEEEE",
    fg="#000716",
    highlightthickness=0
)

section_name_entry.place(
    x=828.0,
    y=122.0,
    width=252.0,
    height=32.0
)

editor_canvas.create_text(
    593.0,
    164.0,
    anchor="nw",
    text="Reading Time:",
    fill="#121212",
    font=("RobotoRoman Regular", 32 * -1)
)

reading_time_entry = Entry(
    bd=0,
    bg="#EEEEEE",
    fg="#000716",
    highlightthickness=0
)
reading_time_entry.place(
    x=816.0,
    y=164.0,
    width=37.0,
    height=35.0
)

editor_canvas.create_text(
    866.0,
    166.0,
    anchor="nw",
    text="m",
    fill="#121212",
    font=("RobotoRoman Regular", 32 * -1)
)

editor_canvas.create_text(
    593.0,
    208.0,
    anchor="nw",
    text="Duration:",
    fill="#121212",
    font=("RobotoRoman Regular", 32 * -1)
)

hour_entry = Entry(
    bd=0,
    bg="#EEEEEE",
    fg="#000716",
    highlightthickness=0
)
hour_entry.place(
    x=734.0,
    y=208.0,
    width=30.0,
    height=35.0
)

editor_canvas.create_text(
    777.0,
    208.0,
    anchor="nw",
    text="h",
    fill="#121212",
    font=("RobotoRoman Regular", 32 * -1)
)

minute_entry = Entry(
    bd=0,
    bg="#EEEEEE",
    fg="#000716",
    highlightthickness=0
)
minute_entry.place(
    x=816.0,
    y=208.0,
    width=37.0,
    height=35.0
)

editor_canvas.create_text(
    866.0,
    208.0,
    anchor="nw",
    text="m",
    fill="#121212",
    font=("RobotoRoman Regular", 32 * -1)
)

# new subject
new_subject_bg = editor_canvas.create_rectangle(
    41.0,
    97.0,
    480.0,
    314.0,
    fill="#F5F5F5",
    outline="")

editor_canvas.create_text(
    46.0,
    48.0,
    anchor="nw",
    text="Add a new subject to the list:",
    fill="#000000",
    font=("RobotoRoman Bold", 32 * -1)
)

editor_canvas.create_text(
    62.0,
    114.0,
    anchor="nw",
    text="Subject Name",
    fill="#121212",
    font=("RobotoRoman Bold", 32 * -1)
)

subject_name_entry = Entry(
    bd=0,
    bg="#EEEEEE",
    fg="#000716",
    highlightthickness=0
)
subject_name_entry.place(
    x=68.0,
    y=156.0,
    width=376.0,
    height=51.0
)

editor_canvas.create_text(
    62.0,
    220.263427734375,
    anchor="nw",
    text="Level",
    fill="#121212",
    font=("RobotoRoman Bold", 32 * -1)
)

IMAGE_HL = PhotoImage(
    file="assets/frame1/button_4.png")
hl_button = Button(
    image=IMAGE_HL,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat"
)
hl_button.place(
    x=109.0,
    y=262.0,
    width=41.0,
    height=26.67449951171875
)

IMAGE_SL = PhotoImage(
    file="assets/frame1/button_5.png")
sl_button = Button(
    image=IMAGE_SL,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat"
)
sl_button.place(
    x=62.0,
    y=262.0,
    width=41.3779296875,
    height=26.793624877929688
)

add_subject_button = Button(
    text="Add",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
add_subject_button.place(
    x=350.0,
    y=247.0,
    width=100.0,
    height=47.0
)

# existing subject list
editor_canvas.create_text(
    41.0,
    335.0,
    anchor="nw",
    text="Choose subject to configure:",
    fill="#000000",
    font=("RobotoRoman Bold", 32 * -1)
)

subject_list = Text(
    bd=0,
    bg="#F5F5F5",
    fg="#000716",
    highlightthickness=0
)
subject_list.place(
    x=53.0,
    y=385.0,
    width=415.0,
    height=325.0
)

# confirm/cancel
IMAGE_CONFIRM = PhotoImage(
    file=relative_to_assets("button_6.png"))
confirm_button = Button(
    image=IMAGE_CONFIRM,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat"
)
confirm_button.place(
    x=1319.0,
    y=25.0,
    width=172.0,
    height=46.0
)

IMAGE_CANCEL = PhotoImage(
    file=relative_to_assets("button_7.png"))
cancel_button = Button(
    image=IMAGE_CANCEL,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_7 clicked"),
    relief="flat"
)
cancel_button.place(
    x=1151.0,
    y=25.0,
    width=163.75146484375,
    height=46.0
)

window.resizable(False, False)
window.mainloop()