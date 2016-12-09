import serial
import time

ser = None
res = None


def serial_open(port_number):
    global ser
    ser = serial.Serial(port=port_number, baudrate=2400, bytesize=8, parity='N', stopbits=1, timeout=1, write_timeout=1)


def serial_close():
    ser.close()


def com(command):
    global res
    command = command.encode('utf-8')
    ser.reset_input_buffer()
    ser.write(command)
    res = ser.readline()
#    print(res)


def read():
    global res
    command = 'O'
    command = command.encode('utf-8')
    ser.reset_input_buffer()
    ser.write(command)
    res = ser.read(8)
#    print(res)


def data_stop():
    com('S')
    time.sleep(1)


def program_in():
    com('P')


def program_out():
    com('E\r')


def koushin_time(t):
    command = str('WP04,' + t + '\r')
    com(command)


def pulse_mode(mode):
    command = str('WP30,' + mode + '\r')
    com(command)
