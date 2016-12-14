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
        self.quit()

    def create_widgets(self):
        # ラベル
        #self.label = tk.Label(self, text='シリアルポート')
        #self.label.grid(row=0, column=0, padx=2, pady=10, sticky='')

        # エントリー
        self.editbox = tk.Entry()
        self.editbox.grid(row=0, column=0, padx=20, pady=10, sticky='nw')

        # ボタン
        self.button1 = tk.Button(self, text='シリアルポート接続')
        self.button1['command'] = self.ser
        self.button1.grid(row=0, column=1, columnspan=2, padx=120, pady=10, sticky='ne')

    def ser(self):
        self.edit_input = self.editbox.get()
        print(self.edit_input)
        self.qp3.serial_open(self.edit_input)
        self.qp3.program_in()
        time.sleep(5)
        self.qp3.program_out()

    def quit(self):
        self.button2 = tk.Button(self, text="QUIT", command=root.destroy)
        self.button2.grid(row=1, column=0, padx=20, pady=10)

root = tk.Tk()
app = Application(master=root)
app.mainloop()


__author__ = 'RyunosukeT'
__date__ = '2016/12/13'
__version__ = '0.1'
