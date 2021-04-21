import time
import network
from machine import Pin, I2C, ADC
from writeoled import write
import sms
import ujson
net = network.WLAN(network.STA_IF)
p1 = Pin(21, Pin.OUT)
p2 = Pin(19, Pin.OUT)
p3 = Pin(18, Pin.OUT)
p4 = Pin(5, Pin.OUT)

write(['Waiting for', 'network...'])
time.sleep(3)
state = {}


def savea(stat):
    with open('state.json', 'w') as f:
        f.write(ujson.dumps(stat))
        f.close()


status = ujson.loads(str(open('state.json', 'r').read()))
if '1' in status.keys():
    state['1'] = status['1']
    if state['1'] == 'off':
        p1.value(0)
    elif state['1'] == 'on':
        p1.value(1)
else:
    state['1'] = 'off'
    savea(state)
if '1' in status.keys():
    state['2'] = status['2']
    if state['2'] == 'off':
        p2.value(0)
    elif state['2'] == 'on':
        p2.value(1)
else:
    state['2'] = 'off'
    savea(state)

write(['---------------', 'IP Address:', net.ifconfig()[0], '---------------'])
while True:
    a = "1: {0} 2: {1}".format(state['1'], state['2'])
    write(['Polling...', net.ifconfig()[0], a])
    lista = sms.check()
    if len(lista) >= 1:
        for entry in lista:
            number = entry['number']
            msgid = entry['msgid']
            message = entry['message']
            write([number, message, msgid])
            message = message.replace('\r', '').replace('\n', '')
            if message.lower() == "on 1":
                state['1'] = 'on'
                savea(state)
                p1.value(1)
                sms.send(number, "Turned on outlet 1")
            elif message.lower() == "off 1":
                state['1'] = 'off'
                savea(state)
                p1.value(0)
                sms.send(number, "Turned off outlet 1")
            elif message.lower() == "on 2":
                state['2'] = 'on'
                savea(state)
                p2.value(1)
                sms.send(number, "Turned on outlet 2")
            elif message.lower() == "off 2":
                state['2'] = 'off'
                savea(state)
                p2.value(0)
                sms.send(number, "Turned off outlet 2")
            elif message.lower() == "on 3":
                p3.value(1)
                sms.send(number, "Turning on 3")
            elif message.lower() == "off 3":
                p3.value(0)
                sms.send(number, "Turning off 3")
            elif message.lower() == "on 4":
                p4.value(1)
                sms.send(number, "Turning on 4")
            elif message.lower() == "off 4":
                p4.value(0)
                sms.send(number, "Turning off 4")
            elif message.lower() == "status":
                sms.send(number, "Outlet 1: {0}, Outlet 2: {1}".format(state['1'], state['2']))
            else:
                sms.send(number, "Error: "+message)
            command = 'AT+CMGD='+msgid
            sms.cmd(command, 0.5)
            time.sleep(1)
    else:
        write(['No new messages'])