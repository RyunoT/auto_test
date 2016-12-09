import serial
import time

ser = None
res = None


def serial_open(port_number):
    global ser
    ser = serial.Serial(port=port_number, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=0.1, write_timeout=0.1)


def serial_close():
    ser.close()


def com(command):
    global res
    command = command.encode('utf-8')
    ser.reset_input_buffer()
    ser.write(command)
    res = ser.readline()
#    print(res)


def oscillator_AB_setup():
    com('G0+050\r')
    com('G1+000\r')
    com('G20\r')
    com('G30\r')


def oscillator_BA_setup():
    com('G0+050\r')
    com('G1+000\r')
    com('G21\r')
    com('G30\r')


def oscillator(f):
    command = str('N0' + f + '\r')
    com(command)
    command = 'T3\r'
    com(command)
    time.sleep(1)


def program_in():
    command = 'P\r'
    com(command)


def program_out():
    command = 'E\r'
    com(command)



