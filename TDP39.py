#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
TDP-39XXのUSB通信制御用プログラムです
"""
# Date: ${YEAR}/${MONTH}/${DAY}
# Filename: ${NAME}


import serial
import time



class RS232C(object):
    """
    RS232C通信を制御するクラス、自動テスト向き
    """

    def __init__(self):
        self.serialport = None  # TDP39XXとつながるシリアルポート、オブジェクト
        self.response = None

    def serial_open(self, port_number):
        self.serialport = serial.Serial(port=port_number, baudrate=2400, bytesize=8,
                                        parity='N', stopbits=1, timeout=1)

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

    def read_only_number(self):
        """表示器の数字のみを読み込む、具体的には\r\n（CRLF）を削除する"""
        self.com('O')
        self.response = self.response[:8]

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
        """更新時間をセットアップ"""
        command = str('WP04,' + refresh_time + '\r')
        self.com(command)

    def pulse_mode(self, mode):
        """モード選択は0or1or2"""
        command = str('WP30,' + mode + '\r')
        self.com(command)


class RS485(RS232C):
    """RS485通信を制御するクラス、RS232Cクラスを継承、serialportとresponseを標準装備"""

    def __init__(self, address):
        RS232C.__init__(self)
        self.address = address

    def serial_open(self, port_number):
        self.serialport = serial.Serial(port=port_number, baudrate=9600, bytesize=8,
                                        parity='N', stopbits=1, timeout=1)

    def com(self, command):
        """汎用コマンド制御"""
        all_command = ('\x05' + self.address + command + '\r\n')
        self.serialport.reset_input_buffer()
        self.serialport.write(all_command.encode('utf-8'))
        self.response = self.serialport.readlines()  # readline → readlinesに変更
        if __name__ == '__main__':  # コード作成時のテスト用
            print(self.response)

    def read_only_number(self):
        """表示器の数字のみを読み込む"""
        self.com('DQ')
        print(a.response[1][3:11])


if __name__ == '__main__':  # コード作成時のテスト用
    a = RS485('00')
    a.serial_open('/dev/tty.usbserial-00001014')
    a.read_only_number()
    a.serial_close()

"""    b = RS232C()
    b.serial_open('/dev/tty.usbserial-FTZ2FBLI')
    b.com('O')
    b.serial_close()
"""

__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'
