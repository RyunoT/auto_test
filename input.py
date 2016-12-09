import serial
import time

ser = serial.Serial('/dev/tty.usbserial-FTZ2FBLI', 2400, timeout=0.1)

ser.write(b'P')
print(ser.readline())

time.sleep(1)

ser.write(b'RV\r')
print(ser.readline())

time.sleep(1)

ser.write(b'RS\r')
print(ser.readline())

time.sleep(1)


ser.write(b'E\r')
print(ser.readline())



'''ser.write(b'S')
print(ser.readline())
time.sleep(1)

ser.write(b'T')
print(ser.readline())
time.sleep(1)

ser.write(b'WP20 1\r')
print(ser.readline())
time.sleep(1)

ser.write(b'WAE666\r')
print(ser.readline())
time.sleep(1)

ser.write(b'E\r')
print(ser.readline())
time.sleep(1)

ser.write(b'S')
print(ser.readline())
'''
ser.close()
