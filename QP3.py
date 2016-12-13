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
    USB通信を制御するクラス、自動テスト向き
    """

    def __init__(self):
        self.serialport = None  # QP-3と繋がるシリアルポート
        self.response = None  # QP-3からのレスポンス

    def serial_open(self, port_number):
        self.serialport = serial.Serial(port=port_number, baudrate=9600, bytesize=8, parity='N',
                                        stopbits=1, timeout=0.1)

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
        self.com(str('N0' + frequency + '\r'))
        self.com('T3\r')
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def sweep_setup(self, start_Hz, stop_Hz, sweep_time_sec, wave_mode):
        """スイープモードセットアップ・出力"""
        start = str(int(start_Hz * 10)).zfill(7)
        stop = str(int(stop_Hz * 10)).zfill(7)
        sweep_time = str(int(sweep_time_sec * 100)).zfill(5)
        self.com('S0' + start + '\r')
        self.com('S1' + stop + '\r')
        self.com('S2' + sweep_time + '\r')
        self.com('S3' + wave_mode + '\r')  # 0:三角、1:鋸歯、2:2周波数切り替え
        self.com('T1\r')
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def Npulse_setup(self, frequency_Hz, pulse_count):
        """Nパルスモードセットアップ・出力"""
        frequency = str(int(frequency_Hz * 10)).zfill(5)
        pulse_count = str(pulse_count.zfill(5))
        self.com('C0' + frequency +'\r')
        self.com('C1' + pulse_count +'\r')
        self.com('T2\r')
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def allmode_setup(self, high_V, low_V, AB_setup, output_mode):

        def voltage_setup(voltage_V):
            if voltage_V >= 0:
                setup_voltage = ('+' + str(int(voltage_V* 10)).zfill(3))
            else:
                setup_voltage = str(int(voltage_V * 10)).zfill(4)
            return setup_voltage

        self.com('G0' + voltage_setup(high_V) + '\r')
        self.com('G1' + voltage_setup(low_V) + '\r')
        self.com('G2' + str(AB_setup) + '\r')  # 0:A_B進み、1:B_A遅れ
        self.com('G3' + str(output_mode) + '\r')  # 0:可変電圧出力、1:セミオープンコレクタ出力


if __name__ == '__main__':  # コード作成時のテスト用
    response = 0
    print(response)
    start_Hz = 100
    start = str(start_Hz * 10).zfill(7)
    print(start)
    high_V = -10
    high = str(high_V * 10)
    print(high.zfill(4))
    test = USB()
    test.serial_open('/dev/tty.usbserial-A501YZDP')
    test.program_in()
    test.allmode_setup(+10, -10, 0, 0)
    test.oscillator(0.01)
    test.program_out()



__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'
