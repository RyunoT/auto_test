#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
teststandで実行するプログラム
一番下でポートだけを書き換えれば汎用的に使える
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
    tdp39_rs232c = TDP39.RS232C()  # クラス変数、なぜクラス変数なのか理由は（よくわから）ない
    qp3_usb = QP3.USB()  # クラス変数、なぜクラス変数なのか理由は（よくわから）ない

    def __init__(self):
        self.data_list = []
        self.test_frequency = input()  # 'Enter range' (separate with commas):とでも書きたいところ

    def TDP_input_mode_test(self, mode):
        """TDP39の入力モードを変更できる周波数テストのインスタンス"""
        Frequency_test.tdp39_rs232c.program_in()
        Frequency_test.tdp39_rs232c.refresh_time_setup('0.1')  # 更新時間を設定
        Frequency_test.tdp39_rs232c.pulse_mode(mode)  # [0, 1, 2] で入力モードを設定
        Frequency_test.tdp39_rs232c.program_out()
        Frequency_test.tdp39_rs232c.data_stop()

        Frequency_test.qp3_usb.oscillator(self.test_frequency)
        Frequency_test.tdp39_rs232c.read_only_number()
        self.data_list.append(Frequency_test.tdp39_rs232c.response.decode('utf-8'))  # 計測結果はdata_listに格納

    def main_test(self, TDP_port, QP3_port):
        """テストのメインプログラム、一番下で実行されているのはコイツ"""
        Frequency_test.qp3_usb.serial_open(QP3_port)
        Frequency_test.tdp39_rs232c.serial_open(TDP_port)
        Frequency_test.tdp39_rs232c.data_stop()

        Frequency_test.qp3_usb.program_in()

        Frequency_test.qp3_usb.oscillator_AB_setup()  # QP3をセットアップ
        self.TDP_input_mode_test('0')  # TDP39をテスト

        Frequency_test.qp3_usb.program_out()

        Frequency_test.qp3_usb.serial_close()
        Frequency_test.tdp39_rs232c.serial_close()

        print(self.data_list[0])  # data_listの0番目を出力


a = Frequency_test()  # メインプログラムの呼び出し
# windowsで変更 TAHARA1-PCではCOM6、TAHARA1-PCではCOM5
a.main_test('/dev/tty.usbserial-FTZ2FBLI', '/dev/tty.usbserial-A501YZDP')  # ポートだけ設定して実行


__author__ = 'RyunosukeT'
__date__ = '2016/12/9'
__version__ = '0.1'
