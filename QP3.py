#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
QP-3(X)のUSB通信制御用プログラムです
"""
# Date: ${YEAR}/${MONTH}/${DAY}
# Filename: ${NAME}

import serial
import time


class USB(object):
    """
    USB通信を制御するクラス
    """

    def __init__(self):
        self.serialport = serial.Serial()  # QP-3と繋がるシリアルポート
        self.response = str()  # QP-3からのレスポンス

    def serial_open(self, port_number):
        self.serialport = serial.Serial(port=port_number, baudrate=9600, bytesize=8, parity='N',
                                        stopbits=1, timeout=0.1)
        self.serialport.read()
        self.serialport.reset_input_buffer()
        self.serialport.reset_output_buffer()

    def serial_close(self):
        self.serialport.close()

    def com(self, command):
        """汎用コマンド制御"""
        command = command.encode('utf-8')
        self.serialport.reset_input_buffer()  # レスポンスバッファをリセット、write直後のレスポンスを読みたいから
        self.serialport.write(command)
        self.response = self.serialport.readline()
        if __name__ == '__main__':  # コード作成時のテスト用
            print(self.response)

    def program_in(self):
        """Hello program mode"""
        self.com('P\r')

    def program_out(self):
        """Goodbye program mode"""
        self.com('E\r')

    def stop_QP3(self):
        """全モードで発振ストップ"""
        self.com('T0\r')

    def oscillator(self, frequency_Hz):
        """オシレータモードセットアップ・出力"""
        frequency = str(int(frequency_Hz * 1000)).zfill(9)
        self.stop_QP3()
        self.com(str('N0' + frequency + '\r'))
        self.com('T3\r')
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def sweep_setup(self, start_Hz, stop_Hz, sweep_time_sec, wave_mode):
        """スイープモードセットアップ・出力"""
        start = str(int(start_Hz * 10)).zfill(7)
        stop = str(int(stop_Hz * 10)).zfill(7)
        sweep_time = str(int(sweep_time_sec * 100)).zfill(5)
        wave_mode = str(int(wave_mode)).zfill(1)
        self.stop_QP3()
        self.com('S0' + start + '\r')
        self.com('S1' + stop + '\r')
        self.com('S2' + sweep_time + '\r')
        self.com('S3' + wave_mode + '\r')  # 0:三角、1:鋸歯、2:2周波数切り替え
        self.com('T1\r')
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def Npulse_setup(self, frequency_Hz, pulse_count):
        """Nパルスモードセットアップ・出力"""
        frequency = str(int(frequency_Hz * 10)).zfill(5)
        pulse_count = str(int(pulse_count)).zfill(5)
        self.stop_QP3()
        self.com('C0' + frequency +'\r')
        self.com('C1' + pulse_count +'\r')
        self.com('T2\r')
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def allmode_setup(self, high_V, low_V, AB_setup, output_mode):

        def voltage_setup(voltage_V):
            """出力電圧の設定値の符号（+, -）を書き込むための関数"""
            if voltage_V >= 0:
                setup_voltage = ('+' + str(int(voltage_V * 10)).zfill(3))
            else:
                setup_voltage = str(int(voltage_V * 10)).zfill(4)
            return setup_voltage

        AB_setup = str(int(AB_setup))
        output_mode = str(int(output_mode))
        self.com('G0' + voltage_setup(high_V) + '\r')
        self.com('G1' + voltage_setup(low_V) + '\r')
        self.com('G2' + AB_setup + '\r')  # 0:A_B進み、1:B_A遅れ
        self.com('G3' + output_mode + '\r')  # 0:可変電圧出力、1:セミオープンコレクタ出力


if __name__ == '__main__':  # コード作成時のテスト用
    test = USB()
    test.serial_open('/dev/tty.usbserial-A501YZDP')

    test.program_in()
    test.com('T3\r')
    test.com('R1\r')
    test.com('T1\r')
    test.com('R1\r')
    test.com('T2\r')
    test.com('R1\r')

    test.com('T3\r')

    test.program_out()

"""    print(type(test.serialport))
    test.program_in()
    test.allmode_setup(+10, -10, 0, 0)
    test.oscillator(0.01)
    test.program_out()
"""

__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'
