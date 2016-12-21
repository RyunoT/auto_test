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
        pass

    def connect_tdp39(self):
        entry = tk.Entry(width=20)
        entry.grid(row=0, column=0, padx=10, pady=50, sticky='')

        def ser():
            """serial open"""
            entry_input = entry.get()
            try:
                tdp39.serial_open(entry_input)
                tdp39.data_stop()
                tdp39.program_in()
                if tdp39.response == b'O\r\n':
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
                tdp39.program_out()
                tdp39.serial_close()
            except Exception:
                pass
            root.destroy()

        button = tk.Button(text="Disconnect and Quit app", command=quit_command)
        button.grid(row=9, column=1, padx=0, pady=50, sticky='')


class Entry_Label_Button():
    """left Entry right Label, and bottom Button"""

    def __init__(self, column):
        self.column = column
        self.entry_list = []
        self.boolean_list = []

    def setting_entry(self, row_begin, row_end):
        row_count = row_end - row_begin
        self.entry_list = [tk.Entry(width=10)] * row_count  # class val changed
        for row in range(row_count):
            self.entry_list[row] = tk.Entry(width=10)
            self.entry_list[row].grid(row=row + 1, column=self.column, padx=10, pady=10, sticky='e')

    def setting_label(self, row_begin, row_end, label_text):
        row_count = row_end - row_begin
        label_list = [tk.Label] * row_count
        for row in range(row_count):
            label_list[row] = tk.Label(text=label_text[row])
            label_list[row].grid(row=row + 1, column=self.column + 1, padx=0, pady=0, sticky='w')

    def setting_radio(self, row, radio_num, radio_text, var_list):
        """No Use!!!!!"""
        radio_list = [tk.Radiobutton] * radio_num
        for num in range(radio_num):
            radio_list[num] = tk.Radiobutton(text=radio_text[num], variable=var_list[num])
            radio_list[num].grid(row=row + 1, column=self.column)

    def setting_check(self, row, text):
        boolean = tk.BooleanVar()
        self.boolean_list.append(boolean)
        check = tk.Checkbutton(text=text, variable=boolean)
        check.grid(row=row + 1, column=self.column, padx=0, pady=0, sticky='e')

    def setting_button(self, row_count, button_text):
        entry_text = [float] * row_count

    def setting_combo(self):
        """combo box"""

        def button_all():
            """汎用性が足りなさすぎる、entryとcheckを可逆にすべき"""
            for row in range(len(self.entry_list)):
                entry_text[row] = float(self.entry_list[row].get())

            for row in range(len(self.boolean_list)):
                print(self.boolean_list[row].get())
                if self.boolean_list[row].get():
                    entry_text[len(self.entry_list) + row] = float(1)
                else:
                    entry_text[len(self.entry_list) + row] = float(0)

            if self.column == 0:
                tdp39.basic_setup(*tuple(entry_text))
#                print(entry_text)
#                print(tuple(entry_text))
            elif self.column == 2:
                pass
                #tdp39.oscillator(entry_text[0])
            elif self.column == 4:
                pass
                #tdp39.sweep_setup(entry_text[0], entry_text[1], entry_text[2], entry_text[3])
            elif self.column == 6:
                pass
                #tdp39.Npulse_setup(entry_text[0], entry_text[1])
            else:
                pass

        button = tk.Button(text=button_text)
        button['command'] = button_all
        button.grid(row=8, column=self.column + 1, padx=0, pady=0, sticky='')



# main code begin
root = tk.Tk()
root.title("TDP-39XX setup Application")
root.geometry("1600x600")
root.grid()
tdp39 = TDP39.RS232C()  # MUST be global !!!!!!!

# serial connect GUI
widget = Widgets()
widget.connect_tdp39()

# column0-1
c0 = Entry_Label_Button(0)
c0.setting_label(0, 6, ['input', 'display', 'point', 'd_time',
                        'm_avg', 'dynamic'])
c0.setting_entry(0, 6)
c0.setting_check(6, 'output')
c0.setting_button(7, 'Basic config')

# quit button GUI
widget.quit()

root.mainloop()

if __name__ == '__main__':
    pass


__author__ = 'RyunosukeT'
__date__ = '2016/12/19'
__version__ = '0.1'

