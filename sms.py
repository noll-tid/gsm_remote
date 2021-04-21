from machine import UART
from time import sleep

uart = UART(2,115200)
uart.init(115200,rx=16,tx=17,rxbuf=2048,txbuf=2048)

def cmd(command,wait):
    uart.write(command+'\n\r')
    sleep(wait)
    return uart.read(uart.any())

def init():
    cmd('AT', 0.2)
    cmd('ATE0', 0.2)
    cmd('AT+CMGF=1', 0.2)
    cmd('AT+CSCS="8859-1"', 0.2)
    cmd('AT+CNMI=0,0,0,0,0', 0.2)

def send(number,message):
    cmd('AT', 0.2)
    cmd('ATE0', 0.2)
    cmd('AT+CMGF=1', 0.2)
    cmd('AT+CMGS="'+str(number)+'"', 0.2)
    uart.write(message)
    sleep(0.2)
    uart.read(uart.any())
    uart.write("\u001A")
    sleep(0.2)
    uart.read(uart.any())

def read():
    cmd('AT', 0.2)
    cmd('ATE0', 0.2)
    cmd('AT+CMGF=1', 0.2)
    cmd('AT+CSCS="8859-1"', 0.2)
    return cmd('AT+CMGL="ALL"', 1.0)    

def check():
    messages = str(read()).split('+CMGL')
    lista = []
    for entry in messages:
        if entry.startswith(':'):
            obj = {}
            entry = entry.replace('"', '')
            parts = entry.split('\\r\\n')
            msgid, status, number, unk, date, time = parts[0].split(",")
            msgid = msgid.split(' ')[1]
            message = parts[1]
            command = 'AT+CMGD='+msgid
            cmd(command,0.5)
            obj['msgid'] = msgid
            obj['message'] = message
            obj['number'] = number
            lista.append(obj)
    return lista
