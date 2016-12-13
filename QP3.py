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
        """発振ストップ"""
        self.com('T0\r')

    def oscillator_ABorBA_setup(self, AB_BA):
        """オシレータモードAB相/BA相セットアップ選択、ABなら0、BAなら1"""
        self.com('G0+050\r')  #ハイレベル電圧
        self.com('G1+000\r')  #ローレベル電圧
        self.com('G2' + AB_BA + '\r')
        self.com('G30\r')

    def oscillator_AB_setup(self):
        """オシレータモードAB相セットアップ、freq_testの関係で存在するムダ"""
        self.oscillator_ABorBA_setup('0')

    def oscillator_BA_setup(self):
        """オシレータモードBA相セットアップ、freq_testの関係で存在するムダ"""
        self.oscillator_ABorBA_setup('1')

    def oscillator(self, frequency):
        """オシレータモード出力"""
        command = str('N0' + frequency + '\r')
        self.com(command)
        self.com('T3\r')
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def sweep_setup(self, start_Hz, stop_Hz, sweep_time_sec, wave_mode):
        """スイープモードセットアップ"""
        start = str(start_Hz * 10)
        stop = str(stop_Hz * 10)
        sweep_time = str(sweep_time_sec * 100)
        self.com('S0' + start + '\r')
        self.com('S1' + stop + '\r')
        self.com('S2' + sweep_time + '\r')
        self.com('S3' + wave_mode + '\r')  # 0:三角、1:鋸歯、2:2周波数切り替え

    def sweep(self):
        """スイープモード出力"""
        self.com('T1\r')
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def Npulse_setup(self, frequency_Hz, pulse_count):
        """Nパルスモードセットアップ"""
        frequency = str(frequency_Hz * 10)
        self.com('C0' + frequency +'\r')
        self.com('C1' + pulse_count +'\r')

    def Npulse(self):
        """スイープモード出力"""
        self.com('T2\r')
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def allmode_setup(self, high_V, low_V, A_B, output_mode):
        high = str(high_V * 10)
        low = str(low_V * 10)
        self.com('G0' + high + '\r')
        self.com('G1' + low + '\r')
        self.com('G2' + A_B + '\r')  # 0:A_B進み、1:B_A遅れ
        self.com('G3' + output_mode + '\r')  # 0:可変電圧出力、1:セミオープンコレクタ出力


if __name__ == '__main__':  # コード作成時のテスト用
    response = 0
    print(response)

__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'
