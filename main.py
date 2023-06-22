from datetime import datetime
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class App(tk.Tk):
    def __init__(self) -> None:
        self.root = ttk.Window(themename="flatly")
        self.root.title("NIST Exam Clock")
        self.root.geometry("1600x900")

        # creating a frame and assigning it to container
        container = ttk.Frame(self.root, height=900, width=1600)
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
  
        # frame switching logic
        self.frames = {}
        for i in (TimerPage, ConfigPage):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

        # add header to container, keep on row 0 = up top
        header = Header(container, self)
        header.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(TimerPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()
        
class TimerPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="timer page")
        label.pack(padx=10, pady=10)

        switch_window_button = ttk.Button(
            self,
            text="Config",
            command=lambda: controller.show_frame(ConfigPage),
        )
        switch_window_button.pack(side="bottom")
        
class ConfigPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="config page")
        label.pack(padx=10, pady=10)

        switch_window_button = ttk.Button(
            self,
            text="Return to Timer",
            command=lambda: controller.show_frame(TimerPage))
             
        switch_window_button.pack(side="bottom")

# adds a clock at the top of the main_window frame
class Header(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        
        # bg canvas for clock
        self.clock_canvas = ttk.Canvas(
            self,
            height=80,
            width=1600
        )
        self.clock_canvas.pack()
        
        self.clock_canvas.configure(background="#EEEEEE")
        
        self.time = self.clock_canvas.create_text(
            20.0,
            40.0,
            anchor="w",
            text="00:00:00",
            fill="#121212",
            font=("SF Pro Display Bold", 50)
        )
        
        self.update_clock()
    
    # continuously updates the clock
    def update_clock(self):
        time = datetime.now().strftime("%H:%M:%S")
        self.clock_canvas.itemconfig(self.time, text=time)
        self.after(1000, self.update_clock)
        
# create an instance of the examclock
app = App()
app.root.mainloop()