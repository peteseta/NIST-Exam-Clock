from tkinter import Canvas, Entry, Listbox, StringVar, IntVar
from tkinter.constants import *
import ttkbootstrap as ttk

from style import HEADING, round_rectangle


# list of sections, handles creating and removing sections, numbering, etc.
class EditorSectionList:
    def __init__(self, parent, existing_sections, callback) -> None:
        """
        Init a new instance of the UI component for editing a subject's sections

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            existing_sections (list): List of Section objects the selected subject already has
            callback (function): EditorPage.register_sections() unfolds the section data and stores them as Section objects in the selected subject's Subject.sections list
        """
        self.parent = parent
        self.callback = callback

        # stores the UI components
        self.components = []
        self.section_count = 0

        # if there are existing sections, populate components and enable save button
        if len(existing_sections) > 0:
            for index, section in enumerate(existing_sections):
                self.components.append(
                    EditorSection(
                        self.parent,
                        self,
                        index + 1,
                        section.name,
                        section.reading_time,
                        section.hours,
                        section.minutes,
                    )
                )

            self.section_count = len(existing_sections)

        # init heading
        self.parent.create_text(
            522, 48, anchor="nw", text="Sections:", fill="#121212", font=HEADING[1]
        )

        self.modify = EditorSectionModify(self.parent, self)
        self.validate_entries()  # in the case of pre-populated sections

    def add_section(self):
        """
        Adds a new UI element for configuring an additional section and moves the modification buttons below the last section element.
        """
        self.section_count += 1
        self.modify.place()  # move modification buttons

        self.components.append(EditorSection(self.parent, self, self.section_count))

        self.validate_entries()

    def remove_section(self):
        """
        Removes the last UI element for configuring a section and moves the modification buttons below the last section element.
        """
        self.section_count -= 1
        self.modify.place()  # move modification buttons

        self.components[-1].canvas.destroy()
        self.components.pop(-1)

        self.validate_entries()

    def validate_entries(self, *args):
        """
        Checks if all the section details are properly filled out - each section must have a name and at least 1 minute duration, excluding reading time. If all entries are valid, the Save button in EdittorSectionModify is enabled.

        Accepts *args due to trace_add() requiring a callback with a certain number of arguments
        """
        for component in self.components:
            if (component.name_var.get() == "") or (
                (component.hours_var.get() + component.minutes_var.get()) == 0
            ):
                self.modify.save_button.config(state="disabled")
                return

        # enable the Save button if all entries are filled
        self.modify.save_button.config(state="active")

    def apply(self):
        """
        Retrives the data from all the entries and passes them to the callback as parallel arrays
        """
        name_list = [component.name_var.get() for component in self.components]
        reading_time_list = [
            component.reading_time_var.get() for component in self.components
        ]
        hours_list = [component.hours_var.get() for component in self.components]
        minutes_list = [component.minutes_var.get() for component in self.components]

        self.callback(name_list, reading_time_list, hours_list, minutes_list)

    def destroy(self):
        """
        When a new subject is selected, destroy() is called to cleanup the old subject
        before a new instance of EditorSectionList is created to configure the new subject's sections
        """
        self.modify.add_button.destroy()
        self.modify.remove_button.destroy()
        self.modify.save_button.destroy()

        for component in self.components:
            component.canvas.destroy()


class EditorSection:
    def __init__(
        self,
        parent,
        controller,
        section_number,
        name="",
        reading_time=0,
        hours=0,
        minutes=0,
    ) -> None:
        """
        Initialize a UI component representing one section of a subject

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            controller (EditorSectionList object): Parent object "overseeing" the list of EditorSection's
            section_number (int): Index (1, 2, 3...) of current section to be displayed as the section number
            name (str, optional): Name of section (if existing). Defaults to "".
            reading_time (int, optional): Reading time for section (if existing). Defaults to 0.
            hours (int, optional): Hour duration of section (if existing). Defaults to 0.
            minutes (int, optional): Minute duration of section (if existing). Defaults to 0.
        """
        self.controller = controller
        self.canvas = Canvas(parent, width=600, height=170)
        self.canvas.place(x=522.0, y=(96.0 + (188 * (section_number - 1))))

        # values will be populated if section already exists
        self.name_var = StringVar(self.canvas, value=name)
        self.reading_time_var = IntVar(self.canvas, value=reading_time)
        self.hours_var = IntVar(self.canvas, value=hours)
        self.minutes_var = IntVar(self.canvas, value=minutes)

        # each time an entry is modified run the validation
        self.name_var.trace_add("write", self.controller.validate_entries)
        self.hours_var.trace_add("write", self.controller.validate_entries)
        self.minutes_var.trace_add("write", self.controller.validate_entries)

        self.section_bg = round_rectangle(
            self.canvas, 0, 0, 600, 170, radius=12, fill="#F5F5F5", outline=""
        )
        self.section_number = self.canvas.create_text(
            20,
            25,
            anchor="nw",
            text=str(section_number),
            fill="#121212",
            font=HEADING[2],
        )
        self.separator_line = self.canvas.create_rectangle(
            47, 30, 52, 150, fill="#EEEEEE", outline=""
        )
        self.section_name_label = self.canvas.create_text(
            70, 30, anchor="nw", text="Section Name:", fill="#121212", font=HEADING[3]
        )
        self.section_name_entry = ttk.Entry(
            self.canvas, bootstyle="dark", textvariable=self.name_var
        )
        self.section_name_entry.place(x=300, y=30, width=252, height=32)
        self.reading_time_label = self.canvas.create_text(
            70, 72, anchor="nw", text="Reading Time:", fill="#121212", font=HEADING[3]
        )
        self.reading_time_entry = ttk.Entry(
            self.canvas, bootstyle="dark", textvariable=self.reading_time_var
        )
        self.reading_time_entry.place(x=300, y=72, width=37, height=35)
        self.canvas.create_text(
            350, 72, anchor="nw", text="m", fill="#121212", font=HEADING[3]
        )
        self.duration_label = self.canvas.create_text(
            70, 114, anchor="nw", text="Duration:", fill="#121212", font=HEADING[3]
        )
        self.hour_entry = ttk.Entry(
            self.canvas, bootstyle="dark", textvariable=self.hours_var
        )
        self.hour_entry.place(x=200, y=114, width=30, height=35)
        self.canvas.create_text(
            250, 114, anchor="nw", text="h", fill="#121212", font=HEADING[3]
        )
        self.minute_entry = ttk.Entry(
            self.canvas, bootstyle="dark", textvariable=self.minutes_var
        )
        self.minute_entry.place(x=300, y=114, width=37, height=35)
        self.canvas.create_text(
            350, 114, anchor="nw", text="m", fill="#121212", font=HEADING[3]
        )


# add/remove section modification buttons
class EditorSectionModify:
    def __init__(self, parent, controller):
        """
        UI component for the Add, Remove, Save buttons at the bottom of the section list

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            controller (EditorSectionList object): Parent object "overseeing" the list of EditorSection's
        """
        self.controller = controller

        self.add_button = ttk.Button(
            parent,
            text="Add",
            command=lambda: self.controller.add_section(),
            bootstyle="light",
        )
        self.remove_button = ttk.Button(
            parent,
            text="Remove",
            command=lambda: self.controller.remove_section(),
            bootstyle="danger",
            state=("disabled" if controller.section_count == 0 else "active"),
        )
        self.save_button = ttk.Button(
            parent,
            text="Save",
            command=lambda: self.controller.apply(),
            bootstyle="success",
            state="disabled",
        )

        self.place()

    def place(self):
        """
        Moves the modification button to the appropriate place below the last section UI element
        """

        # place at the very top if there are no sections yet
        if self.controller.section_count == 0:
            self.x = 522
            self.y = 100

        # otherise place at the end of the last section
        else:
            self.x = 522
            self.y = 285 + (188 * (self.controller.section_count - 1))

        self.add_button.place(x=self.x, y=self.y, width=100, height=47)
        self.remove_button.place(x=self.x + 110, y=self.y, width=100, height=47)
        self.save_button.place(x=self.x + 220, y=self.y, width=100, height=47)


class EditorNewSubject:
    def __init__(self, parent, callback):
        """
        Initializes the UI component for adding a new subject (naming and selecting its level)

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            callback (function): callback to EditorPage.create_subject to register the subejct.
            It first checks for a duplicate then stores the subject details in the list App.subjects as a new Subject object
        """
        self.parent = parent
        self.callback = callback

        self.subject_name = ""
        self.level = -1

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
            outline="",
        )
        self.add_subject_label = self.parent.create_text(
            self.x,
            self.y - 49,
            anchor="nw",
            text="Add a new subject to the list:",
            fill="#000000",
            font=HEADING[1],
        )
        self.subject_name_label = self.parent.create_text(
            self.x + 30,
            self.y + 25,
            anchor="nw",
            text="Subject Name",
            fill="#121212",
            font=HEADING[2],
        )
        self.subject_name_entry = Entry(
            self.parent,
            bd=0,
            bg="#EEEEEE",
            fg="#000716",
            font=HEADING[3],
            highlightthickness=0,
        )
        self.subject_name_entry.place(
            x=self.x + 27, y=self.y + 60, width=376, height=51
        )
        self.level_label = self.parent.create_text(
            self.x + 30,
            self.y + 125,
            anchor="nw",
            text="Level: Not Selected",
            fill="#121212",
            font=HEADING[2],
        )
        self.hl_button = ttk.Button(
            self.parent,
            text="HL",
            bootstyle="success",
            command=lambda: self.set_level(1),
        )
        self.hl_button.place(x=self.x + 78, y=self.y + 158, width=41, height=26)
        self.sl_button = ttk.Button(
            self.parent,
            text="SL",
            bootstyle="info",
            command=lambda: self.set_level(0),
        )
        self.sl_button.place(x=self.x + 31, y=self.y + 158, width=41, height=26)
        self.add_subject_button = ttk.Button(
            self.parent,
            text="Add",
            bootstyle="dark",
            command=lambda: self.register_subject(),
        )
        self.add_subject_button.place(
            x=self.x + 300, y=self.y + 142, width=100, height=47
        )

    def set_level(self, level):
        """
        Updates the label to give visual feedback on the selected level when a level button is clicked

        Args:
            level (int): 0 means SL, 1 means HL
        """
        self.level = level

        label_text = "Level: " + ("SL" if level == 0 else "HL")
        self.parent.itemconfig(self.level_label, text=label_text)

    def register_subject(self):
        """
        Called when "add subject" is clicked. Calls the callback function to store the subject.
        The entries are validated before the callback is called (so garbage data isn't passed on).
        If anything is invalid a status message is displayed.
        """
        self.subject_name = self.subject_name_entry.get()

        if self.subject_name.strip() == "" or self.level == -1:
            self.status_msg("Please fill in all fields")
            return

        self.reset_msg()
        self.callback(self.subject_name.strip(), self.level)

    def status_msg(self, message):
        """
        Shorthand function to display a status (error) message in red

        Args:
            message (string): Message to display
        """
        self.parent.itemconfig(self.add_subject_label, fill="#FF0000", text=message)

    def reset_msg(self):
        """
        Shorthand function to reset the message label back to normal
        """
        self.parent.itemconfig(
            self.add_subject_label,
            fill="#000000",
            text="Add a new subject to the list:",
        )


class EditorSubjectList:
    def __init__(self, parent, callback, subject_list):
        """
        Initializes the UI component for selecting a subject to configure

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            callback (function): Callback for initializing the section editor UI. EditorPage.configure_subject() will init an instance of EditorSectionList to configure the sections of the selected subject.
            subject_list (list): List of existing subjects for first population
        """
        self.callback = callback

        self.x = 0
        self.y = 0

        self.choose_subject_label = parent.create_text(
            self.x + 41,
            self.y + 335,
            anchor="nw",
            text="Choose subject to configure:",
            fill="#000000",
            font=HEADING[1],
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
        self.subject_list.place(x=self.x + 40, y=self.y + 385, width=440, height=285)

        # when an item is selected from the ListBox, call the function
        self.subject_list.bind("<<ListboxSelect>>", self.handle_selection)

        # populate list upon init in case there are already subjects
        self.update_list(subject_list)
        # subject_list isn't stored because now the UI becomes the source of truth to the user until changes are registered.

    def update_list(self, subjects):
        """
        Called upon unit to populate the list as well as by the callback function when a new subject is added

        Args:
            subjects (list): List of Subject objects to be populated into the list
        """
        self.subject_list.delete(0, END)  # existing list cleared

        for subject in subjects:
            display_name = f"{subject.name} {'HL' if subject.level == 1 else 'SL'}"
            self.subject_list.insert(END, display_name)

    def handle_selection(self, event):
        """
        Calls the callback to draw the section configuration component each time a new subject is selected

        Args:
            event (tkinter event): Passed into function by bind(); unused
        """
        selected_index = self.subject_list.curselection()
        self.callback(selected_index)
