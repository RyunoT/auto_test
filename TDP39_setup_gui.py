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
import tkinter.ttk as ttk
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


class Entry_Combo_Check():
    """left Entry right Label, and bottom Button"""

    def __init__(self, column):
        self.column = column
        self.entry_list = []
        self.combo_list = []
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

    def setting_combo(self, row, text_list):
        """combo box"""
        combo = ttk.Combobox(values=text_list, textvariable=tk.StringVar, width=10, state='readonly')
        combo.grid(row=row + 1, column=self.column, padx=0, pady=5, sticky='e')
        self.combo_list.append(combo)

    def setting_check(self, row, text):
        boolean = tk.BooleanVar()
        self.boolean_list.append(boolean)
        check = tk.Checkbutton(text=text, variable=boolean)
        check.grid(row=row + 1, column=self.column, padx=0, pady=5, sticky='e')

    def setting_button(self, button_text):
        """もはや個別に作ってしまった方がマシなのでは？？？継承を使えばいいかも"""

        entry_text = []

        def button_all():
            """entry, combo, check の順番は固定、変えるならfor if の文"""
            del entry_text[:]

            for row in range(len(self.entry_list)):
                entry_text.append(float(self.entry_list[row].get()))

            for row in range(len(self.combo_list)):
                """if you get str, must change TDP39.py"""
                entry_text.append(self.combo_list[row].get())

            for row in range(len(self.boolean_list)):
                if self.boolean_list[row].get():
                    entry_text.append(float(1))
                else:
                    entry_text.append(float(0))

            try:
                tdp39.basic_setup(*tuple(entry_text))
            except:
                tkmsg.showinfo('Error', 'Please fill in ALL boxes in column')

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
c0 = Entry_Combo_Check(0)
c0_label_text = ['Input rate(Hz)\r[0.00001 ~ 999999]',
                 'Display rate(Hz)\r[0.00001 ~ 999999]',
                 'Display refresh(sec)\r[0.1 ~ 99.9]',
                 'Point\r[1 ~ 6: Static]',
                 'Moving avg(count)\r[1 ~ 8]',
                 'Dynamic prediction\r[1: Slow ~ 7: Fast]']
c0.setting_label(0, 6, c0_label_text)
c0.setting_entry(0, 3)
c0_combo_text0 = ['Auto', '1', '2', '3', '4', '5', '6']
c0.setting_combo(3, c0_combo_text0)
c0_combo_text1 = ['1', '2', '3', '4', '5', '6', '7', '8']
c0.setting_combo(4, c0_combo_text1)
c0_combo_text2 = ['OFF', '1', '2', '3', '4', '5', '6', '7']
c0.setting_combo(5, c0_combo_text2)
c0.setting_check(6, 'Output')

c0.setting_button('Basic config')




# quit button GUI
widget.quit()

root.mainloop()

if __name__ == '__main__':
    pass


__author__ = 'RyunosukeT'
__date__ = '2016/12/19'
__version__ = '0.1'

