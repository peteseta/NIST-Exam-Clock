1. Exam:
   - Properties:
     - subject: str (the subject of the exam)
     - duration: int (the duration of the exam in minutes)
     - sections: List[Section] (a list of sections for the exam)
   - Methods:
     - add_section(section: Section) -> None (adds a section to the exam)
     - remove_section(section: Section) -> None (removes a section from the exam)

2. Section:
   - Properties:
     - name: str (the name of the section)
   - Methods:
     - No specific methods required

3. ExamClock:
   - Properties:
     - exams: List[Exam] (a list of exams)
     - reading_time: int (the duration of the reading time in minutes)
     - started_exams: List[Exam] (a list of exams that have been started)
   - Methods:
     - add_exam(exam: Exam) -> None (adds an exam to the clock)
     - remove_exam(exam: Exam) -> None (removes an exam from the clock)
     - start_exam(exam: Exam) -> None (starts an exam)
     - stop_exam(exam: Exam) -> None (stops an exam)
     - start_all_exams() -> None (starts all exams)
     - stop_all_exams() -> None (stops all exams)
     - edit_exam(exam: Exam) -> None (opens a form to edit the exam)

4. ExamForm:
   - Properties:
     - exam: Exam (the exam being edited)
   - Methods:
     - save_exam() -> None (saves the edited exam)

5. ClockWindow:
   - Properties:
     - clock: ExamClock (the exam clock instance)
   - Methods:
     - create_exam_form() -> None (creates a form to add or edit exams)
     - update_clock() -> None (updates the clock display)
     - update_exam_list() -> None (updates the list of exams on the interface)