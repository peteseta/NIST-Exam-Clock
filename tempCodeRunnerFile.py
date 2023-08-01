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