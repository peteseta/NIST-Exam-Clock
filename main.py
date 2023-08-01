from datetime import datetime, timedelta
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# constants for font sizes - treat like H0, H1, etc. in markdown
HEADING = ["system 200 bold", "system 48 bold", "system 32 bold", "system 32"]
# for colors, the custom ttkbootstrap theme named "robin" is packaged.

# represents an IB subject which may contain multiple papers.
class Subject():
    def __init__(self, name) -> None:
        self.name = name
        self.exams = []
    
    def add_exam(self, exam):
        self.exams.append(exam)

# represents a single paper, e.g. Paper 1 of a subject.
class Exam(Subject):
    def __init__(self, subject, name, hours, minutes) -> None:
        super().__init__(subject)
        self.name = name
        self.duration = timedelta(hours=hours, minutes=minutes)

class App(tk.Tk):
    def __init__(self) -> None:
        # init subject list
        self.subjects = []
        
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
        time = datetime.now().strftime("%H:%M:%S")
        self.clock_canvas.itemconfig(self.time, text=time)
        self.after(1000, self.update_clock)

# timer window to be shown to candidates
class TimerPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        # Create the grid headers
        subject_label = ttk.Label(self, text="Subject")
        subject_label.grid(row=0, column=0, padx=10, pady=10)

        exam_label = ttk.Label(self, text="Exam")
        exam_label.grid(row=0, column=1, padx=10, pady=10)

        time_label = ttk.Label(self, text="Time Remaining")
        time_label.grid(row=0, column=2, padx=10, pady=10)

        # Populate the grid with exam details
        for i, subject in enumerate(controller.subjects):
            for j, exam in enumerate(subject.exams):
                subject_name = ttk.Label(self, text=subject.name)
                subject_name.grid(row=i+1, column=0, padx=10, pady=10)

                exam_name = ttk.Label(self, text=exam.name)
                exam_name.grid(row=i+1, column=1, padx=10, pady=10)

                time_remaining = ttk.Label(self, text=self.get_time_remaining(exam.duration))
                time_remaining.grid(row=i+1, column=2, padx=10, pady=10)

    def get_time_remaining(self, duration):
        remaining = duration - datetime.now().time()
        return str(remaining)

# editor window to add/configure exams
class EditorPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)

        self.title = ttk.Label(self, text="Edit/Configure Exams", font=HEADING[2])
        self.title.grid(row=0, column=0, columnspan=2, padx=20, pady=10)

        # Left side for configuring subject detail
        self.subj_conf_name = tk.StringVar()

        self.name_label = ttk.Label(self, anchor="w", text="Subject Name")
        self.name_label.grid(row=1, column=0, padx=10, pady=10)
        self.name_entry = ttk.Entry(self, textvariable=self.subj_conf_name)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Right side for configuring exams for the subject
        self.exam_frame = ttk.Frame(self)
        self.exam_frame.grid(row=1, column=2, padx=10, pady=10)

        self.exam_labels = []
        self.exam_entries = []

        self.add_exam_button = ttk.Button(self, text="Add Exam", command=self.add_exam)
        self.add_exam_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.create_button = ttk.Button(self, text="Create", command=self.create_subject)
        self.create_button.grid(row=2, column=2, padx=10, pady=10)

    def add_exam(self):
        exam_label = ttk.Label(self.exam_frame, anchor="w", text="Exam Name")
        exam_label.grid(row=len(self.exam_labels), column=0, padx=10, pady=10)
        exam_entry = ttk.Entry(self.exam_frame)
        exam_entry.grid(row=len(self.exam_entries), column=1, padx=10, pady=10)
        self.exam_labels.append(exam_label)
        self.exam_entries.append(exam_entry)

    def create_subject(self):
        subject_name = self.subj_conf_name.get()
        subject = Subject(subject_name)
        for exam_entry in self.exam_entries:
            exam_name = exam_entry.get()
            exam = Exam(subject, exam_name, 0, 0)  # Replace 0, 0 with actual hours and minutes
            subject.add_exam(exam)
        app.subjects.append(subject)
        self.destroy()


# create an instance of the app
app = App()
app.root.mainloop()
