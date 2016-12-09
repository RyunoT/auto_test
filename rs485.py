import serial
import serial.rs485
import time
import binascii as ba

ser = serial.Serial('/dev/tty.usbserial-00001014', baudrate=9600, timeout=1,
                    bytesize=8, stopbits=1)
#ser.rs485_mode = serial.rs485.RS485Settings()
print(ser.readline())
ser.write(b'\x0500PI\x0d\x0a')
print(ser.readline())
time.sleep(0.1)
print(ser.readline())

ser.close()

#print(b'^E')
#print(ba.b2a_hex(b'\x0500PIF9\r\n'))
#print(ba.a2b_hex(b'053030504946390d0a'))

