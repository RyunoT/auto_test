import serial
import time
import TDP39
import QP3

QP3.serial_open('/dev/tty.usbserial-A501YZDP')
TDP39.serial_open('/dev/tty.usbserial-FTZ2FBLI')
TDP39.data_stop()

QP3.program_in()

QP3.oscillator('001000000')
TDP39.read()
data1 = TDP39.res

QP3.oscillator('200000000')
TDP39.read()
data2 = TDP39.res

QP3.program_out()

QP3.serial_close()
TDP39.serial_close()

print(data1.decode('utf-8'))
print(data2.decode('utf-8'))
