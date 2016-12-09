#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
teststand
"""
# Date: ${YEAR}/${MONTH}/${DAY}
# Filename: ${NAME}



import serial
import time
import TDP39
import QP3
import sys


data_list = []
numbers = input()  # Enter range (separate with commas):
test_freq = numbers


TDP39_RS232C = TDP39.RS232C()
QP3_USB = QP3.USB()


def TDP_mode(mode):
    TDP39_RS232C.program_in()
    TDP39_RS232C.refresh_time_setup('0.1')
    TDP39_RS232C.pulse_mode(mode)
    TDP39_RS232C.program_out()
    TDP39_RS232C.data_stop()

    global test_freq
#    test_freq = '100000000'
    QP3_USB.oscillator(test_freq)
    TDP39_RS232C.read()
    data_list.append(TDP39_RS232C.response.decode('utf-8'))


QP3_USB.serial_open('/dev/tty.usbserial-A501YZDP')  # windowsで変更 TAHARA1-PCではCOM6
TDP39_RS232C.serial_open('/dev/tty.usbserial-FTZ2FBLI')  # windowsで変更 TAHARA1-PCではCOM5
TDP39_RS232C.data_stop()

QP3_USB.program_in()

QP3_USB.oscillator_AB_setup()
TDP_mode('0')

'''ひとまず消去
QP3_USB.oscillator_AB_setup()
TDP_mode('1')
QP3_USB.oscillator_BA_setup()
TDP_mode('1')

QP3_USB.oscillator_AB_setup()
TDP_mode('2')
QP3_USB.oscillator_BA_setup()
TDP_mode('2')
'''

QP3_USB.program_out()

QP3_USB.serial_close()
TDP39_RS232C.serial_close()

a = data_list[0]
print(a)

#for x in data_list:
#    print(x)

__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'
