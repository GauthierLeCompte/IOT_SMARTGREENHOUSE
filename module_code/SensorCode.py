from network import LoRa
from network import WLAN
import socket
import time
import ubinascii
import machine
import pycom
from crypto import AES
import crypto
from network import LTE



from pycoproc_2 import Pycoproc
from SI7006A20 import SI7006A20
from LIS2HH12 import LIS2HH12
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE


key = b'sF2t@L8q9!yP$azx'

    # initialize the PySense
py = Pycoproc()
si = SI7006A20(py)
lt = LTR329ALS01(py)

# initialize LoRa
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRa join parameters
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('508BF33153F8E2B303E66AFDBF040953')
# backlog for data percistency
backlog = []

# data percistency, load the backlog
def setup_data():
    with open('backlog.txt', 'r') as file:
        global backlog
        backlog = file.readlines()
        backlog = [line.strip() for line in backlog]
        
def make_connection():
    # try to make a connection 
    lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
    timeout = 15
    # wait until LoRa is joined
    while not lora.has_joined():
        time.sleep(2.5)
        print('Not yet joined...')
        timeout -= 2.5
        if timeout<0:
            return False
    print("Joined")
    return True
        
def gather_data():
    # Gather data
    temperature = si.temperature()*0.75
    humidity = si.humidity()
    light = lt.light()
    
    # format the sensor data
    data2 = str(temperature) + "-" + str(humidity) + "-" + str(light)
    # encrypt the data
    iv = crypto.getrandbits(128)
    cipher = AES(key, AES.MODE_CFB, iv)
    data2 = iv+cipher.encrypt(data2)
    x = data2
    
    # Encode the encrypted data as hexadecimal
    encoded_data = ubinascii.hexlify(data2).decode("utf-8")
    return encoded_data
    # print(x)
    # return x

def main(retryThis=0):
    if(retryThis ==0):
        print("first try")
    else:
        print("tries to go:"+str(retryThis))
    # Try to make a connectio
    global backlog
    connected = make_connection()
    # If the connection is not made at previous try
    if retryThis>0:
        retryThis-=1
        # if still not connected
        if not connected:
            # try again maximum x times
            if retryThis > 0:
                main(retryThis)
        # if connected write the full backlog
        else:
            while backlog!=[]:
                send_data(backlog[0])
                backlog.pop(0)
    # If this is the first try
    else:
        # gather the data
        data2 = gather_data()
        backlog.append(data2)
        # if not connected try again
        if not connected:
            main(1)
        # if connected
        else:
            # write the full backlog
            while backlog!=[]:
                send_data(backlog[0])

                backlog.pop(0)

            
def send_data(data2):
    # Send data and wait long enough to really send it
    s.send(data2)
    
    # msg = ubinascii.unhexlify(data2.encode("utf-8"))
    # cipher = AES(key, AES.MODE_CFB, msg[:16])
    # original = cipher.decrypt(msg[16:])
    time.sleep(5)
    
def deepsleep():
    # Implement deepsleep
    # Write backlog for percitency through deepsleep
    print("backlog: ")
    print(backlog)
    with open('backlog.txt', 'w') as file:
        file.write('\n'.join(backlog))
    # close everything so a signall doesn't wake the deepsleep
    lte = LTE()
    pycom.heartbeat(False)
    wlan = WLAN()
    wlan.deinit()
    pycom.rgbled(0x00FF00)
    time.sleep(1)
    lte.deinit(detach=False, reset=False)
    # sleep 30 sec
    machine.deepsleep(30*1000)
    
# main loop
while True:
    setup_data()
    main()
    deepsleep()
    
