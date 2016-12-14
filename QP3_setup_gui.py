#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
QP3をセットアップするGUIを備えたアプリケーションです
"""
# Date: 2016/12/13
# Filename: qp3_setup_gui

import sys
import tkinter as tk
import QP3
import time

root = tk.Tk()


def create_widgets():
    # ラベル
    # label = tk.Label(text='シリアルポート')
    # label.grid(row=0, column=0, padx=2, pady=10, sticky='')

    # エントリー
    editbox = tk.Entry(width=20)
    editbox.grid(row=0, column=0, padx=10, pady=50, sticky='')

    def ser():
        """serial open"""
        edit_input = editbox.get()
        print(edit_input)

        qp3.serial_open(edit_input)

    # ボタン
    button1 = tk.Button(text='シリアルポート接続')
    button1['command'] = ser
    button1.grid(row=0, column=1, padx=0, pady=0, sticky='')


def allmode():
    """QP3 allmode setup"""
    allmode_edit1 = tk.Entry(width=10)
    allmode_edit1.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    allmode_button1 = tk.Button(text="High_V")
    allmode_button1['command'] = allmode_button1
    allmode_button1.grid(row=1, column=1, padx=0, pady=0, sticky='w')

    allmode_edit2 = tk.Entry(width=10)
    allmode_edit2.grid(row=2, column=0, padx=10, pady=10, sticky='e')
    allmode_button2 = tk.Button(text="High_V")
    allmode_button2['command'] = allmode_button2
    allmode_button2.grid(row=2, column=1, padx=0, pady=0, sticky='w')

    allmode_edit3 = tk.Entry(width=10)
    allmode_edit3.grid(row=3, column=0, padx=10, pady=10, sticky='e')
    allmode_button3 = tk.Button(text="A_B")
    allmode_button3['command'] = allmode_button1
    allmode_button3.grid(row=3, column=1, padx=0, pady=0, sticky='w')

    allmode_edit4 = tk.Entry(width=10)
    allmode_edit4.grid(row=4, column=0, padx=10, pady=10, sticky='e')
    allmode_button4 = tk.Button(text="Output_mode")
    allmode_button4['command'] = allmode_button1
    allmode_button4.grid(row=4, column=1, padx=0, pady=0, sticky='w')

    def allmode_button_all():
        """allmode setup button"""
        allmode_input1 = float(allmode_edit1.get())
        allmode_input2 = float(allmode_edit2.get())
        allmode_input3 = float(allmode_edit3.get())
        allmode_input4 = float(allmode_edit4.get())
        qp3.program_in()
        qp3.allmode_setup(float(allmode_input1), float(allmode_input2),
                          float(allmode_input3), float(allmode_input4))
        qp3.program_out()

    allmode_button5 = tk.Button(text="All_setup")
    allmode_button5['command'] = allmode_button_all
    allmode_button5.grid(row=5, column=1, padx=0, pady=0, sticky='')


def quit():
    """quit"""
    def quit_command():
        qp3.serial_close()
        root.destroy()
    button2 = tk.Button(text="QUIT", command=quit_command)
    button2.grid(row=6, column=1, padx=0, pady=50, sticky='')


root.title("QP-3 setup Application")
root.geometry("800x600")
root.grid()

qp3 = QP3.USB()
create_widgets()
allmode()
quit()

root.mainloop()

__author__ = 'RyunosukeT'
__date__ = '2016/12/13'
__version__ = '0.1'
