"""
'subscribe.py'
==========================
Subscribes to an Adafruit IO Feed

Author(s): Brent Rubell, Todd Treece for Adafruit Industries
"""
import Adafruit_DHT
import socket
# Import standard python modules.
import sys
import RPi.GPIO as GPIO
import os
# This example uses the MQTTClient instead of the REST client
from Adafruit_IO import MQTTClient


def sensordata():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, 27)
    return (humidity, temperature)


# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'aio_hHUb12rSJYjGPokRYUCUHYz1WTaZ'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'BaTuan'

# Set to the ID of the feed to subscribe to for updates.
FEED_ID = 'den'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, 0)


# Define callback functions which will be called when certain events happen.
def connected(client):
    """Connected function will be called when the client is connected to
    Adafruit IO.This is a good place to subscribe to feed changes.  The client
    parameter passed to this function is the Adafruit IO MQTT client so you
    can make calls against it easily.
    """
    # Subscribe to changes on a feed named Counter.
    print('Subscribing to Feed {0}'.format(FEED_ID))
    client.subscribe(FEED_ID)
    print('Waiting for feed data...')


def disconnected(client):
    """Disconnected function will be called when the client disconnects."""
    sys.exit(1)


def message(client, feed_id, payload):
    """Message function will be called when a subscribed feed has a new value.
    The feed_id parameter identifies the feed, and the payload parameter has
    the new value.
    """
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if str(payload) == "1":
        GPIO.output(5, 1)
    if str(payload) == "0":
        GPIO.output(5, 0)
    if str(payload) == "2":
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('192.168.43.36', 10001)
        i = 1
        try:
            while (i):
                i = i-1
                h, t = sensordata()
                message = str(h) + ',' + str(t)
                # send data
                print('sending '"%s" % message)
                sent = sock.sendto(message.encode(), server_address)
        finally:
            print('closing socket')
            sock.close()


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

# Connect to the Adafruit IO server.
client.connect()

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_blocking()
