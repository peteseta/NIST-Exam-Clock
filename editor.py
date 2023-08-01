from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Listbox
from tkinter.constants import *
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame

from style import HEADING, round_rectangle

# list of sections, handles creating and removing sections, numbering, etc.
class EditorSectionList:
    def __init__(self, parent, existing_sections, callback) -> None:
        self.parent = parent
        self.callback = callback
        
        # stores the UI components
        self.components = []
        self.section_count = 0
        
        # if there are existing sections, populate components
        if len(existing_sections) > 0:
            self.section_count = len(existing_sections)
            for index, section in enumerate(existing_sections):
                self.components.append(EditorSection())
        
        # init heading
        self.parent.create_text(
            522,
            48,
            anchor="nw",
            text="Sections:",
            fill="#121212",
            font=HEADING[1]
        )

        self.modify = EditorSectionModify(self.parent, self)
    
    def add_section(self):
        self.section_count += 1
        
        self.modify.destroy()
        self.modify = EditorSectionModify(self.parent, self)
        
        self.components.append(EditorSection(self.parent, self.section_count))
        
    def remove_section(self):
        self.section_count -= 1
        
        self.modify.destroy()
        self.modify = EditorSectionModify(self.parent, self)
        
        self.components[-1].canvas.destroy()
        self.components.pop(-1)
        
    def apply(self):
        print("sections modified")
        # use self.callback to call main.py -> EditorPage.register_sections()
    
    def destroy(self):
        self.modify.destroy()
        for component in self.components:
            component.canvas.destroy()
        

class EditorSection:
    def __init__(self, parent, section_count):
        self.canvas = Canvas(parent, width=600, height=170)
        self.canvas.place(x=522.0, y=(96.0 + (188 * (section_count - 1))))
        
        self.section_bg = round_rectangle(
            self.canvas,
            0,
            0,
            600,
            170,
            radius=12,
            fill="#F5F5F5",
            outline=""
        )
        self.section_number = self.canvas.create_text(
            20,
            20,
            anchor="nw",
            text=str(section_count),
            fill="#121212",
            font=HEADING[3]
        )
        self.separator_line = self.canvas.create_rectangle(
            47,
            30,
            52,
            150,
            fill="#EEEEEE",
            outline=""
        )
        self.section_name_label = self.canvas.create_text(
            70,
            30,
            anchor="nw",
            text="Section Name:",
            fill="#121212",
            font=HEADING[3]
        )
        self.section_name_entry = ttk.Entry(
            self.canvas,
            bootstyle="dark",
        )
        self.section_name_entry.place(
            x=300,
            y=30,
            width=252,
            height=32
        )
        self.reading_time_label = self.canvas.create_text(
            70,
            72,
            anchor="nw",
            text="Reading Time:",
            fill="#121212",
            font=HEADING[3]
        )
        self.reading_time_entry = ttk.Entry(
            self.canvas,
            bootstyle="dark",
        )
        self.reading_time_entry.place(
            x=300,
            y=72,
            width=37,
            height=35
        )
        self.canvas.create_text(
            350,
            72,
            anchor="nw",
            text="m",
            fill="#121212",
            font=HEADING[3]
        )
        self.duration_label = self.canvas.create_text(
            70,
            114,
            anchor="nw",
            text="Duration:",
            fill="#121212",
            font=HEADING[3]
        )
        self.hour_entry = ttk.Entry(
            self.canvas,
            bootstyle="dark",
        )
        self.hour_entry.place(
            x=200,
            y=114,
            width=30,
            height=35
        )
        self.canvas.create_text(
            250,
            114,
            anchor="nw",
            text="h",
            fill="#121212",
            font=HEADING[3]
        )
        self.minute_entry = ttk.Entry(
            self.canvas,
            bootstyle="dark",
        )
        self.minute_entry.place(
            x=300,
            y=114,
            width=37,
            height=35
        )
        self.canvas.create_text(
            350,
            114,
            anchor="nw",
            text="m",
            fill="#121212",
            font=HEADING[3]
        )

# add/remove section modification buttons
class EditorSectionModify:
    def __init__(self, parent, controller):
        self.controller = controller
        
        # place at the very top if there are no sections yet
        if self.controller.section_count == 0:
            self.x = 522
            self.y = 100
        # otherise place at the end of the last section
        else:
            self.x = 522
            self.y = 285+(188 * (self.controller.section_count - 1))
        
        self.add_button = ttk.Button(
            parent,
            text="Add",
            command=lambda: self.controller.add_section(),
            bootstyle="light"
        )
        self.add_button.place(x=self.x, y=self.y, width=100, height=47)
        
        self.remove_button = ttk.Button(
            parent,
            text="Remove",
            command=lambda: self.controller.remove_section(),
            bootstyle="danger",
            state=("disabled" if controller.section_count == 0 else "active")
        )
        self.remove_button.place(x=self.x+110, y=self.y, width=100, height=47)
        
        self.save_button = ttk.Button(
            parent,
            text="Save",
            command=lambda: self.controller.apply(),
            bootstyle="success",
            state="disabled"
        )
        self.save_button.place(x=self.x+220, y=self.y, width=100, height=47)
    
    def destroy(self):
        self.add_button.destroy()
        self.remove_button.destroy()
        self.save_button.destroy()
        
# section_buttons = EditorSectionModify(editor_canvas)
# section_buttons.place(0)

class EditorNewSubject:
    def __init__(self, parent, callback):
        self.parent = parent
        
        # init values for empty form
        self.subject_name = ""
        self.level = -1
        
        # for the App class to register the subjects
        self.callback = callback
        
        # init ui
        self.x = 41.0
        self.y = 97.0
        
        self.new_subject_bg = round_rectangle(
            self.parent,
            self.x,
            self.y,
            self.x + 439,
            self.y + 217,
            radius=20,
            fill="#F5F5F5",
            outline=""
        )
        self.add_subject_label = self.parent.create_text(
            self.x,
            self.y - 49,
            anchor="nw",
            text="Add a new subject to the list:",
            fill="#000000",
            font=HEADING[1]
        )
        self.subject_name_label = self.parent.create_text(
            self.x + 30,
            self.y + 25,
            anchor="nw",
            text="Subject Name",
            fill="#121212",
            font=HEADING[2]
        )
        self.subject_name_entry = Entry(
            self.parent,
            bd=0,
            bg="#EEEEEE",
            fg="#000716",
            font=HEADING[3],
            highlightthickness=0
        )
        self.subject_name_entry.place(
            x=self.x + 27,
            y=self.y + 60,
            width=376,
            height=51
        )
        self.level_label = self.parent.create_text(
            self.x + 30,
            self.y + 125,
            anchor="nw",
            text="Level: Not Selected",
            fill="#121212",
            font=HEADING[2]
        )
        self.hl_button = ttk.Button(
            self.parent,
            text="HL",
            bootstyle="success",
            command=lambda: self.set_level(1),
        )
        self.hl_button.place(
            x=self.x + 78,
            y=self.y + 158,
            width=41,
            height=26
        )
        self.sl_button = ttk.Button(
            self.parent,
            text="SL",
            bootstyle="info",
            command=lambda: self.set_level(0),
        )
        self.sl_button.place(
            x=self.x + 31,
            y=self.y + 158,
            width=41,
            height=26
        )
        self.add_subject_button = ttk.Button(
            self.parent,
            text="Add",
            bootstyle="dark",
            command=lambda: self.register_subject(),
        )
        self.add_subject_button.place(
            x=self.x + 300,
            y=self.y + 142,
            width=100,
            height=47
        )
    def set_level(self, level):
        self.level = level
        
        label_text = "Level: " + ("SL" if level == 0 else "HL")
        self.parent.itemconfig(self.level_label, text=label_text)
    
    def register_subject(self):
        self.subject_name = self.subject_name_entry.get()
        
        if self.subject_name.strip() == "" or self.level == -1:
            self.status_msg("Please fill in all fields")
            return      
         
        self.reset_msg()
        self.callback(self.subject_name.strip(), self.level)
    
    def status_msg(self, message):
        self.parent.itemconfig(self.add_subject_label, fill="#FF0000", text=message)
    
    def reset_msg(self):
        self.parent.itemconfig(self.add_subject_label, fill="#000000", text="Add a new subject to the list:")
             
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
            font=HEADING[1]
        )
        self.subject_list = Listbox(
            parent,
            bd=0,
            bg="#F5F5F5",
            fg="#000716",
            font=HEADING[4],
            highlightthickness=0,
            selectmode=SINGLE,
        )
        self.subject_list.place(
            x=self.x + 40,
            y=self.y + 385,
            width=440,
            height=285
        )
        
        self.subject_list.bind("<<ListboxSelect>>", self.handle_selection)

    def update_list(self, subjects):
        self.subject_list.delete(0, END)
        
        for subject in subjects:
            display_name = subject.name + (" HL" if subject.level == 1 else " SL")
            self.subject_list.insert(END, display_name)

    def handle_selection(self, event):
        selected_index = self.subject_list.curselection()
        self.callback(selected_index)

# i dont think we need this


# confirm_cancel = ConfirmCancel(window, 0, 0)