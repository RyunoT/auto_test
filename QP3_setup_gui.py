#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
QP3をセットアップするGUIを備えたアプリケーションです
"""
# Date: 2016/12/13
# Filename: qp3_setup_gui

import sys
import tkinter as tk
import tkinter.messagebox as tkmsg
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
        try:
            qp3.serial_open(edit_input)
        except:
            tkmsg.showinfo('Error', 'ポート番号が違います')

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
    allmode_button3['command'] = allmode_button3
    allmode_button3.grid(row=3, column=1, padx=0, pady=0, sticky='w')

    allmode_edit4 = tk.Entry(width=10)
    allmode_edit4.grid(row=4, column=0, padx=10, pady=10, sticky='e')
    allmode_button4 = tk.Button(text="Output_mode")
    allmode_button4['command'] = allmode_button4
    allmode_button4.grid(row=4, column=1, padx=0, pady=0, sticky='w')

    def allmode_button_all():
        """allmode setup button"""
        allmode_input1 = float(allmode_edit1.get())
        allmode_input2 = float(allmode_edit2.get())
        allmode_input3 = float(allmode_edit3.get())
        allmode_input4 = float(allmode_edit4.get())
        qp3.program_in()
        qp3.allmode_setup(allmode_input1, allmode_input2,
                          allmode_input3, allmode_input4)

    allmode_button5 = tk.Button(text="Output_setup")
    allmode_button5['command'] = allmode_button_all
    allmode_button5.grid(row=5, column=1, padx=0, pady=0, sticky='')


def oscillator():
    edit1 = tk.Entry(width=10)
    edit1.grid(row=1, column=2, padx=10, pady=10, sticky='e')

    def oscillator_button():
        """oscillator mode button"""
        oscillator_input1 = float(edit1.get())
        qp3.program_in()
        qp3.oscillator(oscillator_input1)

    button1 = tk.Button(text="Oscillator_Frequency_Hz")
    button1['command'] = oscillator_button
    button1.grid(row=1, column=3, padx=0, pady=0, sticky='w')

def sweep():
    edit1 = tk.Entry(width=10)
    edit1.grid(row=1, column=4, padx=10, pady=10, sticky='e')
    button1 = tk.Button(text="Start_Hz")
    button1['command'] = button1
    button1.grid(row=1, column=5, padx=0, pady=0, sticky='w')

    edit2 = tk.Entry(width=10)
    edit2.grid(row=2, column=4, padx=10, pady=10, sticky='e')
    button2 = tk.Button(text="Stop_Hz")
    button2['command'] = button2
    button2.grid(row=2, column=5, padx=0, pady=0, sticky='w')

    edit3 = tk.Entry(width=10)
    edit3.grid(row=3, column=4, padx=10, pady=10, sticky='e')
    button3 = tk.Button(text="Sweep_time_sec")
    button3['command'] = button3
    button3.grid(row=3, column=5, padx=0, pady=0, sticky='w')

    edit4 = tk.Entry(width=10)
    edit4.grid(row=4, column=4, padx=10, pady=10, sticky='e')
    button4 = tk.Button(text="Wave_mode")
    button4['command'] = button4
    button4.grid(row=4, column=5, padx=0, pady=0, sticky='w')

    def sweep_button_all():
        """sweep setup button"""
        sweep_input1 = float(edit1.get())
        sweep_input2 = float(edit2.get())
        sweep_input3 = float(edit3.get())
        sweep_input4 = float(edit4.get())
        qp3.program_in()
        qp3.sweep_setup(sweep_input1, sweep_input2,
                        sweep_input3, sweep_input4)

    button5 = tk.Button(text="Sweep_setup")
    button5['command'] = sweep_button_all
    button5.grid(row=5, column=5, padx=0, pady=0, sticky='')

def Npulse():
    edit1 = tk.Entry(width=10)
    edit1.grid(row=1, column=6, padx=10, pady=10, sticky='e')
    button1 = tk.Button(text="Frequency_Hz")
    button1['command'] = button1
    button1.grid(row=1, column=7, padx=0, pady=0, sticky='w')

    edit2 = tk.Entry(width=10)
    edit2.grid(row=2, column=6, padx=10, pady=10, sticky='e')
    button2 = tk.Button(text="count")
    button2['command'] = button2
    button2.grid(row=2, column=7, padx=0, pady=0, sticky='w')

    def Npulse_button_all():
        """sweep setup button"""
        Npulse_input1 = float(edit1.get())
        Npulse_input2 = float(edit2.get())
        qp3.program_in()
        qp3.Npulse_setup(Npulse_input1, Npulse_input2)

    button3 = tk.Button(text="Npulse_setup")
    button3['command'] = Npulse_button_all
    button3.grid(row=5, column=7, padx=0, pady=0, sticky='')


def quit():
    """quit"""
    def quit_command():
        try:
            qp3.program_out()
            qp3.serial_close()
        finally:
            root.destroy()

    button2 = tk.Button(text="QUIT", command=quit_command)
    button2.grid(row=6, column=1, padx=0, pady=50, sticky='')


root.title("QP-3 setup Application")
root.geometry("1600x600")
root.grid()

qp3 = QP3.USB()
create_widgets()
allmode()
oscillator()
sweep()
Npulse()
quit()
aaaaaaaaaaaaaa
aaaaaaaaaaaaa
root.mainloop()

__author__ = 'RyunosukeT'
__date__ = '2016/12/13'
__version__ = '0.1'
