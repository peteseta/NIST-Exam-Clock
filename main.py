import tkinter as tk
import tkinter.simpledialog as simpledialog
from collections import defaultdict
from datetime import timedelta

import arrow
import ttkbootstrap as ttk

from editor import EditorNewSubject, EditorSubjectList, EditorSectionList
from timer import Timer


class Subject:
    """
    Represents an IB subject which may contain multiple papers.
    """

    id_counter: int = 0

    def __init__(self, name: str, level: int) -> None:
        self.name: str = name
        self.level: int = level  # 0 for SL, 1 for HL
        self.sections: list[Section] = []

        self.id: int = Subject.id_counter
        Subject.id_counter += 1

        self.timestamp: arrow.Arrow = arrow.now()


class Section:
    """
    Represents a single section (paper) of a subject, e.g. Paper 1 of a subject.
    """

    id_counter: int = 0

    def __init__(self, name: str, hours: int, minutes: int) -> None:
        """
        Initializes a new section.
        """
        self.name: str = name
        self.hours: int = hours
        self.minutes: int = minutes

        self.section_in_progress: bool = False
        self.section_run: bool = False

        self.id: int = Section.id_counter
        Section.id_counter += 1


class App(tk.Tk):
    def __init__(self) -> None:
        """
        Initializes the main app UI (showing the clock and timer page by default)
        Initializes base data structures
        """

        # FIXME: resizing breaks the border (clockheader)

        self.subjects: list[Subject] = []
        self.active_subjects: list[Subject] = []

        # debug
        # self.subjects.append(Subject("English", 0))
        # self.subjects[0].sections.append(Section("Paper 1", 0, 1))

        self.root = ttk.Window(themename="robin")
        self.root.title("NIST Exam Clock")
        self.root.geometry("1920x1080")
        self.root.minsize(560, 1)

        container = ttk.Frame(self.root, height=900, width=1600)
        container.pack(side="top", fill="both", expand=True)
        
        self.header = ClockHeader(container, self)
        self.header.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=0)  # make the header row not resizable
        container.grid_columnconfigure(0, weight=1)  # make the column resizable

        self.timer_page = TimerPage(container, self)
        self.timer_page.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        container.grid_rowconfigure(1, weight=1)

    def create_new_window(
        self, frame_class, width: int = 1520, height: int = 760
    ) -> None:
        """
        Handles creating a new popup window, e.g. for the editor

        Args:
            frame_class (class): Object that defines the frame to be shown.
            width (int, optional): Width of popup. Defaults to 1520.
            height (int, optional): height of popup. Defaults to 760.
        """
        popup = tk.Toplevel(self.root)
        popup.geometry(f"{width}x{height}")
        frame_class(popup, self)

    def get_subject(self, requested_id: int) -> Subject | None:
        """
        Returns the subject that has the given ID.
        """

        for subject in self.subjects + self.active_subjects:
            if subject.id == requested_id:
                return subject

        return None


# TODO: add custom start (choose subjects to start)
class ClockHeader(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        """
        Initializes the UI for the header of the exam clock
        Shows the time and buttons to start/stop/edit exams
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

        # initialize style
        s = ttk.Style()
        s.configure('grey.TFrame', background='#EEEEEE')

        # subframe for buttons
        self.button_frame = ttk.Frame(self, style='grey.TFrame')
        self.button_frame.place(relx=0.99, rely=0.25, width=500, height=35, anchor='ne')

        self.buttons = [
            ttk.Button(
                self.button_frame,
                text="Edit",
                command=lambda: self.controller.create_new_window(EditorPage),
                bootstyle="secondary",
                state="normal",
            ),
            ttk.Button(
                self.button_frame,
                text="Start",
                command=lambda: self.on_start_button_click(),
                bootstyle="secondary",
                state="normal",
            ),
            ttk.Button(
                self.button_frame,
                text="Pause",
                command=lambda: self.on_pause_button_click(),
                bootstyle="secondary",
                state="disabled",
            ),
            ttk.Button(
                self.button_frame,
                text="Resume",
                command=lambda: self.on_resume_button_click(),
                bootstyle="secondary",
                state="disabled",
            ),
            ttk.Button(
                self.button_frame,
                text="Stop",
                command=lambda: self.on_stop_button_click(),
                bootstyle="secondary",
                state="disabled",
            ),
            ttk.Button(
                self.button_frame,
                text="Next",
                command=lambda: self.controller.timer_page.advance_timers(),
                bootstyle="secondary",
                state="disabled",
            ),
        ]

        self.update_buttons()

    def update_buttons(self):
        # clear all buttons
        for button in self.buttons:
            button.pack_forget()
            print(f"forgot {button['text']}")

        # repack buttons based on their state
        for button in self.buttons:
            if not button.state():
                button.pack(side="right")

    def on_start_button_click(self):
        self.buttons[1]['state'] = 'disabled'  # Disable the "Start" button
        self.buttons[2]['state'] = 'normal'  # Enable the "Pause" button
        self.buttons[4]['state'] = 'normal'  # Enable the "Stop" button
        self.update_buttons()
        self.controller.timer_page.start_timers()

    def on_pause_button_click(self):
        self.buttons[2]['state'] = 'disabled'  # Disable the "Pause" button
        self.buttons[3]['state'] = 'normal'  # Enable the "Resume" button
        self.update_buttons()
        self.controller.timer_page.pause_timers()

    def on_resume_button_click(self):
        self.buttons[3]['state'] = 'disabled'  # Disable the "Resume" button
        self.buttons[2]['state'] = 'normal'  # Enable the "Pause" button
        self.update_buttons()
        self.controller.timer_page.resume_timers()

    def on_stop_button_click(self):
        self.buttons[2]['state'] = 'disabled'  # Disable the "Pause" button
        self.buttons[3]['state'] = 'disabled'  # Disable the "Resume" button
        self.buttons[4]['state'] = 'disabled'  # Disable the "Stop" button
        self.buttons[1]['state'] = 'normal'  # Enable the "Start" button
        self.update_buttons()
        self.controller.timer_page.stop_timers()

    def update_clock(self) -> None:
        """
        Updates the clock time. Continuously called to update each second.
        """
        time: str = arrow.now().format("HH:mm:ss")
        self.clock_canvas.itemconfig(self.clock_text, text=time)
        self.after(1000, self.update_clock)


class TimerPage(ttk.Frame):
    def __init__(self, parent: ttk.Frame, controller: App):
        """
        Initializes the UI for the timer page, which shows the current exam timers
        """

        # TODO: separation between timers (white and grey)

        ttk.Frame.__init__(self, parent, padding=20)

        self.controller: App = controller
        self.grid_rowconfigure(0, weight=1)

        self.timers: list[Timer] = []

        self.group_timers()
        self.draw_timers()

    def group_timers(self):
        """
        Groups each subject's first section (that hasn't been run) by duration
        Creates a timer for each duration
        """
        sections_by_duration: defaultdict[timedelta] = defaultdict(list)

        # group the first not yet run section of each subject by duration
        for subject in self.controller.subjects:
            for section in subject.sections:
                if not section.section_run:
                    section.section_in_progress = True
                    duration: timedelta = timedelta(
                        hours=section.hours, minutes=section.minutes
                    )
                    sections_by_duration[duration].append(subject)
                    break

        # add a timer for each duration
        for duration in sorted(sections_by_duration.keys()):
            # check if an unstarted timer with this duration already exists
            existing_timer: Timer | None = next(
                (
                    t
                    for t in self.timers
                    if t.duration == duration and t.is_running is False
                ),
                None,
            )
            if existing_timer:
                # if it does, add the subjects to this timer
                for subject in sections_by_duration[duration]:
                    # exclude subjects already in the timer
                    if not self.get_timer_by_id(subject.id):
                        existing_timer.add_subject(subject)
            else:
                # check if subjects are not already in with another timer
                subjects_for_new_timer = [
                    subject
                    for subject in sections_by_duration[duration]
                    if not self.get_timer_by_id(subject.id)
                ]
                if subjects_for_new_timer:
                    timer = Timer(self, self.finish, subjects_for_new_timer, duration)
                    self.timers.append(timer)

    def draw_timers(self):
        """
        Populates the timerpage with Timer objects
        """
        for index, timer in enumerate(self.timers):
            timer.frame.grid(row=0, column=index, sticky="nsew")

    def start_timers(self):
        """
        Starts all the inactive timers on the page
        Marks each subject as active
        Disables the button to advance to the next section
        """
        for timer in self.timers:
            if not timer.is_running:
                timer.start_timer()
                
                # mark subjects as active
                for subject in timer.subjects:
                    self.controller.active_subjects.append(subject)
                    if subject in self.controller.subjects:
                        self.controller.subjects.remove(subject)
    
    def resume_timers(self):
        for timer in self.timers:
            timer.resume_timer()
            
    def pause_timers(self):
        for timer in self.timers:
            timer.pause_timer()

    def stop_timers(self):
        for timer in self.timers:
            if timer.is_running:
                timer.stop_timer()
                # mark subjects as inactive
                for subject in timer.subjects:
                    self.controller.subjects.append(subject)
                    if subject in self.controller.active_subjects:
                        self.controller.active_subjects.remove(subject)

    def finish(self, subjects: list[Subject]):
        """
        Called by the Timer objects whenever a timer is finished.
        Marks the sections as run and adds the subjects back to the subjects list
        so that it is eligible for the next grouping run.
        Enables the button to advance to the next section
        """

        for subject in subjects:
            for section in subject.sections:
                # mark sections as run
                if section.section_in_progress:
                    subject.subject_queued = False
                    section.section_in_progress = False
                    section.section_run = True
                    break

            # mark subject as inactive
            self.controller.subjects.append(subject)
            if subject in self.controller.active_subjects:
                self.controller.active_subjects.remove(subject)

        # activate button to start the next section
        # self.controller.header.advance_button.configure(state="normal")
        self.controller.header.advance_button.pack()

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

    def get_timer_by_id(self, subject_id: int) -> Timer | None:
        """
        Returns the timer object that contains the subject with the given ID
        """

        for timer in self.timers:
            for subject in timer.subjects:
                if subject.id == subject_id:
                    return timer
        return None

    def update_subject_name(self, subject_id: int, name):
        """
        Updates the name of the subject with the given ID
        """
        timer = self.get_timer_by_id(subject_id)
        if timer:
            for subject_label in timer.subject_list.labels:
                if subject_label.id == subject_id:
                    subject_label.update_details(name)
                    break
        else:
            return Exception("Subject not found")

    def remove_subject(self, subject_id: int):
        """
        Removes the subject with the given ID from the timer
        If the timer only contains that subject, destroys it,
        otherwise just removes the subject
        """
        timer = self.get_timer_by_id(subject_id)
        if timer:
            if len(timer.subject_list.labels) == 1:
                timer.frame.destroy()
                self.timers.remove(timer)
            else:
                for subject_label in timer.subject_list.labels:
                    if subject_label.id == subject_id:
                        subject_label.frame.destroy()
                        break
        else:
            return Exception("Subject not found")

    def update_subject_level(self, subject_id: int, level: int):
        """
        Updates the level of the subject with the given ID
        """
        timer = self.get_timer_by_id(subject_id)
        if timer:
            for subject_label in timer.subject_list.labels:
                if subject_label.id == subject_id:
                    subject_label.update_details(level=level)
                    break
        else:
            return Exception("Subject not found")

    def update_subject_duration(self, subject_id: int, duration: timedelta):
        # TODO: use unique id to allow changing details like subject duration after starting timer
        pass


class EditorPage(ttk.Frame):
    def __init__(self, parent: tk.Toplevel, controller: App):
        """
        Initializes the UI for the editor page
        Allows the user to add and configure subjects and sections
        """
        ttk.Frame.__init__(self, parent)

        self.controller: App = controller
        self.pack(fill="both", expand=True)

        self.active_subject_id = -1

        self.editor_canvas = tk.Canvas(self)
        self.editor_canvas.pack(fill="both", expand=True)

        # draw subject addition/selection elements
        self.new_subject = EditorNewSubject(self.editor_canvas, self.create_subject)

        # TODO: why am i passing all of this in?
        self.listbox = EditorSubjectList(
            self.editor_canvas,
            self.configure_subject,
            self.rename_subject,
            self.remove_subject,
            self.toggle_subject_level,
            self.controller.subjects,
            self.controller.active_subjects,
        )

        # bind to window closing
        parent.protocol("WM_DELETE_WINDOW", self.close)

    def create_subject(self, subject_name: str, level: int):
        """
        Called by editor.EditorNewSubject to register a new subject
        Stores the subject details in the controller's subject list
        Redraws the list of subjects
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

    def configure_subject(self, subject_id: int):
        """
        Called by editor.EditorSubjectList each time a subject is selected
        Draws the UI (EditorSectionList component) to configure sections
        """

        # destroy any existing UI (if there was a previously selected subject)
        # old EditorSectionList would become ready for garbage collection (safe)
        if hasattr(self, "section_config"):
            self.section_config.destroy()

        # subject object that has the ID, whether it's active or not
        self.active_subject_id = subject_id
        subject: Subject = self.controller.get_subject(self.active_subject_id)

        # draws the UI (EditorSectionList component) to configure sections
        self.section_config: EditorSectionList = EditorSectionList(
            self.editor_canvas,
            subject.sections,
            self.register_sections,
        )

    def remove_subject(self, subject_id: int):
        """
        Called by editor.EditorSubjectList to remove the given subject
        """
        subject: Subject = self.controller.get_subject(subject_id)

        # remove subject object
        if subject in self.controller.subjects:
            self.controller.subjects.remove(subject)
        elif subject in self.controller.active_subjects:
            self.controller.active_subjects.remove(subject)

        # remove from listbox and destroy configuration ui
        self.listbox.update_list()
        self.section_config.destroy()

        # remove from TimerPage
        self.controller.timer_page.remove_subject(subject_id)

    def rename_subject(self, subject_id: int):
        """
        Called by editor.EditorSubjectList to rename the given subject
        Creates a dialog to get the new name
        """
        new_name = simpledialog.askstring("Rename subject", "New name:")

        # only update the name if Ok was pressed on the simpledialog, not cancel
        if new_name is not None:
            # update name in subject object
            subject: Subject = self.controller.get_subject(subject_id)
            subject.name = new_name

            # update name in listbox
            self.listbox.update_list()

            # update name in TimerPage
            self.controller.timer_page.update_subject_name(subject_id, new_name)

    def toggle_subject_level(self, subject_id: int):
        """
        Called by editor.EditorSubjectList to toggle the level of a subject

        Args:
            subject_id (int): id of subject to toggle the level of
        """
        # update level in subject object
        subject: Subject = self.controller.get_subject(subject_id)
        subject.level = 1 - subject.level  # toggle

        # update level in listbox
        self.listbox.update_list()

        # update level in TimerPage
        self.controller.timer_page.update_subject_level(subject_id, subject.level)

    def register_sections(
        self, name_list: list[str], hours_list: list[int], minutes_list: list[int]
    ):
        """
        Called by the save button in EditorSectionList to modify a subject's sections
        Unpacks the section details and stores them in the subject's sections list
        """

        # TODO: check for edited section name and update in timer page

        # clear existing sections
        subject: Subject = self.controller.get_subject(self.active_subject_id)
        subject.sections = []

        # populate sections list with Section objects
        for name, hours, minutes in zip(name_list, hours_list, minutes_list):
            section = Section(name, hours, minutes)
            subject.sections.append(section)

        # update the listbox and the dictionary
        self.listbox.update_list()

    def close(self):
        """
        When the editor window is closed, redraw and regroup all timers
        """
        self.controller.timer_page.group_timers()
        self.controller.timer_page.draw_timers()

        # destroy the editor window
        self.master.destroy()


# create an instance of the app
app = App()
app.root.mainloop()
