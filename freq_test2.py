import serial
import time
import TDP39
import QP3
import sys

data_list = []
numbers = input('Enter range (separate with commas): ')
test_freq = numbers


def TDP_mode(mode):
    TDP39.program_in()
    TDP39.koushin_time('0.1')
    TDP39.pulse_mode(mode)
    TDP39.program_out()
    TDP39.data_stop()

    global test_freq
#    test_freq = '100000000'
    QP3.oscillator(test_freq)
    TDP39.read()
    data_list.append(TDP39.res.decode('utf-8'))


QP3.serial_open('/dev/tty.usbserial-A501YZDP')
TDP39.serial_open('/dev/tty.usbserial-FTZ2FBLI')
TDP39.data_stop()

QP3.program_in()

QP3.oscillator_AB_setup()
TDP_mode('0')

QP3.oscillator_AB_setup()
TDP_mode('1')
QP3.oscillator_BA_setup()
TDP_mode('1')

QP3.oscillator_AB_setup()
TDP_mode('2')
QP3.oscillator_BA_setup()
TDP_mode('2')

QP3.program_out()

QP3.serial_close()
TDP39.serial_close()

for x in data_list:
    print(x)

'''import pandas as pd

df = pd.Series(data_list)
df.to_csv('freq_test2.csv')
'''