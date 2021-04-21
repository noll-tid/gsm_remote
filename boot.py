import esp
import network
import webrepl
import time
from writeoled import write

esp.osdebug(None)
import uos, machine
import gc
gc.collect()
write(['Starting'])
import sms
sms.init()
net = network.WLAN(network.STA_IF)
net.active(True)
net.active()
net.connect('Robins crib','88888888')
time.sleep(2)
write([net.ifconfig()[0]])
webrepl.start()
#import webrepl_setup