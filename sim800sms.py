from machine import UART
uart = UART(1,115200)
uart.init(115200,rx=12,tx=14)
def send(number,message):
    uart.write("AT\r\n")
    uart.write("AT+CMGF=1\r\n")
    uart.write('AT+CMGS="'+str(number)+'"\n\r')
    uart.write(message)
    uart.write("\u001A")
