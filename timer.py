import datetime
import tkinter as tk
from tkinter.constants import HORIZONTAL

import ttkbootstrap as ttk

from style import HEADING


class Timer:
    def __init__(
        self, parent, callback, subjects_with_duration, duration, section_id
    ) -> None:
        """
        Initializes the UI component for one timer
        (one timer for one duration; one timer can have multiple subjects)
        
        Args:
            parent (TimerPage): parent tkinter frame
            callback (function): TimerPage.finish()
            subjects_with_duration (list): list of subjects with the same duration
            duration (datetime.timedelta): duration of the timer
            section_id (list): IDs for each section in the timer
            # TODO: use unique id to allow changing details after starting timer
        """
        self.frame = ttk.Frame(parent, padding=10)
        self.frame.grid_rowconfigure(2, weight=1)  # expand Info to bottom

        self.callback = callback
        self.duration = duration

        self.subjects = subjects_with_duration
        self.section_id = section_id

        self.progress_bar = ProgressBar(self.frame)
        self.subject_list = SubjectList(self.frame, subjects_with_duration)

        self.is_running = False
        self.finished = False

        # update text to show duration
        self.progress_bar.update(datetime.timedelta(0), duration, duration)

    def start_timer(self):
        """
        Calculates the start time, end time, 5 and 30min warnings if applicable
        Adds this information in an info frame (Info class)
        """
        self.start_time = datetime.datetime.now()
        self.end_time = self.start_time + self.duration
        if self.duration > datetime.timedelta(minutes=30):
            self.thirty_min = self.end_time - datetime.timedelta(minutes=30)
        else:
            self.thirty_min = None

        if self.duration > datetime.timedelta(minutes=5):
            self.five_min = self.end_time - datetime.timedelta(minutes=5)
        else:
            self.five_min = None

        self.info = Info(
            self.frame,
            self.duration,
            self.start_time,
            self.end_time,
            self.thirty_min,
            self.five_min,
        )

        self.is_running = True
        self.update_loop()

    def update_loop(self):
        """
        Calculates the elapsed and remaining time
        If the timer is over, call the callback
        Calls itself to update every second
        """
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
        """
        Initializes the UI for the progressbar and elapsed/remaining text

        Args:
            parent (ttk.Frame): parent Timer frame
        """
        self.canvas = ttk.Canvas(parent, height=120, width=440)
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
        """
        Updates the elapsed/remaining text and the progressbar

        Args:
            elapsed (datetime.timedelta): elapsed time
            remaining (datetime.timedelta): remaining time
            duration (datetime.timedelta): total duration of the section
        """
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
        """
        Initializes the UI for the list of subject names for this timer
        Creates a SubjectLabel element for each subject/section in the timer

        Args:
            parent (ttk.Frame): parent Timer frame
            subjects (list): list of Subject objects in the timer
        """
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=1, sticky="nw")

        self.labels = []

        for index, subject in enumerate(subjects):
            if subject.sections[index].section_in_progress:
                self.labels.append(
                    SubjectLabel(self.frame, subject.name, subject.sections[index].name)
                )
                self.labels[index].frame.grid(row=index, sticky="w")


class SubjectLabel:
    def __init__(self, parent, subject_name, section_name) -> None:
        """
        Initializes the UI for a single subject's label

        Args:
            parent (ttk.Frame): parent SubjectList frame
            subject_name (str): name of the subject
            section_name (str): name of the section
        """
        self.frame = ttk.Frame(parent, width=440)
        ttk.Label(
            self.frame,
            text=subject_name,
            wraplength=440,
            justify="left",
            anchor="w",
            foreground="#121212",
            font=HEADING[1],
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            self.frame,
            text=section_name,
            wraplength=440,
            justify="left",
            anchor="w",
            foreground="#838383",
            font=HEADING[2],
        ).grid(row=1, column=0, sticky="w")


class Info:
    def __init__(
        self, parent, duration, start_time, end_time, thirty_min, five_min
    ) -> None:
        """
        Initializes the UI for the info section of the timer

        Args:
            parent (ttk.Frame): parent Timer frame
            duration (datetime.timedelta): total duration of the timer
            start_time (datetime.datetime): start time of the timer
            end_time (datetime.datetime): end time of the timer
            thirty_min (datetime.datetime): time of the 30-minute mark
            five_min (datetime.datetime): time of the 5-minute mark
        """
        self.frame = ttk.Frame(parent, width=440)
        self.frame.grid(row=2, sticky="sw")
        self.frame.grid_rowconfigure(2, weight=1)

        self.duration = (datetime.datetime(1, 1, 1) + duration).strftime("%Hh %Mm")
        self.start_time = start_time.strftime("%H:%M")
        self.end_time = end_time.strftime("%H:%M")
        self.thirty_min = thirty_min.strftime("%H:%M") if thirty_min else None
        self.five_min = five_min.strftime("%H:%M") if five_min else None

        if self.thirty_min and self.five_min:
            label_text = f"30m: {self.thirty_min} | 5min: {self.five_min}"
        elif self.thirty_min:
            label_text = f"30m: {self.thirty_min}"
        elif self.five_min:
            label_text = f"5min: {self.five_min}"
        else:
            label_text = ""

        ttk.Label(
            self.frame,
            text=f"{self.duration} ({self.start_time} → {self.end_time})",
            font=HEADING[4],
            foreground="#838383",
        ).grid(row=0, column=0, sticky="sw")
        ttk.Label(
            self.frame,
            text=label_text,
            font=HEADING[4],
            foreground="#838383",
        ).grid(row=1, column=0, sticky="sw")
