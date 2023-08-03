import datetime
import tkinter as tk
from tkinter.constants import HORIZONTAL

import ttkbootstrap as ttk

from style import HEADING


class Timer:
    def __init__(self, parent, callback, subjects_with_duration, duration) -> None:
        self.frame = ttk.Frame(parent, padding=10)
        self.callback = callback
        self.duration = duration
        self.subjects = subjects_with_duration

        self.progress_bar = ProgressBar(self.frame)
        self.subject_list = SubjectList(self.frame, subjects_with_duration)

        self.is_running = False
        self.finished = False

        # update text to show duration
        self.progress_bar.update(datetime.timedelta(0), duration, duration)

    def start_timer(self):
        self.start_time = datetime.datetime.now()
        self.end_time = self.start_time + self.duration
        self.thirty_min = self.end_time - datetime.timedelta(minutes=30)
        self.five_min = self.end_time - datetime.timedelta(minutes=5)

        self.is_running = True
        self.update_loop()

    def update_loop(self):
        self.elapsed = datetime.datetime.now() - self.start_time
        self.remaining = self.end_time - datetime.datetime.now()

        if datetime.datetime.now() >= self.end_time:
            self.finished = True
            self.callback(self.subjects)
        else:
            self.progress_bar.update(self.elapsed, self.remaining, self.duration)

        self.frame.after(1000, self.update_loop)


class ProgressBar:
    def __init__(self, parent) -> None:
        self.canvas = ttk.Canvas(
            parent,
            height=120,
            width=440,
        )
        self.canvas.grid(row=0)

        self.canvas.create_text(
            0.0, 0.0, anchor="nw", text="ELAPSED", fill="#121212", font=HEADING[3]
        )

        self.elapsed = self.canvas.create_text(
            0, 25.0, anchor="nw", text="47m 13s", fill="#121212", font=HEADING[1]
        )

        self.canvas.create_text(
            440, 0.0, anchor="ne", text="REMAINING", fill="#121212", font=HEADING[2]
        )

        self.remaining = self.canvas.create_text(
            440, 25.0, anchor="ne", text="1h 47m 13s", fill="#121212", font=HEADING[1]
        )

        self.progressbar_value = tk.IntVar()
        self.progressbar = ttk.Progressbar(
            self.canvas,
            orient=HORIZONTAL,
            length=440,
            variable=self.progressbar_value,
            mode="determinate",
            bootstyle="primary",
        )
        self.progressbar.place(x=0, y=70)
        self.progressbar_value.set(50)

    def update(self, elapsed, remaining, duration):
        if elapsed.total_seconds() < 3600:
            elapsed_text = str(elapsed)[2:7]  # format as MM:SS
        else:
            elapsed_text = str(elapsed).split(".")[0]  # format as HH:MM:SS

        if remaining.total_seconds() < 3600:
            remaining_text = str(remaining)[2:7]  # format as MM:SS
        else:
            remaining_text = str(remaining).split(".")[0]  # format as HH:MM:SS

        self.canvas.itemconfig(self.elapsed, text=elapsed_text)
        self.canvas.itemconfig(self.remaining, text=remaining_text)

        self.progressbar_value.set(
            100 * elapsed.total_seconds() / duration.total_seconds()
        )


class SubjectList:
    def __init__(self, parent, subjects) -> None:
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=1, sticky="w")

        self.labels = []

        for index, subject in enumerate(subjects):
            self.labels.append(
                SubjectLabel(self.frame, subject.name, subject.sections[0].name)
            )
            self.labels[index].canvas.grid(row=index, sticky="w")


class SubjectLabel:
    def __init__(self, parent, subject_name, section_name) -> None:
        self.canvas = ttk.Frame(parent, width=440)
        ttk.Label(
            self.canvas,
            text=subject_name,
            wraplength=440,
            justify="left",
            anchor="w",
            foreground="#121212",
            font=HEADING[1],
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            self.canvas,
            text=section_name,
            wraplength=440,
            justify="left",
            anchor="w",
            foreground="#838383",
            font=HEADING[2],
        ).grid(row=1, column=0, sticky="w")
