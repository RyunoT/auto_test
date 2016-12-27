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
        self.serialport = serial.Serial()  # TDP39XXとつながるシリアルポート、オブジェクト
        self.response = str()

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

    def read_config(self, number):
        """設定値読み込み"""
        self.com('RP' + str(number).zfill(2) + '\r')

    def write_config(self, number, str_value):
        """設定値書き込み"""
        self.com('WP' + str(number).zfill(2) + ','
                 + str(str_value) + '\r')

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

    def basic_setup(self, input_rate_Hz, display_rate_Hz, display_refresh_sec,
                    point_position, moving_avg, display_dynamic, output):

        def _float_setting(x):
            if x < 1:
                return '%.5f' % x
            else:
                return int(x)

        input_rate = _float_setting(input_rate_Hz)
        display_rate = _float_setting(display_rate_Hz)

        if point_position == 'Auto':
            point_position = 0
        if display_dynamic == 'OFF':
            display_dynamic = 0

        self.write_config(1, input_rate)
        self.write_config(2, display_rate)
        self.write_config(4, int(display_refresh_sec))
        self.write_config(3, int(point_position))
        self.write_config(5, int(moving_avg))
        self.write_config(6, int(display_dynamic))
        self.write_config(7, int(output))

    def comparator_setup(self, ):
        pass

    def

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
    b = RS232C()
    b.serial_open('/dev/tty.usbserial-FTZ2FBLI')
    b.com('S')
    b.program_in()
    b.basic_setup(1, 1, 0, 1, 1, 0, 0)
    b.program_out()
    b.serial_close()

"""    a = RS485('00')
    a.serial_open('/dev/tty.usbserial-00001014')
    a.read_only_number()
    a.serial_close()
"""

__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'
