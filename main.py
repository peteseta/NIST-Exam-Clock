import arrow

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from style import HEADING
from editor import EditorNewSubject, EditorSubjectList, EditorSectionList
from timer import *

# https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
# https://ttkbootstrap.readthedocs.io/en/latest/themes/themecreator/

class Subject():
    """
    Represents an IB subject which may contain multiple papers.
    """
    def __init__(self, name, level) -> None:
        self.name = name
        self.level = level # 0 for SL, 1 for HL
        self.sections = []
    
    def add_exam(self, exam):
        self.sections.append(exam)

class Section():
    """
    Represents a single section (paper) of a subject, e.g. Paper 1 of a subject.
    """
    def __init__(self, name, reading_time, hours, minutes) -> None:
        """
        Initilizes a new section.
        
        Args:
            name (str): Section name.
            reading_time (int): Reading time in minutes.
            hours (int): Hour component of the duration of the section.
            minutes (int): Minute component of the duration of the section.
        """
        self.name = name
        self.reading_time = reading_time
        self.hours = hours
        self.minutes = minutes

class App(tk.Tk):
    def __init__(self) -> None:
        """
        Initializes the main application window (showing the clock and timer page by defualt) and base data structures
        """
        
        # TODO: remove debug
        # self.subjects = []
        self.subjects = [Subject("Test", 1)]
        self.subjects[0].sections.append(Section("Test Section", 5, 1, 15))
        
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
            frame_class (ttk.Frame): Object that defines the frame to be shown.
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
        Initializes the UI for the header of the exam clock, which shows the time and buttons to start/stop/edit exams

        Args:
            parent (ttk.Frame): Parent tkinter container, for the UI elements
            controller (App): Master instance of the application class, to be able to call create_new_window
        """
        self.controller = controller
        ttk.Frame.__init__(self, parent)

        self.clock_canvas = ttk.Canvas(
            self,
            height=80,
            width=1920
        )
        self.clock_canvas.pack(expand=True, fill="both")
        self.clock_canvas.configure(background="#EEEEEE")

        self.clock_text = self.clock_canvas.create_text(
            20.0,
            40.0,
            anchor="w",
            text="00:00:00",
            fill="#121212",
            font=("SF Pro Display Bold", 50)
        )
        self.update_clock()

        self.show_editor_button = ttk.Button(
            self,
            text="Edit Exams",
            command=lambda: self.controller.create_new_window(EditorPage),
            bootstyle="secondary"
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
            controller (App): Master instance of the application class, to be able to access subject/section data
        """
        self.controller = controller
        ttk.Frame.__init__(self, parent, padding=20)
        
        test_text = ttk.Label(self, text="Test", foreground="#121212", font=HEADING[1])
        test_text.grid(row=0, column=0, sticky="nsew")
        
class EditorPage(ttk.Frame):
    def __init__(self, parent, controller):
        """
        Initializes the UI for the editor page, which allows the user to add and configure subjects and sections

        Args:
            parent (tk.Toplevel): Parent tkinter Toplevel window, for the UI elements
            controller (App): Master instance of the application class, to be able to access subject/section data
        """
        self.controller = controller
        ttk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        
        self.editor_canvas = tk.Canvas(self)
        self.editor_canvas.pack(fill="both", expand=True)
        
        # draw subject addition/selection elements
        self.new_subject = EditorNewSubject(self.editor_canvas, self.create_subject)
        self.subject_list = EditorSubjectList(self.editor_canvas, self.configure_subject, self.controller.subjects)
    
    def create_subject(self, subject_name, level):
        """
        Called by editor.EditorNewSubject to register a new subject
        Stores the subject details in the controller's subject list, and redraws the list of subjects

        Args:
            subject_name (str): Name of the subject.
            level (int): Level of the subject (0 for SL, 1 for HL).
        """
        
        # check if subject already exists
        if any((subject.name == subject_name and subject.level == level) for subject in self.controller.subjects):
            self.new_subject.status_msg("Subject already exists!")
            return
        
        subject = Subject(subject_name, level)
        self.controller.subjects.append(subject)
        
        # redraw list of subjects
        self.subject_list.update_list(self.controller.subjects)
        
    def configure_subject(self, subject_index):
        """
        Called by editor.EditorSubjectList each time a subject is selected
        Draws the UI (EditorSectionList component) to configure sections

        Args:
            subject_index (int): Index (0, 1, 2...) of the subject in the controller's subject list
        """
        self.subject_index = subject_index[0]
        print(self.subject_index)
        
        # destroy any existing UI (if there was a previously selected subject for config)
        # old EditorSectionList would become ready for garbage collection (safe)
        if hasattr(self, 'section_config'):
            self.section_config.destroy()
        
        # draws the UI (EditorSectionList component) to configure sections
        self.section_config = EditorSectionList(self.editor_canvas, self.controller.subjects[subject_index[0]].sections, self.register_sections)
    
    # called by EditorSectionList to register a section
    def register_sections(self, name_list, reading_time_list, hours_list, minutes_list):
        """
        Called by editor.EditorSectionList to modify a subject's sections
        Unpacks the parallel arrays of section details and stores them in the subject's sections list

        Args:
            name_list (list): Parallel list of names of the sections
            reading_time_list (list): Parallel list of reading times of the sections
            hours_list (list): Parallel list of hour component of the duration of the sections
            minutes_list (list): Parallel list of minute component of the duration of the sections
        """
        # clear existing sections
        self.controller.subjects[self.subject_index].sections = []
        
        # populate sections list with Section objects
        for name, reading_time, hours, minutes in zip(name_list, reading_time_list, hours_list, minutes_list):
            section = Section(name, reading_time, hours, minutes)
            self.controller.subjects[self.subject_index].sections.append(section)

# create an instance of the app
app = App()
app.root.mainloop()
