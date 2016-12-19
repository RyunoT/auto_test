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
        button.grid(row=6, column=1, padx=0, pady=50, sticky='')


# main code begin
root = tk.Tk()
root.title("TDP-39XX setup Application")
root.geometry("1600x600")
root.grid()

# serial connect GUI
widget = Widgets()
widget.connect_tdp39()



# quit button GUI
widget.quit()

root.mainloop()




__author__ = 'RyunosukeT'
__date__ = '2016/12/19'
__version__ = '0.1'

