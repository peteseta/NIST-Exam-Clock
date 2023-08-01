from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Listbox
from tkinter.constants import *

from style import HEADING

# list of sections, handles creating and removing sections, numbering, etc.
class EditorSectionList:
    pass

# add/remove section modification buttons
class EditorSectionModify(EditorSectionList):
    def __init__(self, parent):
        self.add_button = Button(
            parent,
            text="Add",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Add section clicked"),
            relief="flat"
        )
        self.remove_button = Button(
            parent,
            text="Remove",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Remove section clicked"),
            relief="flat"
        )

    # call place(self, index) to place the buttons below the last section
    def place(self, index):
        self.add_button.place(x=522.0, y=(277.0+(170*index)), width=100.0, height=47.0)
        self.remove_button.place(x=630, y=277.0+(170.0*index), width=100.0, height=47.0)
        
# section_buttons = EditorSectionModify(editor_canvas)
# section_buttons.place(0)

# section object
class EditorSection(EditorSectionList):
    def __init__(self, parent, section_number):
        self.x = 522.0
        self.y = 96.0
        self.section_bg = parent.create_rectangle(
            self.x,
            self.y,
            self.x + 600,
            self.y + 170,
            fill="#F5F5F5",
            outline=""
        )
        self.section_number = parent.create_text(
            self.x + 20,
            self.y + 20,
            anchor="nw",
            text=str(section_number),
            fill="#121212",
            font=("RobotoRoman Bold", 32 * -1)
        )
        self.separator_line = parent.create_rectangle(
            self.x + 47,
            self.y + 30,
            self.x + 52,
            self.y + 150,
            fill="#EEEEEE",
            outline=""
        )
        self.section_name_label = parent.create_text(
            self.x + 70,
            self.y + 30,
            anchor="nw",
            text="Section Name:",
            fill="#121212",
            font=("RobotoRoman Bold", 32 * -1)
        )
        self.section_name_entry = Entry(
            parent,
            bd=0,
            bg="#EEEEEE",
            fg="#000716",
            highlightthickness=0
        )
        self.section_name_entry.place(
            x=self.x + 300,
            y=self.y + 30,
            width=252,
            height=32
        )
        self.reading_time_label = parent.create_text(
            self.x + 70,
            self.y + 72,
            anchor="nw",
            text="Reading Time:",
            fill="#121212",
            font=("RobotoRoman Regular", 32 * -1)
        )
        self.reading_time_entry = Entry(
            parent,
            bd=0,
            bg="#EEEEEE",
            fg="#000716",
            highlightthickness=0
        )
        self.reading_time_entry.place(
            x=self.x + 300,
            y=self.y + 72,
            width=37,
            height=35
        )
        self.duration_label = parent.create_text(
            self.x + 70,
            self.y + 114,
            anchor="nw",
            text="Duration:",
            fill="#121212",
            font=("RobotoRoman Regular", 32 * -1)
        )
        self.hour_entry = Entry(
            parent,
            bd=0,
            bg="#EEEEEE",
            fg="#000716",
            highlightthickness=0
        )
        self.hour_entry.place(
            x=self.x + 200,
            y=self.y + 114,
            width=30,
            height=35
        )
        self.minute_entry = Entry(
            parent,
            bd=0,
            bg="#EEEEEE",
            fg="#000716",
            highlightthickness=0
        )
        self.minute_entry.place(
            x=self.x + 300,
            y=self.y + 114,
            width=37,
            height=35
        )
        
# section = EditorSection(editor_canvas, 1)

# new subject
class EditorNewSubject:
    def __init__(self, parent, callback):
        # init values for empty form
        self.subject_name = ""
        self.level = -1
        
        # for the App class to register the subjects
        self.callback = callback
        
        # init ui
        self.x = 41.0
        self.y = 97.0
        
        self.new_subject_bg = parent.create_rectangle(
            self.x,
            self.y,
            self.x + 439,
            self.y + 217,
            fill="#F5F5F5",
            outline=""
        )
        self.add_subject_label = parent.create_text(
            self.x,
            self.y - 49,
            anchor="nw",
            text="Add a new subject to the list:",
            fill="#000000",
            font=("RobotoRoman Bold", 32 * -1)
        )
        self.subject_name_label = parent.create_text(
            self.x + 25,
            self.y + 20,
            anchor="nw",
            text="Subject Name",
            fill="#121212",
            font=("RobotoRoman Bold", 32 * -1)
        )
        self.subject_name_entry = Entry(
            parent,
            bd=0,
            bg="#EEEEEE",
            fg="#000716",
            highlightthickness=0
        )
        self.subject_name_entry.place(
            x=self.x + 27,
            y=self.y + 60,
            width=376,
            height=51
        )
        self.level_label = parent.create_text(
            self.x + 30,
            self.y + 116,
            anchor="nw",
            text="Level: Not Selected",
            fill="#121212",
            font=("RobotoRoman Bold", 32 * -1)
        )
        self.hl_button = Button(
            parent,
            text="HL",
            fg="#FFFFFF",
            bg="#61CA6C",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.set_level(parent, 1),
            relief="flat"
        )
        self.hl_button.place(
            x=self.x + 78,
            y=self.y + 158,
            width=41,
            height=26
        )
        self.sl_button = Button(
            parent,
            text="SL",
            fg="#FFFFFF",
            bg="#4184EC",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.set_level(parent, 0),
            relief="flat"
        )
        self.sl_button.place(
            x=self.x + 31,
            y=self.y + 158,
            width=41,
            height=26
        )
        self.add_subject_button = Button(
            parent,
            text="Add",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.register_subject(parent),
            relief="flat"
        )
        self.add_subject_button.place(
            x=self.x + 300,
            y=self.y + 142,
            width=100,
            height=47
        )
    def set_level(self, parent, level):
        self.level = level
        
        label_text = "Level: " + ("SL" if level == 0 else "HL")
        parent.itemconfig(self.level_label, text=label_text)
    
    def register_subject(self, parent):
        self.subject_name = self.subject_name_entry.get()
        
        if self.subject_name.strip() == "" or self.level == -1:
            parent.itemconfig(self.add_subject_label, text="Invalid details!")
            return      
         
        self.callback(self.subject_name, self.level)


class EditorSubjectList:
    def __init__(self, parent, callback):
        self.callback = callback
        
        self.x = 0
        self.y = 0
        
        self.choose_subject_label = parent.create_text(
            self.x + 41,
            self.y + 335,
            anchor="nw",
            text="Choose subject to configure:",
            fill="#000000",
            font=HEADING[2]
        )
        self.subject_list = Listbox(
            parent,
            bd=0,
            bg="#F5F5F5",
            fg="#000716",
            highlightthickness=0,
            selectmode=SINGLE,
            
        )
        self.subject_list.place(
            x=self.x + 40,
            y=self.y + 385,
            width=440,
            height=325
        )
        
        self.subject_list.bind("<<ListboxSelect>>", self.handle_selection)
    
    def update_list(self, subjects):
        for subject in subjects:
            self.subject_list.insert(END, subject.name)

    def handle_selection(self, event):
        selected_index = self.subject_list.curselection()
        self.callback(selected_index)


# existing_subject_list = EditorSubjectList(editor_canvas)

class EditorApplyButtons:
    def __init__(self, parent):
        self.x = 0
        self.y = 0
        
        # IMAGE_CONFIRM = PhotoImage(file=relative_to_assets("button_6.png"))
        # IMAGE_CANCEL = PhotoImage(file=relative_to_assets("button_7.png"))
        
        self.confirm_button = Button(
            parent,
            text="Confirm",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )
        self.confirm_button.place(
            x=1319,
            y=25,
            width=172,
            height=46
        )
        self.cancel_button = Button(
            parent,
            text="Cancel",
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
        )
        self.cancel_button.place(
            x=1151,
            y=25,
            width=163.75146484375,
            height=46
        )

# confirm_cancel = ConfirmCancel(window, 0, 0)