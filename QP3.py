#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
QP-3(X)のUSB通信制御用プログラムです
"""
# Date: ${YEAR}/${MONTH}/${DAY}
# Filename: ${NAME}
__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'

import serial
import time


class USB:
    """
    USB通信を制御するクラス、自動テスト向き
    """

    serialport = None  # QP-3と繋がるシリアルポート、オブジェクト
    response = None  # QP-3からのレスポンス

    def serial_open(self, port_number):
        self.serialport = serial.Serial(port=port_number, baudrate=9600, bytesize=8, parity='N',
                                        stopbits=1, timeout=0.1, write_timeout=0.1)

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

    def oscillator_ABorBA_setup(self, AB_BA):
        """オシレータモードAB相/BA相セットアップ選択、0または1"""
        AB_BA = AB_BA.encode('utf-8')  # ABなら0、BAなら1
        self.com('G0+050\r')
        self.com('G1+000\r')
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
        command = 'T3\r'
        self.com(command)
        time.sleep(1)  # ハードの動作時間があるので余裕を持たせる

    def program_in(self):
        """Hello program mode"""
        command = 'P\r'
        self.com(command)

    def program_out(self):
        """Goodbye program mode"""
        command = 'E\r'
        self.com(command)


