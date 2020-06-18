# -*- coding: utf-8 -*-

from time import sleep
import sys
import random
import cloud4rpi
#import ds18b20
import rpi
import RPi.GPIO as GPIO  # pylint: disable=F0401
import Adafruit_DHT
# Put your device token here. To get the token,
# sign up at https://cloud4rpi.io and create a device.

DEVICE_TOKEN = '4D8uTXJCvAPce1yi8NkZELA3a'

# Constants
LED_PIN = 5
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11
 
# Set GPIO sensor is connected to
gpio=27

# Change these values depending on your requirements.
DATA_SENDING_INTERVAL = 60  # secs
DIAG_SENDING_INTERVAL = 650  # secs
POLL_INTERVAL = 0.5  # 500 ms

LOCATIONS = [
    {'lat': 51.500741, 'lng': -0.124626},  # Big Ben, London, United Kingdom
    {'lat': 40.689323, 'lng': -74.044503}  # Statue of Liberty, New York, USA
]

# Configure GPIO library
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)


# Handler for the button or switch variable
def led_control(value=None):
    GPIO.output(LED_PIN, value)
    return GPIO.input(LED_PIN)

def temp(value=None):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

    return temperature

def humid(value=None):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)

    return humidity


def listen_for_events():
    # Write your own logic here
    result = random.randint(1, 5)
    if result == 1:
        return 'RING'

    if result == 5:
        return 'BOOM'

    return 'IDLE'


def get_location():
    return random.choice(LOCATIONS)


def sensor_not_connected():
    return 'Sensor not connected'


def main():
    # Load w1 modules
   ## ds18b20.init_w1()

    # Detect ds18b20 temperature sensors
   ## ds_sensors = ds18b20.DS18b20.find_all()

    # Put variable declarations here
    # Available types: 'bool', 'numeric', 'string', 'location'
    variables = {
        'Room Temp': {
            'type': 'numeric',# if ds_sensors else 'string',
            'bind': temp
        },
#	'Room humid': {
      #      'type': 'numeric',# if ds_sensors else 'string',
      #      'bind': humid
#	},
         'Outside humid': {
             'type': 'numeric',
             'bind': humid
         },
        'LED On': {
            'type': 'bool',
            'value': False,
            'bind': led_control
        },
        'CPU Temp': {
            'type': 'numeric',
            'bind': rpi.cpu_temp
        },
        'STATUS': {
            'type': 'string',
            'bind': listen_for_events
        },
        'Location': {
            'type': 'location',
            'bind': get_location
        }
    }

    diagnostics = {
        'CPU Temp': rpi.cpu_temp,
        'IP Address': rpi.ip_address,
        'Host': rpi.host_name,
        'Operating System': rpi.os_name,
        'Client Version:': cloud4rpi.__version__,
    }
    device = cloud4rpi.connect(DEVICE_TOKEN)

    # Use the following 'device' declaration
    # to enable the MQTT traffic encryption (TLS).
    #
    # tls = {
    #     'ca_certs': '/etc/ssl/certs/ca-certificates.crt'
    # }
    # device = cloud4rpi.connect(DEVICE_TOKEN, tls_config=tls)

    try:
        device.declare(variables)
        device.declare_diag(diagnostics)

        device.publish_config()

        # Adds a 1 second delay to ensure device variables are created
        sleep(1)

        data_timer = 0
        diag_timer = 0

        while True:
            if data_timer <= 0:
                device.publish_data()
                data_timer = DATA_SENDING_INTERVAL

            if diag_timer <= 0:
                device.publish_diag()
                diag_timer = DIAG_SENDING_INTERVAL

            sleep(POLL_INTERVAL)
            diag_timer -= POLL_INTERVAL
            data_timer -= POLL_INTERVAL

    except KeyboardInterrupt:
        cloud4rpi.log.info('Keyboard interrupt received. Stopping...')

    except Exception as e:
        error = cloud4rpi.get_error_message(e)
        cloud4rpi.log.exception("ERROR! %s %s", error, sys.exc_info()[0])

    finally:
        sys.exit(0)


if __name__ == '__main__':
    main()
