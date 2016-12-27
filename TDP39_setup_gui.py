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
        for row in range(row_count):
            entry = tk.Entry(width=10)
            entry.grid(row=row_begin + row + 1, column=self.column, padx=10, pady=10, sticky='e')
            self.entry_list.append(entry)

    def setting_label(self, row_begin, row_end, label_text):
        row_count = row_end - row_begin
        label_list = [tk.Label] * row_count
        for row in range(row_count):
            label_list[row] = tk.Label(text=label_text[row])
            label_list[row].grid(row=row_begin + row + 1, column=self.column + 1, padx=0, pady=0, sticky='w')

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

    def setting_button(self, button_text, tdp39_function):
        """tdp39_functionはTDP39.pyから引っ張ってくること"""
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
                tdp39_function(*tuple(entry_text))
            except:
                # tkmsg.showinfo('Error', 'Please fill in ALL boxes in column')
                pass

        button = tk.Button(text=button_text)
        button['command'] = button_all
        button.grid(row=8, column=self.column + 1, padx=0, pady=0, sticky='')


class Comparator(Entry_Combo_Check):
    """
    コンパレータGUI作成用
    """
    def __init__(self, column):
        Entry_Combo_Check.__init__(self, column)

    def setting_combo(self, row, column, text_list):
        combo = ttk.Combobox(values=text_list, textvariable=tk.StringVar, width=2, state='readonly')
        combo.grid(row=row + 1, column=self.column + column, padx=0, pady=5, sticky='e')
        self.combo_list.append(combo)

    def setting_entry(self, row_begin, row_end, column):
        row_count = row_end - row_begin
        for row in range(row_count):
            entry = tk.Entry(width=10)
            entry.grid(row=row_begin + row + 1, column=self.column + column, padx=10, pady=10, sticky='e')
            self.entry_list.append(entry)


    def setting_label(self, row_begin, row_end, column, w_or_e, label_text):
        row_count = row_end - row_begin
        label_list = [tk.Label] * row_count
        for row in range(row_count):
            label_list[row] = tk.Label(text=label_text[row])
            label_list[row].grid(row=row_begin + row + 1, column=self.column + column, padx=0, pady=0, sticky=w_or_e)

    def setting_combo2(self, row, column, text_list):
        combo = ttk.Combobox(values=text_list, textvariable=tk.StringVar, width=8, state='readonly')
        combo.grid(row=row + 1, column=self.column + column, columnspan=2, padx=0, pady=5, sticky='e')
        self.combo_list.append(combo)

    def setting_button(self, button_text, tdp39_function):
        """tdp39_functionはTDP39.pyから引っ張ってくること"""
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
                print(entry_text)
                tdp39_function(*tuple(entry_text))
            except:
                # tkmsg.showinfo('Error', 'Please fill in ALL boxes in column')
                pass

        button = tk.Button(text=button_text)
        button['command'] = button_all
        button.grid(row=8, column=self.column + 1, columnspan=3, padx=0, pady=0, sticky='')




# main code begin
root = tk.Tk()
root.title("TDP-39XX setup Application")
root.geometry("1600x600")
root.grid()
tdp39 = TDP39.RS232C()  # MUST be global !!!!!!!

# serial connect GUI
widget = Widgets()
widget.connect_tdp39()

# column 0-1
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
c0.setting_button('Basic config', tdp39.basic_setup)


# column 2-3
c1 = Entry_Combo_Check(2)
c1_label_text = ['Divide(count)\r[1 ~ 999]',
                 'Input Pulse',
                 'f or T',
                 'Hold mode',
                 'Chattering Suppression']
c1.setting_label(0, 4, c1_label_text)
c1.setting_entry(0, 1)
c1_combo_pulse = ['Single', 'UP/DOWN', 'A/B']
c1_combo_f_or_T = ['Frequency', 'Period']
c1_combo_hold = ['Data', 'Peak', 'Valley']
c1.setting_combo(1, c1_combo_pulse)
c1.setting_combo(2, c1_combo_f_or_T)
c1.setting_combo(3, c1_combo_hold)
c1.setting_check(4, 'Chattering\rSuppression')
c1.setting_button('Mode Config', tdp39.mode_setup)


# column 4-5
c2 = Entry_Combo_Check(4)
c2_label_text = ['Input rate(Hz)\r[0.00001 ~ 999999]',
                 'Display rate(Hz)\r[0.00001 ~ 999999]',
                 'Point\r[1 ~ 6: Static]']
c2.setting_label(0, 3, c2_label_text)
c2.setting_entry(0, 2)
c2_combo_text0 = ['Auto', '1', '2', '3', '4', '5', '6']
c2.setting_combo(2, c2_combo_text0)
c2.setting_button('Dual Range Config', tdp39.dual_setup)


# column 6-9
c3 = Comparator(6)
c3.setting_label(0, 1, 0, 'e', ['     If Input '])
c3.setting_combo(0, 1, ['≦', '≧'])
c3.setting_entry(0, 1, 2)
c3.setting_label(0, 1, 3, 'w', ['Hz'])
c3.setting_label(1, 2, 2, 'e', ['Comp High = '])
c3.setting_combo(1, 3, ['+V', '-V'])

c3.setting_label(2, 3, 0, 'e', ['     If Input '])
c3.setting_combo(2, 1, ['≦', '≧'])
c3.setting_entry(2, 3, 2)
c3.setting_label(2, 3, 3, 'w', ['Hz'])
c3.setting_label(3, 4, 2, 'e', ['Comp Low = '])
c3.setting_combo(3, 3, ['+V', '-V'])
c3.setting_combo2(4, 0, ['Display', 'Analog Out'])
c3.setting_label(4, 5, 2, 'w', ['Comp Sync'])
c3.setting_button('Comparator Config', tdp39.comparator_setup)

#c3.setting_combo()

# quit button GUI
widget.quit()

root.mainloop()

if __name__ == '__main__':
    pass


__author__ = 'RyunosukeT'
__date__ = '2016/12/19'
__version__ = '0.1'

