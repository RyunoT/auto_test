#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
TDP-39XX setup application
"""
# Date: 2016/12/19
# Filename: TDP39_setup_gui

import sys
import tkinter as tk
import tkinter.messagebox as tkmsg
import TDP39
import time



class Widgets(object):
    def __init__(self):
        self.tdp39 = TDP39.RS232C()

    def connect_tdp39(self):
        entry = tk.Entry(width=20)
        entry.grid(row=0, column=0, padx=10, pady=50, sticky='')

        def ser():
            """serial open"""
            entry_input = entry.get()
            try:
                self.tdp39.serial_open(entry_input)
                self.tdp39.program_in()
                time.sleep(1)
                self.tdp39.program_in()  # First TDP39X connection is not respond sometimes
                if self.tdp39.response == b'O\r\x00':
                    self.tdp39.data_stop()
                    tkmsg.showinfo('Connect', 'Welcome to TDP-39XX')
                else:
                    pass
            except Exception:
                tkmsg.showinfo('Error', 'Port Number Error!!')

        button = tk.Button(text='Connect TDP-39XX')
        button['command'] = ser
        button.grid(row=0, column=1, padx=0, pady=0, sticky='')

    def quit(self):
        def quit_command():
            try:
                self.tdp39.program_out()
                self.tdp39.serial_close()
            except:
                pass
            root.destroy()

        button = tk.Button(text="Disconnect and Quit app", command=quit_command)
        button.grid(row=8, column=1, padx=0, pady=50, sticky='')


class Entry_Label_Button(object):
        """left Entry right Label, and bottom Button"""

        def __init__(self, column):
            self.tdp39 = TDP39.RS232C()
            self.column = column
            self.entry_list = [tk.Entry(width=10)]

        def setting_entry(self, row_begin, row_end):
            row_count = row_end - row_begin
            entry_list = self.entry_list * row_count
            for row in range(row_count):
                entry_list[row] = tk.Entry(width=10)
                entry_list[row].grid(row=row + 1, column=self.column, padx=10, pady=10, sticky='e')

        def setting_label(self, row_begin, row_end, label_text):
            row_count = row_end - row_begin
            label_list = [tk.Label] * row_count
            for row in range(row_count):
                label_list[row] = tk.Label(text=label_text[row])
                label_list[row].grid(row=row + 1, column=self.column + 1, padx=0, pady=0, sticky='w')

        def setting_button(self, row_count, button_text, column):
            entry_text = [float] * row_count

            def button_all():
                for row in range(row_count):
                    entry_text[row] = float(entry_list[row].get())
                self.tdp39.program_in()
                if column == 0:
                    self.tdp39.basic_setup(*tuple(entry_text))
                elif column == 1:
                    self.tdp39.oscillator(entry_text[0])
                elif column == 2:
                    self.tdp39.sweep_setup(entry_text[0], entry_text[1], entry_text[2], entry_text[3])
                elif column == 3:
                    self.tdp39.Npulse_setup(entry_text[0], entry_text[1])
                else:
                    pass

            button = tk.Button(text=button_text)
            button['command'] = button_all
            button.grid(row=5, column=self.column + 1, padx=0, pady=0, sticky='')

'''        def setting_ELB(self):
            """Entry Label Button"""
            self.setting_entry()
            self.setting_label()
            self.setting_button(self.button_select)
'''


# main code begin
root = tk.Tk()
root.title("TDP-39XX setup Application")
root.geometry("1600x600")
root.grid()

# serial connect GUI
widget = Widgets()
widget.connect_tdp39()

# column0-1
c0 = Entry_Label_Button(0)
c0.setting_label(0, 7, ['input', 'display', 'point', 'd_time',
                        'm_avg', 'dynamic', 'output'])
c0.setting_entry(0, 7)


# quit button GUI
widget.quit()

root.mainloop()




__author__ = 'RyunosukeT'
__date__ = '2016/12/19'
__version__ = '0.1'

