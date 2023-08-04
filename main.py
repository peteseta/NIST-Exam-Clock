import tkinter as tk
from collections import defaultdict
from datetime import timedelta

import arrow
import ttkbootstrap as ttk

from editor import EditorNewSubject, EditorSubjectList, EditorSectionList
from timer import Timer


# https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
# https://ttkbootstrap.readthedocs.io/en/latest/themes/themecreator/


class Subject:
    """
    Represents an IB subject which may contain multiple papers.
    """

    def __init__(self, name, level) -> None:
        self.name = name
        self.level = level  # 0 for SL, 1 for HL
        self.sections = []

    def add_exam(self, exam):
        self.sections.append(exam)


class Section:
    """
    Represents a single section (paper) of a subject, e.g. Paper 1 of a subject.
    """

    id_counter = 0

    def __init__(self, name, hours, minutes) -> None:
        """
        Initializes a new section.

        Args:
            name (str): Section name.
            hours (int): Hour component of the duration of the section.
            minutes (int): Minute component of the duration of the section.
        """
        self.name = name
        self.hours = hours
        self.minutes = minutes

        self.section_in_progress = False
        self.section_run = False

        self.id = Section.id_counter
        Section.id_counter += 1


class App(tk.Tk):
    def __init__(self) -> None:
        """
        Initializes the main app UI (showing the clock and timer page by default)
        Initializes base data structures
        """

        # TODO: remove debug
        self.subjects = [
            Subject("2 min then 1 min", 1),
            Subject("1 min x3", 1),
        ]
        self.active_subjects = []

        # TODO: remove debug
        self.subjects[0].sections.append(Section("Two Min Section", 0, 2))
        self.subjects[0].sections.append(Section("One Min Section", 0, 1))
        self.subjects[1].sections.append(Section("Test Section1", 0, 1))
        self.subjects[1].sections.append(Section("Test Section2", 0, 1))
        self.subjects[1].sections.append(Section("Test Section3", 0, 1))

        self.root = ttk.Window(themename="robin")
        self.root.title("NIST Exam Clock")
        self.root.geometry("1920x1080")

        container = ttk.Frame(self.root, height=900, width=1600)
        container.pack(side="top", fill="both", expand=True)

        self.timer_page = TimerPage(container, self)
        self.timer_page.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        self.header = ClockHeader(container, self)
        self.header.grid(row=0, column=0, sticky="nsew")

    def create_new_window(self, frame_class, width=1520, height=760):
        """
        Handles creating a new popup window, e.g. for the editor

        Args:
            frame_class (EditorPage): Object that defines the frame to be shown.
            width (int, optional): Width of popup. Defaults to 1520.
            height (int, optional): height of popup. Defaults to 760.
        """
        popup = tk.Toplevel(self.root)
        popup.geometry(f"{width}x{height}")
        frame_class(popup, self)


# permanent header for clock regardless of main window state
class ClockHeader(ttk.Frame):
    def __init__(self, parent, controller):
        """
        Initializes the UI for the header of the exam clock
        Shows the time and buttons to start/stop/edit exams

        Args:
            parent (ttk.Frame): Parent tkinter container, for the UI elements
            controller (App): Master instance of the app class to call create_new_window
        """
        self.controller = controller
        ttk.Frame.__init__(self, parent)

        self.clock_canvas = ttk.Canvas(self, height=80, width=1920)
        self.clock_canvas.pack(expand=True, fill="both")
        self.clock_canvas.configure(background="#EEEEEE")

        self.clock_text = self.clock_canvas.create_text(
            20.0,
            40.0,
            anchor="w",
            text="00:00:00",
            fill="#121212",
            font=("SF Pro Display Bold", 50),
        )
        self.update_clock()

        self.start_button = ttk.Button(
            self,
            text="Start All Exams",
            command=lambda: self.controller.timer_page.start_timers(),
            bootstyle="secondary",
        )
        self.start_button.place(x=1670, y=20, width=120, height=35)

        self.advance_button = ttk.Button(
            self,
            text="Start Next Section(s)",
            command=lambda: self.controller.timer_page.advance_timers(),
            bootstyle="secondary",
            state="disabled",
        )
        self.advance_button.place(x=1510, y=20, width=150, height=35)

        self.show_editor_button = ttk.Button(
            self,
            text="Edit Exams",
            command=lambda: self.controller.create_new_window(EditorPage),
            bootstyle="secondary",
        )
        self.show_editor_button.place(x=1800, y=20, width=100, height=35)

    def update_clock(self):
        """
        Updates the clock time. Continuously called to update each second.
        """
        time = arrow.now().format("HH:mm:ss")
        self.clock_canvas.itemconfig(self.clock_text, text=time)
        self.after(1000, self.update_clock)


class TimerPage(ttk.Frame):
    def __init__(self, parent, controller):
        """
        Initializes the UI for the timer page, which shows the current exam timers

        Args:
            parent (ttk.Frame): Parent tkinter container, for the UI elements
            controller (App): Master instance of the app to access subject/section data
        """
        self.controller = controller
        ttk.Frame.__init__(self, parent, padding=20)

        self.timers = []

        self.group_timers()
        self.draw_timers()

    def group_timers(self):
        """
        Groups each subject's first section (that hasn't been run) by duration
        Creates a timer for each duration
        """
        sections_by_duration = defaultdict(list)

        for subject in self.controller.subjects:
            for section in subject.sections:
                if not section.section_run:
                    section.section_in_progress = True
                    duration = timedelta(hours=section.hours, minutes=section.minutes)
                    sections_by_duration[duration].append(subject)
                    self.controller.active_subjects.append(
                        subject
                    )  # add subject to active_subjects
                    break

        # remove active subjects from subjects
        for subject in self.controller.active_subjects:
            if subject in self.controller.subjects:
                self.controller.subjects.remove(subject)

        # add a timer for each duration
        for duration in sorted(sections_by_duration.keys()):
            # pass the subjects with the same duration
            timer = Timer(
                self, self.finish, sections_by_duration[duration], duration, 0
            )
            self.timers.append(timer)

    def draw_timers(self):
        """
        Draws the timers on the page
        """
        for index, timer in enumerate(self.timers):
            timer.frame.grid(row=0, column=index, sticky="s")
            timer.frame.rowconfigure(2, weight=1)

    def start_timers(self):
        """
        Starts all the inactive timers on the page
        Disables the button to advance to the next section
        """
        for timer in self.timers:
            if not timer.is_running:
                timer.start_timer()

        self.controller.header.advance_button.configure(state="disabled")

    def finish(self, subjects):
        """
        Called by the Timer objects whenever a timer is finished.
        Marks the sections as run and adds the subjects back to the subjects list
        so that it is eligible for the next grouping run.
        Enables the button to advance to the next section
        """
        # mark sections as run
        for subject in subjects:
            for section in subject.sections:
                if section.section_in_progress:
                    section.section_in_progress = False
                    section.section_run = True
                    self.controller.subjects.append(
                        subject
                    )  # add subject back to subjects
                    if subject in self.controller.active_subjects:
                        self.controller.active_subjects.remove(
                            subject
                        )  # remove subject from active_subjects

        # activate button to start the next section
        self.controller.header.advance_button.configure(state="normal")

    def advance_timers(self):
        """
        Destroys the finished timers.
        Regroups the remaining sections by duration and creates new timers.
        """

        # destroy finished timers
        for timer in self.timers:
            if timer.finished:
                timer.frame.destroy()
                self.timers.remove(timer)

        # regroup and start new timers
        self.group_timers()
        self.draw_timers()


class EditorPage(ttk.Frame):
    def __init__(self, parent, controller):
        """
        Initializes the UI for the editor page
        Allows the user to add and configure subjects and sections

        Args:
            parent (tk.Toplevel): Parent tkinter Toplevel window, for the UI elements
            controller (App): Master instance of the app to access subject/section data
        """
        self.controller = controller
        ttk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)

        self.editor_canvas = tk.Canvas(self)
        self.editor_canvas.pack(fill="both", expand=True)

        # draw subject addition/selection elements
        self.new_subject = EditorNewSubject(self.editor_canvas, self.create_subject)
        self.listbox = EditorSubjectList(
            self.editor_canvas,
            self.configure_subject,
            self.controller.subjects,
            self.controller.active_subjects,
        )

    def create_subject(self, subject_name, level):
        """
        Called by editor.EditorNewSubject to register a new subject
        Stores the subject details in the controller's subject list
        Redraws the list of subjects

        Args:
            subject_name (str): Name of the subject.
            level (int): Level of the subject (0 for SL, 1 for HL).
        """

        # check if subject already exists
        if any(
            (subject.name == subject_name and subject.level == level)
            for subject in self.controller.subjects + self.controller.active_subjects
        ):
            self.new_subject.status_msg("Subject already exists!")
            return

        subject = Subject(subject_name, level)
        self.controller.subjects.append(subject)

        # redraw list of subjects
        self.listbox.update_list()

    def configure_subject(self, subject_list, subject_index):
        """
        Called by editor.EditorSubjectList each time a subject is selected
        Draws the UI (EditorSectionList component) to configure sections

        Args:
            subject_list (list): Either self.controller.subjects or self.controller.active_subjects
            subject_index (tuple): Tuple with index (0, 1, 2...) of the subject in the subject list
        """
        self.subject_list = subject_list
        self.subject_index = subject_index

        # destroy any existing UI (if there was a previously selected subject)
        # old EditorSectionList would become ready for garbage collection (safe)
        if hasattr(self, "section_config"):
            self.section_config.destroy()

        # draws the UI (EditorSectionList component) to configure sections
        self.section_config = EditorSectionList(
            self.editor_canvas,
            self.subject_list[subject_index].sections,
            self.register_sections,
        )

    # called by EditorSectionList to register a section
    def register_sections(self, name_list, hours_list, minutes_list):
        """
        Called by the save button in editor.EditorSectionList to modify a subject's sections
        Unpacks the section details and stores them in the subject's sections list

        Args:
            name_list (list): Parallel list of names of the sections
            hours_list (list): List of hour components of the sections
            minutes_list (list): List of minute components of the sections
        """
        # clear existing sections
        self.subject_list[self.subject_index].sections = []

        # populate sections list with Section objects
        for name, hours, minutes in zip(name_list, hours_list, minutes_list):
            section = Section(name, hours, minutes)
            self.subject_list[self.subject_index].sections.append(section)

        # regroup and redraw timers
        self.controller.timer_page.group_timers()
        self.controller.timer_page.draw_timers()


# create an instance of the app
app = App()
app.root.mainloop()
