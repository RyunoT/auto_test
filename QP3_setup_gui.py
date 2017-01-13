# -*- coding:utf-8 -*-
"""
QP3XをセットアップするGUIを備えたアプリケーションです
"""
# Date: 2016/12/13
# Filename: qp3_setup_gui

import sys
import tkinter as tk
import tkinter.messagebox as tkmsg
import tkinter.filedialog as tkfd
import QP3
import time
import csv
import shutil
import os

config_dict = {}


class Entry_Label_Button(object):
    """left Entry right Label, and bottom Button"""
    def __init__(self, column, row_count, label_text, button_text, button_select):
        self.qp3 = QP3.USB()
        self.column = column
        self.row_count = row_count
        self.label_text = label_text
        self.button_text = button_text
        self.button_select = button_select
        self.entry_list = [tk.Entry(width=10)]*self.row_count

    def setting_entry(self):
        for row in range(self.row_count):
            self.entry_list[row] = tk.Entry(width=10)
            self.entry_list[row].grid(row=row+1, column=self.column, padx=10, pady=10, sticky='e')

    def setting_label(self):
        label_list = [tk.Label]*self.row_count
        for row in range(self.row_count):
            label_list[row] = tk.Label(text=self.label_text[row])
            label_list[row].grid(row=row+1, column=self.column+1, padx=0, pady=0, sticky='w')

    def setting_button(self, button_select):
        entry_text = [float] * self.row_count
        row_count = self.row_count
        entry_list = self.entry_list

        def button_all():
            for row in range(row_count):
                entry_text[row] = float(entry_list[row].get())
            qp3.program_in()
            if button_select == 0:
                qp3.allmode_setup(*tuple(entry_text))
            elif button_select == 1:
                qp3.oscillator(*tuple(entry_text))
            elif button_select == 2:
                qp3.sweep_setup(*tuple(entry_text))
            elif button_select == 3:
                qp3.Npulse_setup(*tuple(entry_text))
            else:
                pass

        button = tk.Button(text=self.button_text)
        button['command'] = button_all
        button.grid(row=5, column=self.column+1, padx=0, pady=0, sticky='')

    def setting_ELB(self):
        """Entry Label Button"""
        self.setting_entry()
        self.setting_label()
        self.setting_button(self.button_select)

    def import_entry(self, key_list):
        """Import csv to entry box"""
        for i in range(len(self.entry_list)):
            self.entry_list[i].delete(0)
            self.entry_list[i].insert(0, config_dict[key_list[i]])  # config_dict is global


def connect_qp3x():
    entry = tk.Entry(width=20)
    entry.grid(row=0, column=0, padx=10, pady=50, sticky='')

    def ser():
        """serial open"""
        entry_input = entry.get()
        try:
            qp3.serial_open(entry_input)
            qp3.program_in()
            time.sleep(1)
            qp3.program_in()  # First QP3X connection is not respond sometimes
            if qp3.response == b'OK\r\x00':
                tkmsg.showinfo('Connect', 'Welcome to QP-3X')
                qp3.all_read_config()

                global config_dict

                with open("QP3X_config.csv", "r") as f:
                    global config_dict
                    config_dict = dict(csv.reader(f))

                config_dict['High(V*10)'] = int(config_dict['High(V*10)']) / 10
                config_dict['Low(V*10)'] = int(config_dict['Low(V*10)']) / 10
                config_dict['Oscillator(Hz*1000)'] = int(config_dict['Oscillator(Hz*1000)']) / 1000
                config_dict['Start(Hz*10)'] = int(config_dict['Start(Hz*10)']) / 10
                config_dict['Stop(Hz*10)'] = int(config_dict['Stop(Hz*10)']) / 10
                config_dict['Sweep time(sec*100)'] = int(config_dict['Sweep time(sec*100)']) / 100
                config_dict['Frequency(Hz*10)'] = int(config_dict['Frequency(Hz*10)']) / 10
                import_config_to_app()

            else:
                pass
        except Exception:
            tkmsg.showinfo('Error', 'Port Number Error!!')

    button = tk.Button(text='Connect QP-3X')
    button['command'] = ser
    button.grid(row=0, column=1, padx=0, pady=0, sticky='')


def quit():
    def quit_command():
        try:
            qp3.all_read_config()
            qp3.program_out()
            qp3.serial_close()
        except:
            pass
        root.destroy()

    button = tk.Button(text="Disconnect and Quit app", command=quit_command)
    button.grid(row=6, column=1, padx=0, pady=50, sticky='')

def csv_save():
    """csv saving button"""
    button = tk.Button(text='Making CSV file')

    def dialog():
        qp3.all_read_config()
        file_name = tkfd.asksaveasfilename(filetypes=[('CSV Files', '*.csv')], defaultextension='csv')
        print(file_name)
        shutil.copyfile(src='QP3X_config.csv', dst=file_name)

    button['command'] = dialog
    button.grid(row=0, column=6, padx=0, pady=0, sticky='')


# main code begin
root = tk.Tk()
root.title("QP-3X setup Application")
root.geometry("1600x600")
root.grid()
qp3 = QP3.USB()

# serial connect GUI
connect_qp3x()

# output setting GUI
output_label = ['High(V)\r[-12.0 ~ +12.0]',
                'Low(V)\r[-12.0 ~ +12.0]',
                'AB mode\r[0:A-B, 1:B-A]',
                'Output\r[0=Var.V, 1=Semi Open]']
output_setup = Entry_Label_Button(column=0, row_count=4, label_text=output_label,
                                  button_text='Output setting', button_select=0)
output_setup.setting_ELB()

# oscillator mode GUI
oscillator_label = ['Oscillator(Hz)\r[0.001 ~ 600000]']
oscillator_setup = Entry_Label_Button(column=2, row_count=1, label_text=oscillator_label,
                                      button_text='Oscillator mode', button_select=1)
oscillator_setup.setting_ELB()

# sweep mode GUI
sweep_label = ['Start(Hz)\r[0.1 ~ 200000]',
               'Stop(Hz)\r[0.1 ~ 200000]',
               'Sweep time(sec)\r[0.01 ~ 999.99]',
               'Wave mode\r[0=Triangle,\r1=Saw, 2=Square]']
sweep_setup = Entry_Label_Button(column=4, row_count=4, label_text=sweep_label,
                                 button_text='Sweep mode', button_select=2)
sweep_setup.setting_ELB()

# Npulse mode GUI
npulse_label = ['Frequency(Hz)\r[0.1 ~ 3000]',
                'Pulse count\r[1 ~ 60000]']
npulse_setup = Entry_Label_Button(column=6, row_count=2, label_text=npulse_label,
                                  button_text='Npulse mode', button_select=3)
npulse_setup.setting_ELB()

# quit button GUI
quit()

# csv button GUI
csv_save()


# import all Entry
def import_config_to_app():
    a = ['High(V*10)', 'Low(V*10)', 'AB mode', 'Output']
    b = ['Oscillator(Hz*1000)']
    c = ['Start(Hz*10)', 'Stop(Hz*10)', 'Sweep time(sec*10)', 'Wave mode']
    d = ['Frequency(Hz*10)', 'Pulse count']
    output_setup.import_entry(key_list=a)
    oscillator_setup.import_entry(key_list=b)
    sweep_setup.import_entry(key_list=c)
    npulse_setup.import_entry(key_list=d)

root.mainloop()

__author__ = 'RyunosukeT'
__date__ = '2016/12/16'
__version__ = '0.2'
