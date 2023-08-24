from tkinter import Canvas, Entry, Listbox, StringVar, IntVar
from tkinter.constants import SINGLE, END

import ttkbootstrap as ttk

from style import HEADING, round_rectangle


# list of sections, handles creating and removing sections, numbering, etc.
class EditorSectionList:
    def __init__(self, parent, existing_sections, callback) -> None:
        """
        Init a new instance of the UI component for editing a subject's sections

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            existing_sections (list): List of Section's the selected subject already has
            callback (function): EditorPage.register_sections()
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
        Adds a new UI element for configuring an additional section
        Moves the modification buttons below the last section element.
        """
        self.section_count += 1
        self.modify.place()  # move modification buttons

        self.components.append(EditorSection(self.parent, self, self.section_count))

        self.validate_entries()

    def remove_section(self):
        """
        Removes the last UI element for configuring a section
        Moves the modification buttons below the last section element.
        """
        self.section_count -= 1
        self.modify.place()  # move modification buttons

        self.components[-1].canvas.destroy()
        self.components.pop(-1)

        self.validate_entries()

    def validate_entries(self, *args):
        """
        Checks if all the section details are properly filled out
        Each section must have a name and at least 1 minute duration
        If all entries are valid, the Save button in EditorSectionModify is enabled.
        If there are already 4 sections, the Add button is disabled.

        Accepts *args due to trace_add() requiring it for the callback.
        """

        # no more than 4 sections
        self.modify.add_button.config(
            state="disabled" if self.section_count >= 4 else "active"
        )

        # no less than 0 sections
        self.modify.remove_button.config(
            state="disabled" if self.section_count == 0 else "active"
        )

        # check if any entry is empty or has 0 hours and minutes
        if any(
            component.name_var.get() == ""
            or ((component.hours_var.get() + component.minutes_var.get()) == 0)
            for component in self.components
        ):
            self.modify.save_button.config(state="disabled")
        else:
            self.modify.save_button.config(state="active")  # enable save button

    def apply(self):
        """
        Retrieves the data from all the entries,
        passes them to the callback as parallel arrays
        """
        name_list = [component.name_var.get() for component in self.components]
        hours_list = [component.hours_var.get() for component in self.components]
        minutes_list = [component.minutes_var.get() for component in self.components]

        self.callback(name_list, hours_list, minutes_list)

    def destroy(self):
        """
        When a new subject is selected, destroy() is called to clean up the old subject
        before a new instance of EditorSectionList is created to configure the new
        subject's sections
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
        hours=0,
        minutes=0,
    ) -> None:
        """
        Initialize a UI component representing one section of a subject

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            controller (EditorSectionList object): Parent object "overseeing" the list
            section_number (int): Index of current section, displayed as the section no.
            name (str, optional): Name of section (if existing). Defaults to "".
            hours (int, optional): Hour duration of section (if existing).
            minutes (int, optional): Minute duration of section (if existing).
        """
        self.controller = controller
        self.canvas = Canvas(parent, width=600, height=120)
        self.canvas.place(x=522.0, y=(96.0 + (138 * (section_number - 1))))

        # values will be populated if section already exists
        self.name_var = StringVar(self.canvas, value=name)
        self.hours_var = IntVar(self.canvas, value=hours)
        self.minutes_var = IntVar(self.canvas, value=minutes)

        # each time an entry is modified run the validation
        self.name_var.trace_add("write", self.controller.validate_entries)
        self.hours_var.trace_add("write", self.controller.validate_entries)
        self.minutes_var.trace_add("write", self.controller.validate_entries)

        self.section_bg = round_rectangle(
            self.canvas, 0, 0, 600, 120, radius=12, fill="#F5F5F5", outline=""
        )
        self.section_number = self.canvas.create_text(
            20,
            25,
            anchor="nw",
            text=str(section_number),
            fill="#121212",
            font=HEADING[2],
        )
        self.separator_line = round_rectangle(
            self.canvas, 45, 30, 50, 100, radius=5, fill="#EEEEEE", outline=""
        )
        self.section_name_label = self.canvas.create_text(
            70, 25, anchor="nw", text="Section Name:", fill="#121212", font=HEADING[3]
        )
        self.section_name_entry = ttk.Entry(
            self.canvas, bootstyle="dark", textvariable=self.name_var
        )
        self.section_name_entry.place(x=250, y=25, width=252, height=32)
        self.duration_label = self.canvas.create_text(
            70, 70, anchor="nw", text="Duration:", fill="#121212", font=HEADING[3]
        )
        self.hour_entry = ttk.Entry(
            self.canvas, bootstyle="dark", textvariable=self.hours_var
        )
        self.hour_entry.place(x=200, y=70, width=30, height=35)
        self.canvas.create_text(
            250, 70, anchor="nw", text="h", fill="#121212", font=HEADING[3]
        )
        self.minute_entry = ttk.Entry(
            self.canvas, bootstyle="dark", textvariable=self.minutes_var
        )
        self.minute_entry.place(x=300, y=70, width=37, height=35)
        self.canvas.create_text(
            350, 70, anchor="nw", text="m", fill="#121212", font=HEADING[3]
        )


# add/remove section modification buttons
class EditorSectionModify:
    def __init__(self, parent, controller):
        """
        UI component for the Add, Remove, Save buttons at the bottom of the section list

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            controller (EditorSectionList): Parent object "overseeing" the whole list
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
        )
        self.save_button = ttk.Button(
            parent,
            text="Save",
            command=lambda: self.controller.apply(),
            bootstyle="success",
        )

        self.place()

    def place(self):
        """
        Moves the modification button to the appropriate place,
        below the last section UI element
        """

        # place at the very top if there are no sections yet
        if self.controller.section_count == 0:
            self.x = 522
            self.y = 100

        # otherwise place at the end of the last section
        else:
            self.x = 522
            self.y = 235 + (138 * (self.controller.section_count - 1))

        self.add_button.place(x=self.x, y=self.y, width=100, height=47)
        self.remove_button.place(x=self.x + 110, y=self.y, width=100, height=47)
        self.save_button.place(x=self.x + 220, y=self.y, width=100, height=47)


class EditorNewSubject:
    def __init__(self, parent, callback):
        """
        Initializes the UI component for adding a new subject
        (naming and selecting its level)

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            callback (function): EditorPage.create_subject()
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
        Updates the level label to give visual feedback on the selection

        Args:
            level (int): 0 means SL, 1 means HL
        """
        self.level = level

        label_text = "Level: " + ("SL" if level == 0 else "HL")
        self.parent.itemconfig(self.level_label, text=label_text)

    def register_subject(self):
        """
        Called when "add subject" is clicked.
        Entries are validated before the callback is called.
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
    def __init__(
        self,
        parent,
        configure_callback,
        rename_callback,
        remove_callback,
        level_callback,
        subject_list,
        active_subject_list,
    ):
        """
        Initializes the UI component for selecting a subject to configure

        Args:
            parent (tkinter parent): A canvas housing all elements in EditorPage
            configure_callback (function): EditorPage.configure_subject()
            rename_callback (function): EditorPage.rename_subject()
            remove_callback (function): EditorPage.remove_subject()
            level_callback (function): EditorPage.toggle_subject_level()
            subject_list (list): List of subjects without active timers
            active_subject_list (list): List of subjects with active timers
        """
        self.configure_callback = configure_callback
        self.rename_callback = rename_callback
        self.remove_callback = remove_callback
        self.level_callback = level_callback

        self.choose_subject_label = parent.create_text(
            41,
            335,
            anchor="nw",
            text="Choose subject to configure:",
            fill="#000000",
            font=HEADING[1],
        )
        self.listbox = Listbox(
            parent,
            bd=0,
            bg="#F5F5F5",
            fg="#000716",
            font=HEADING[4],
            highlightthickness=0,
            selectmode=SINGLE,
        )
        self.listbox.place(x=40, y=385, width=440, height=285)

        # when an item is selected from the ListBox, call the function
        self.listbox.bind("<<ListboxSelect>>", self.handle_selection)

        # populate list on init
        self.subject_list = subject_list
        self.active_subject_list = active_subject_list
        self.update_list()

        self.remove_button = ttk.Button(
            parent,
            text="Remove Subject",
            command=self.remove_subject,
            state="disabled",
            bootstyle="danger",
        )
        self.remove_button.place(x=40, y=670)

        self.rename_button = ttk.Button(
            parent,
            text="Rename Subject",
            command=self.rename_subject,
            state="disabled",
            bootstyle="info",
        )
        self.rename_button.place(x=170, y=670)

        self.change_level_button = ttk.Button(
            parent,
            text="Change Level",
            command=self.toggle_level,
            state="disabled",
            bootstyle="warning",
        )
        self.change_level_button.place(x=300, y=670)

    def update_list(self):
        """
        Called upon init to populate the list
        Called by callback function when a new subject is added
        """

        self.listbox.delete(0, END)  # existing listbox cleared

        # Create dictionary mapping listbox indices to subject IDs
        all_subjects = sorted(
            self.subject_list + self.active_subject_list,
            key=lambda subject: subject.timestamp,
        )

        self.subject_ids = {}

        for index, subject in enumerate(all_subjects):
            self.subject_ids[index] = subject.id

            display_name = f"{subject.name} {'HL' if subject.level == 1 else 'SL'}"
            self.listbox.insert(END, display_name)

    def handle_selection(self, event):
        """
        Calls EditorPage.configure_subject() to draw the section configuration
        component each time a new subject is selected

        Args:
            event (tkinter event): Passed into function by bind(); unused
        """

        # enable remove and rename subject buttons
        self.remove_button["state"] = "normal"
        self.rename_button["state"] = "normal"
        self.change_level_button["state"] = "normal"

        selected_index = self.listbox.curselection()[0]
        selected_id = self.subject_ids[selected_index]
        self.configure_callback(selected_id)

    @property
    def selected_id(self):
        selected_index = self.listbox.curselection()[0]
        selected_id = self.subject_ids[selected_index]
        return selected_id

    def remove_subject(self):
        self.remove_callback(self.selected_id)

    def rename_subject(self):
        self.rename_callback(self.selected_id)

    def toggle_level(self):
        self.level_callback(self.selected_id)
