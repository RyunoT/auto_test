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

    def float_setting(self, x):
        """floatを小数点下5桁に揃える関数"""
        if x < 10:
            return str('%.5f' % x)
        elif x > 99999:
            return str(int(x))
        else:
            return str(float(x))

    def basic_setup(self, input_rate_Hz, display_rate_Hz, display_refresh_sec,
                    point_position, moving_avg, display_dynamic, output):

        input_rate = self.float_setting(input_rate_Hz)
        display_rate = self.float_setting(display_rate_Hz)

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

    def comparator_setup(self, high_Hz, low_Hz, high_co, high_V,
                         low_co, low_V, sync):
        high = self.float_setting(high_Hz)
        low = self.float_setting(low_Hz)
        combo1 = {'≤': str(0), '≥': str(1)}
        combo2 = {'+V': str(0), '-V': str(1)}
        combo3 = {'Display': str(0), 'Analog Out': str(1)}

        self.write_config(20, combo1[high_co] + combo2[high_V])
        self.write_config(21, high)
        self.write_config(23, combo1[low_co] + combo2[low_V])
        self.write_config(24, low)
        self.write_config(26, combo3[sync])

    def mode_setup(self, divide, pulse, f_or_T, hold, chattering):

        _divide = str(int(divide)).zfill(3)

        if pulse == 'Single':
            pulse = 0
        elif pulse == 'UP/DOWN':
            pulse = 1
        elif pulse == 'A/B':
            pulse = 2
        if f_or_T == 'Frequency':
            f_or_T = 0
        elif f_or_T == 'Period':
            f_or_T = 1
        if hold == 'Data':
            hold = 0
        elif hold == 'Peak':
            hold = 1
        elif hold == 'Valley':
            hold = 2

        self.write_config(31, _divide)
        self.write_config(30, pulse)
        self.write_config(32, f_or_T)
        self.write_config(33, hold)
        self.write_config(34, int(chattering))

    def dual_setup(self, input_rate_Hz, display_rate_Hz, point_position):
        input_rate = self.float_setting(input_rate_Hz)
        display_rate = self.float_setting(display_rate_Hz)

        if point_position == 'Auto':
            point_position = 0

        self.write_config(40, input_rate)
        self.write_config(41, display_rate)
        self.write_config(42, int(point_position))



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
    c = RS232C()
    print(c.float_setting(100000))

"""    b = RS232C()
    b.serial_open('/dev/tty.usbserial-FTZ2FBLI')
    b.com('S')
    b.program_in()
    b.basic_setup(1, 1, 0, 1, 1, 0, 0)
    b.program_out()
    b.serial_close()
"""
"""    a = RS485('00')
    a.serial_open('/dev/tty.usbserial-00001014')
    a.read_only_number()
    a.serial_close()
"""

__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'
