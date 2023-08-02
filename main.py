from datetime import datetime, timedelta
import arrow
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from style import HEADING
from editor import EditorNewSubject, EditorSubjectList, EditorSectionList

# https://www.digitalocean.com/community/tutorials/tkinter-working-with-classes
# https://ttkbootstrap.readthedocs.io/en/latest/themes/themecreator/

# represents an IB subject which may contain multiple papers.
class Subject():
    def __init__(self, name, level) -> None:
        self.name = name
        self.level = level # 0 for SL, 1 for HL
        self.sections = []
    
    def add_exam(self, exam):
        self.sections.append(exam)

# represents a single paper, e.g. Paper 1 of a subject.
class Section(Subject):
    def __init__(self, name, reading_time, hours, minutes) -> None:
        self.name = name
        self.reading_time = reading_time
        self.hours = hours
        self.minutes = minutes

class App(tk.Tk):
    def __init__(self) -> None:
        # init subject list
        self.subjects = [Subject("Test", 1)]
        
        # debug
        self.subjects[0].sections.append(Section("Test Section", 5, 1, 15))
        
        # init tkinter ui
        self.root = ttk.Window(themename="robin")
        self.root.title("NIST Exam Clock")
        self.root.geometry("1920x1080")

        # creating a frame and assigning it to container
        container = ttk.Frame(self.root, height=900, width=1600)
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # add TimerPage to container
        self.timer_page = TimerPage(container, self)
        self.timer_page.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # add header to container, keep on row 0 = up top
        header = ClockHeader(container, self)
        header.grid(row=0, column=0, sticky="nsew")

    # handles creating a new popup window, e.g. for the editor
    def create_new_window(self, frame_class, width=1520, height=760):
        new_window = tk.Toplevel(self.root)
        new_window.geometry(f"{width}x{height}")
        frame = frame_class(new_window, self)
        return new_window
    
    def list_subjects(self):
        for subject in self.subjects:
                print(f"Subject Name: {subject.name}")
                print(f"Level: {'SL' if subject.level == 0 else 'HL'}")
                print("Exams:")
                for exam in subject.exams:
                    print(f"  - {exam.name}")

# permanent header for clock regardless of main window state
class ClockHeader(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.configure(height=80)

        # bg canvas for clock
        self.clock_canvas = ttk.Canvas(
            self,
            height=80,
            width=1920
        )
        self.clock_canvas.pack()
        self.clock_canvas.configure(background="#EEEEEE")

        # clock text
        self.time = self.clock_canvas.create_text(
            20.0,
            40.0,
            anchor="w",
            text="00:00:00",
            fill="#121212",
            font=("SF Pro Display Bold", 50)
        )
        self.update_clock()

        # button to edit exams
        self.show_editor_button = ttk.Button(
            self,
            text="Edit Exams",
            command=lambda: controller.create_new_window(EditorPage),
            bootstyle="secondary"
        )
        self.show_editor_button.place(x=1800, y=20, width=100, height=35)
        
    # continuously updates the clock
    def update_clock(self):
        time = arrow.now().format("HH:mm:ss")
        self.clock_canvas.itemconfig(self.time, text=time)
        self.after(1000, self.update_clock)


# timer window to be shown to candidates
class TimerPage(ttk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        
        ttk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        
        # canvas to hold timers
        self.timer_canvas = ttk.Canvas(self)
        self.timer_canvas.pack(fill="both", expand=True)
        
        
        

# editor window to add/configure exams
class EditorPage(ttk.Frame):
    # parent represents the Toplevel window containing the EditorPage
    # controller represents the instance of the App class
    def __init__(self, parent, controller):
        self.controller = controller
        
        ttk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        
        # create a canvas
        self.editor_canvas = tk.Canvas(self)
        self.editor_canvas.pack(fill="both", expand=True)
        
        # draw subject addition/selection elements
        self.new_subject = EditorNewSubject(self.editor_canvas, self.create_subject)
        self.subject_list = EditorSubjectList(self.editor_canvas, self.configure_subject, self.controller.subjects)
    
    # called by EditorNewSubject to register a new subject
    def create_subject(self, subject_name, level):
        if any((subject.name == subject_name and subject.level == level) for subject in self.controller.subjects):
            self.new_subject.status_msg("Subject already exists!")
            return
        
        subject = Subject(subject_name, level)
        self.controller.subjects.append(subject)
        
        # redraw list of subjects
        self.subject_list.update_list(self.controller.subjects)
        
    # called by EditorSubjectList component each time a subject is selected
    def configure_subject(self, subject_index):
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
        # clear existing sections
        self.controller.subjects[self.subject_index].sections = []
        
        # populate sections list with Section objects
        for name, reading_time, hours, minutes in zip(name_list, reading_time_list, hours_list, minutes_list):
            section = Section(name, reading_time, hours, minutes)
            self.controller.subjects[self.subject_index].sections.append(section)

# create an instance of the app
app = App()
app.root.mainloop()
