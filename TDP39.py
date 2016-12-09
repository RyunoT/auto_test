#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
TDP-39XXのUSB通信制御用プログラムです
"""
# Date: ${YEAR}/${MONTH}/${DAY}
# Filename: ${NAME}
__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'


import serial
import time


class RS232C(object):
    """
    RS232C通信を制御するクラス、自動テスト向き
    """
    serialport = None  # TDP39XXとつながるシリアルポート、オブジェクト
    response = None

    def serial_open(self, port_number):
        self.serialport = serial.Serial(port=port_number, baudrate=2400, bytesize=8,
                                        parity='N', stopbits=1, timeout=1, write_timeout=1)

    def serial_close(self):
        self.serialport.close()

    def com(self, command):
        """汎用コマンド制御"""
        command = command.encode('utf-8')
        self.serialport.reset_input_buffer()
        self.serialport.write(command)
        self.response = self.serialport.readline()
        if __name__ == '__main__':  # コード作成時のテスト用
            print(self.response)

    def read(self):
        self.com('O')
        self.response = self.response[:8]
        """
        変更しました、未テスト
        command = 'O'
        command = command.encode('utf-8')
        self.serialport.reset_input_buffer()
        self.serialport.write(command)
        self.response = self.serialport.read(8)
        if __name__ == '__main__':  # コード作成時のテスト用
            print(self.response)
        """

    def data_stop(self):
        """データ垂れ流しをストップ"""
        self.com('S')
        time.sleep(1)  # データストップのコマンドを送ってから応答時間が必要でしょ？

    def program_in(self):
        """Hello program mode"""
        self.com('P')

    def program_out(self):
        """Goodbye program mode"""
        self.com('E\r')

    def refresh_time_setup(self, refresh_time):
        """koushin_time"""
        command = str('WP04,' + refresh_time + '\r')
        self.com(command)

    def pulse_mode(self, mode):
        """モード選択は0or1or2"""
        command = str('WP30,' + mode + '\r')
        self.com(command)


if __name__ == '__main__':  # コード作成時のテスト用
    response = '9000000000000\r\n'
    print(response)
    response = response[:8]
    print(response)

