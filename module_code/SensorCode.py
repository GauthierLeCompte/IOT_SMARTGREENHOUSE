from network import LoRa
import socket
import time
import ubinascii

# from pysense import Pysense
from SI7006A20 import SI7006A20
from pycoproc_2 import Pycoproc

# initialize the PySense
print("accesed")
py = Pycoproc()
si = SI7006A20(py)
print("accesed")

# initialize LoRa
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRa region
# lora.region('EU868')

# set the LoRa join parameters
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('508BF33153F8E2B303E66AFDBF040953')
print("accesed")
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)


# wait until LoRa is joined
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print('Joined!')

# send sensor data every 30 seconds
while True:
    temperature = si.temperature()
    humidity = si.humidity()

    # format the sensor data
    data = '{};{}'.format(temperature, humidity)

    # send the sensor data
    s.send(data)

    print('Sent: {}'.format(data))

    # wait for 30 seconds
    time.sleep(30)