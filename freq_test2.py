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

class Frequency_test(object):
    """
    周波数テスト
    """
    def __init__(self):
        self.data_list = []
        self.numbers = input()  # 'Enter range' (separate with commas):
        self.test_freq = self.numbers

    TDP39_RS232C = TDP39.RS232C()
    QP3_USB = QP3.USB()

    def TDP_mode(self, mode):
        TDP39_RS232C = Frequency_test.TDP39_RS232C
        QP3_USB = Frequency_test.QP3_USB

        TDP39_RS232C.program_in()
        TDP39_RS232C.refresh_time_setup('0.1')
        TDP39_RS232C.pulse_mode(mode)
        TDP39_RS232C.program_out()
        TDP39_RS232C.data_stop()

        QP3_USB.oscillator(self.test_freq)
        TDP39_RS232C.read()
        self.data_list.append(TDP39_RS232C.response.decode('utf-8'))

    def main_test(self):
        TDP39_RS232C = Frequency_test.TDP39_RS232C
        QP3_USB = Frequency_test.QP3_USB

        QP3_USB.serial_open('/dev/tty.usbserial-A501YZDP')  # windowsで変更 TAHARA1-PCではCOM6
        TDP39_RS232C.serial_open('/dev/tty.usbserial-FTZ2FBLI')  # windowsで変更 TAHARA1-PCではCOM5
        TDP39_RS232C.data_stop()

        QP3_USB.program_in()

        QP3_USB.oscillator_AB_setup()
        self.TDP_mode('0')

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

        a = self.data_list[0]
        print(a)

b = Frequency_test()
b.main_test()

        # for x in data_list:
    #    print(x)


__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'
