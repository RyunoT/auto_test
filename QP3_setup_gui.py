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


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("QP-3 setup Application")
        self.master.geometry("800x600")
        self.grid()

        self.qp3 = QP3.USB()
        self.create_widgets()
        self.allmode()
        self.quit()

    def create_widgets(self):
        # ラベル
        #self.label = tk.Label(self, text='シリアルポート')
        #self.label.grid(row=0, column=0, padx=2, pady=10, sticky='')

        # エントリー
        self.editbox = tk.Entry(width=20)
        self.editbox.grid(row=0, column=0, padx=20, pady=10, sticky='nw')

        # ボタン
        self.button1 = tk.Button(self, text='シリアルポート接続')
        self.button1['command'] = self.ser
        self.button1.grid(row=0, column=1, padx=20, pady=10, sticky='ne')

    def ser(self):
        """serial open"""
        self.edit_input = self.editbox.get()
        print(self.edit_input)

        self.qp3.serial_open(self.edit_input)
        """
        self.qp3.program_in()
        time.sleep(5)
        self.qp3.program_out()
        """

    def allmode(self):
        """QP3 allmode setup"""
        self.allmode_edit1 = tk.Entry()
        self.allmode_edit1.grid(row=1, column=0, padx=20, pady=10, sticky='nw')
        self.allmode_button1 = tk.Button(self, text="High_V")
        self.allmode_button1['command'] = self.allmode_button1
        self.allmode_button1.grid(row=1, column=1, padx=20, pady=10, sticky='ne')

        self.allmode_edit2 = tk.Entry()
        self.allmode_edit2.grid(row=2, column=0, padx=20, pady=10, sticky='nw')
        self.allmode_button2 = tk.Button(self, text="High_V")
        self.allmode_button2['command'] = self.allmode_button2
        self.allmode_button2.grid(row=2, column=1, columnspan=2, padx=20, pady=10, sticky='ne')

        self.allmode_edit3 = tk.Entry()
        self.allmode_edit3.grid(row=3, column=0, padx=20, pady=10, sticky='nw')
        self.allmode_button3 = tk.Button(self, text="High_V")
        self.allmode_button3['command'] = self.allmode_button1
        self.allmode_button3.grid(row=3, column=1, columnspan=2, padx=20, pady=10, sticky='ne')

        self.allmode_edit4 = tk.Entry()
        self.allmode_edit4.grid(row=4, column=0, padx=20, pady=10, sticky='nw')
        self.allmode_button4 = tk.Button(self, text="AB")
        self.allmode_button4['command'] = self.allmode_button1
        self.allmode_button4.grid(row=4, column=1, columnspan=2, padx=20, pady=10, sticky='ne')

        self.allmode_button5 = tk.Button(self, text="Output_mode")
        self.allmode_button5['command'] = self.allmode_button_all
        self.allmode_button5.grid(row=5, column=1, columnspan=2, padx=20, pady=10, sticky='ne')


    def allmode_button_all(self):
        """allmode setup button"""
        self.allmode_input1 = float(self.allmode_edit1.get())
        self.allmode_input2 = float(self.allmode_edit2.get())
        self.allmode_input3 = float(self.allmode_edit3.get())
        self.allmode_input4 = float(self.allmode_edit4.get())
        self.qp3.program_in()
        self.qp3.allmode_setup(float(self.allmode_input1), float(self.allmode_input2),
                               float(self.allmode_input3), float(self.allmode_input4))
        self.qp3.program_out()
        self.qp3.serial_close()

    def quit(self):
        """quit"""
        self.button2 = tk.Button(self, text="QUIT", command=root.destroy)
        self.button2.grid(row=6, column=1, columnspan=2, padx=120, pady=10, sticky='ne')

root = tk.Tk()
app = Application(master=root)
app.mainloop()


__author__ = 'RyunosukeT'
__date__ = '2016/12/13'
__version__ = '0.1'
