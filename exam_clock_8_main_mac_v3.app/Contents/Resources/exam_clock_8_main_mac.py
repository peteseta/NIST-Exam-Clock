import tkmacosx
import tkinter
import time
from tkinter import *

exams = []


class exam:
    def __init__(self, es, d):
        self.exam_subject = es
        self.duration = int(d)
        self.start = 0
        self.thirty_warn = 0
        self.five_warn = 0
        self.end = 0
        self.started = False

    def set_times(self, time):
        self.start = time
        self.thirty_warn = time + (self.duration * 60 - 1800)
        self.five_warn = time + (self.duration * 60 - 300)
        self.end = time + self.duration * 60

    def set_started(self,started):
        self.started = started


class popupWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.l = Label(top, text="Add Exam")
        self.l.pack()
        self.lname = Label(top, text="Subject")
        self.lname.pack()
        self.exname = Entry(top)
        self.exname.pack()
        self.ldur = Label(top, text="Duration (in minutes)")
        self.ldur.pack()
        self.exdur = Entry(top)
        self.exdur.pack()
        self.b = Button(top, text='Add', command=self.add_exam)
        self.b.pack()

    def add_exam(self):
        self.current_exam = exam(self.exname.get(), int(self.exdur.get()))
        exams.append(self.current_exam)
        window.show_exam()
        self.top.destroy()


class popupWindow_start(object):

    def __init__(self, master,exam):
        top = self.top = Toplevel(master)

        self.lname = Label(top, text="Start Time")
        self.lname.pack()
        self.extime = Entry(top)
        self.extime.pack()
        self.b = Button(top, text='Set time', command= lambda : self.start_exam(exam,self.extime.get()))
        self.b.pack()

    def start_exam(self, input_ex,extime):
        for exam in exams:
            if exam.exam_subject == input_ex:
                start_epoch = int(time.mktime(time.strptime((window.day + ' ' + extime), '%d/%m/%Y %H:%M:%S')))
                exam.set_times(start_epoch)
                exam.started = True
        window.show_exam()
        self.top.destroy()

class popupWindow_remove(object):

    def __init__(self, master):
        self.checks = []
        top = self.top = Toplevel(master)

        for exam in exams:
            var = IntVar()
            self.ck = Checkbutton(top, text=exam.exam_subject, variable=var)
            self.ck.pack(anchor=W)
            self.checks.append(var)

        self.b = Button(top, text='Remove Selected', command= lambda : self.remove_sel())
        self.b.pack()
        self.b = Button(top, text='Remove All', command=self.remove_all)
        self.b.pack()

    def remove_sel(self):
        i = 0
        del_list = []
        while i < len(exams):
            if self.checks[i].get() == 1:
                del_list.append(exams[i])
            i = i + 1
        for d in del_list:
            exams.remove(d)

        for widget in window.exams_frame.winfo_children():
            widget.destroy()

        window.show_exam()
        self.top.destroy()

    def remove_all(self):
        exams.clear()

        for widget in window.exams_frame.winfo_children():
            widget.destroy()
        window.show_exam()
        self.top.destroy()


class main_gui_window(
    tkinter.Frame):  # this class determines the visual components of the program, if you want to change how it looks, this is where you will change code
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.day = time.strftime('%d/%m/%Y')
        self.screen_width = 1920
        self.screen_height = 1080

        self.large_clock_frame = tkinter.Frame(bg='#ffffff')
        self.btn_frame = tkinter.Frame(self.large_clock_frame, bg='#ffffff')
        self.btn_frame.pack(fill=tkinter.BOTH, expand=False, padx=0, pady=0, side=tkinter.LEFT)
        self.large_clock = tkinter.Label(self.large_clock_frame, bg='#ffffff', fg='#132e52',
                                         text=time.strftime('%H:%M:%S'),
                                         font=('Helvetica', (int(round(self.screen_height * 0.15))), 'bold'),
                                         width=(int(round(self.screen_width * 0.5))))
        self.add_button = tkmacosx.Button(self.btn_frame, bg='#132e52', fg='#ffffff', activeforeground='#ffffff',
                                          activebackground='#132e52', text='Add Exam',
                                          font=('Helvetica', (int(round(self.screen_height * 0.015))), 'bold'),
                                          command=self.popup)
        self.add_button.pack(expand=False, padx=1, pady=1, anchor=W, side =BOTTOM )
        self.remove_button = tkmacosx.Button(self.btn_frame, bg='#132e52', fg='#ffffff',
                                          activeforeground='#ffffff',
                                          activebackground='#132e52', text='Remove Exam',
                                          font=('Helvetica', (int(round(self.screen_height * 0.015))), 'bold'),
                                          command=lambda:self.popup_remove())
        self.remove_button.pack(expand=False, padx=1, pady=1,anchor=W, side = BOTTOM)
        self.all_button = tkmacosx.Button(self.btn_frame, bg='#132e52', fg='#ffffff', activeforeground='#ffffff',
                                          activebackground='#132e52', text='Start All',
                                          font=('Helvetica', (int(round(self.screen_height * 0.015))), 'bold'),
                                          command= self.start_all)
        self.all_button.pack(expand=False, padx=1, pady=1, anchor=W, side =BOTTOM )
        self.large_clock_frame.pack()

        self.large_clock.pack(fill=tkinter.BOTH, expand=True, padx=0, pady=0, side=tkinter.RIGHT)




        self.exams_frame = tkinter.Frame(bg='#ffffff')
        self.exams_frame_headers = tkinter.Frame(bg='#ffffff')
        self.exams_frame_headers.pack(fill=tkinter.BOTH)
        # Create & Configure frame


        self.exams_frame.pack(fill=tkinter.BOTH)
        self.start_epoch = time.time()
        self.subject_head = tkinter.Label(self.exams_frame_headers)
        self.duration_head = tkinter.Label(self.exams_frame_headers)
        self.start_head = tkinter.Label(self.exams_frame_headers)
        self.thirty_head = tkinter.Label(self.exams_frame_headers)
        self.five_head = tkinter.Label(self.exams_frame_headers)
        self.end_head = tkinter.Label(self.exams_frame_headers)

        self.subject_head.configure(bg='#ffffff', fg='#132e52', anchor='w', text='SUBJECT(s)',
                                    font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.017))))
        self.duration_head.configure(bg='#ffffff', fg='#132e52', anchor='center', text='DURATION',
                                     font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.0050))))
        self.start_head.configure(bg='#ffffff', fg='#132e52', anchor='center', text='START',
                                  font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.0050))))
        self.thirty_head.configure(bg='#ffffff', fg='#132e52', anchor='center', text='30 Min',
                                   font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.0050))))
        self.five_head.configure(bg='#ffffff', fg='#132e52', anchor='center', text='5 Min',
                                 font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.0050))))
        self.end_head.configure(bg='#ffffff', fg='#132e52', anchor='center', text='END', font=('Helvetica', 35, 'bold'),
                                width=(int(round(self.screen_width * 0.0080))))

        self.subject_head.grid(row=0, column=0, pady=2, padx=10)
        self.duration_head.grid(row=0, column=1, pady=2)
        self.start_head.grid(row=0, column=2, pady=2)
        self.thirty_head.grid(row=0, column=3, pady=2)
        self.five_head.grid(row=0, column=4, pady=2)
        self.end_head.grid(row=0, column=5, pady=2)



        self.show_exam()
        self.update_large_clock()  # this function updates the large clock. It must be called at the end of the class

    def popup(self):
        self.w = popupWindow(self.master)
        self.add_button["state"] = "disabled"
        self.remove_button["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.add_button["state"] = "normal"
        self.remove_button["state"] = "normal"

    def popup_start_later(self,exam_later):
        self.w = popupWindow_start(self.master,exam_later)
        self.startnow_button["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.startnow_button["state"] = "normal"

    def popup_remove(self):
        self.w = popupWindow_remove(self.master)
        self.add_button["state"] = "disabled"
        self.remove_button["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.add_button["state"] = "normal"
        self.remove_button["state"] = "normal"

    def update_large_clock(self):
        self.large_clock.configure(text=time.strftime('%H:%M:%S'))
        self.after(200, self.update_large_clock)
    
    def start_all(self):
        for exam in exams:
            start_epoch = int(time.mktime(time.strptime((window.day + ' ' + time.strftime('%H:%M:%S')), '%d/%m/%Y %H:%M:%S')))
            if exam.started == False:
                exam.set_times(start_epoch)
                exam.started = True
        self.show_exam()

    def start_now(self,subject):
        start_epoch = int(time.mktime(time.strptime((window.day + ' ' + time.strftime('%H:%M:%S')), '%d/%m/%Y %H:%M:%S')))
        for exam in exams:
            print(subject)
            if exam.exam_subject == subject:
                exam.started = True
                exam.set_times(start_epoch)
        self.show_exam()




    def show_exam(self):
        sortedBystatus = sorted(exams, key=lambda x: x.started,reverse=True)
        i = 1
        for exam in sortedBystatus:
            self.subject = tkinter.Label(self.exams_frame)
            self.duration = tkinter.Label(self.exams_frame)
            self.start = tkinter.Label(self.exams_frame)
            self.thirty = tkinter.Label(self.exams_frame)
            self.five = tkinter.Label(self.exams_frame)
            self.end = tkinter.Label(self.exams_frame)


            color = "#132e52"
            if (exam.started == False):
                color = "#D3D3D3"
                self.startnow_button = tkinter.Button(self.exams_frame)
                self.startlater_button = tkinter.Button(self.exams_frame)
                self.startnow_button.configure(bg='#132e52', fg='#ffffff', activeforeground='#ffffff',
                                               activebackground='#132e52', text='Start Now',
                                               font=('Helvetica', 10, 'bold'),
                                               command=lambda i=exam.exam_subject: self.start_now(i), width=10,
                                               height=2)
                self.startlater_button.configure(bg='#132e52', fg='#ffffff', activeforeground='#ffffff',
                                                 activebackground='#132e52', text='Start Later',
                                                 font=('Helvetica', 10, 'bold'),
                                                 command=lambda j=exam.exam_subject: self.popup_start_later(j),
                                                 width=10, height=2)



            self.subject.configure(bg='#ffffff', fg=color, anchor='w', text=exam.exam_subject,
                                   font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.017))))
            self.duration.configure(bg='#ffffff', fg=color, anchor='center', text=exam.duration,
                                    font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.0050))))
            self.start.configure(bg='#ffffff', fg=color, anchor='center',
                                 text=time.strftime('%H:%M:%S', time.localtime(exam.start)),
                                 font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.0050))))
            self.thirty.configure(bg='#ffffff', fg=color, anchor='center',
                                  text=time.strftime('%H:%M:%S', time.localtime(exam.thirty_warn)),
                                  font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.0050))))
            self.five.configure(bg='#ffffff', fg=color, anchor='center',
                                text=time.strftime('%H:%M:%S', time.localtime(exam.five_warn)),
                                font=('Helvetica', 26, 'bold'), width=(int(round(self.screen_width * 0.0050))))
            self.end.configure(bg='#ffffff', fg=color, anchor='center',
                               text=time.strftime('%H:%M:%S', time.localtime(exam.end)), font=('Helvetica', 50, 'bold'),
                               width=10)


            self.subject.grid(row=i, column=0, pady=0, padx=10)
            self.duration.grid(row=i, column=1, pady=0)

            if exam.started == False:
                self.startnow_button.grid(row=i, column=2, pady=4)
                self.startlater_button.grid(row=i, column=3, pady=4)
            else:
                self.start.grid(row=i, column=2, pady=2)
                self.thirty.grid(row=i, column=3, pady=2)
                self.five.grid(row=i, column=4, pady=2)
                self.end.grid(row=i, column=5, pady=2)
            i = i + 1


main_frame = tkinter.Tk()
window = main_gui_window(main_frame)
exams.append(exam("Business Management HL & SL paper 1",int(60)))
exams.append(exam("Business Management HL & SL paper 2",int(60)))
exams.append(exam("3not active",int(60)))
exams.append(exam("4not active",int(60)))
exams.append(exam("5active",int(60)))
exams.append(exam("6not active",int(60),))
main_frame.title('NIST Exam Clock')  # title of the window
main_frame.geometry('1920x1080')  # size of the window (best practice is to set it to the resolution of the machine)
main_frame.config(bg='#ffffff')  # overall background of the program\
window.update()
main_frame.mainloop()
