from datetime import datetime
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class App(tk.Tk):
    def __init__(self) -> None:
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
        header = Header(container, self)
        header.grid(row=0, column=0, sticky="nsew")

    # handles creating a new window, e.g. for the editor
    def create_new_window(self, frame_class, width=1520, height=760):
        new_window = tk.Toplevel(self.root)
        new_window.geometry(f"{width}x{height}")
        frame = frame_class(new_window, self)
        return new_window
        
class TimerPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="timer page")
        label.pack(side=TOP, padx=10, pady=10)

# adds a clock at the top of the main_window frame
class Header(ttk.Frame):
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
            command=lambda: controller.create_new_window(Editor),
            bootstyle="secondary"
        )
        self.show_editor_button.place(x=1800, y=20, width=100, height=35)
    
    # continuously updates the clock
    def update_clock(self):
        time = datetime.now().strftime("%H:%M:%S")
        self.clock_canvas.itemconfig(self.time, text=time)
        self.after(1000, self.update_clock)
        
class Editor(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.pack(fill="both", expand=True)
        
        label = ttk.Label(self, text="editor page")
        label.pack(padx=10, pady=10)
        
# create an instance of the examclock
app = App()
app.root.mainloop()