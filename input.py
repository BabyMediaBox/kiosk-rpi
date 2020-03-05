import os
import sys
import json
import time
import serial
import requests

import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

if not os.path.exists('config.json'):
    print('Missing config.json')
    sys.exit()

readInput = "serial"
if len(sys.argv) > 1:
    if sys.argv[1] == "cli":
        readInput = "cli"


def handle_button(current_pin, pin, btn):
    if current_pin == pin:
        button_url = serverUri + '/button/' + btn
        try:
            result = requests.post(url=button_url)
            print('send request to', button_url, result.status_code, result.content)
        except:
            print('error sending request to ', button_url)
            print('error', sys.exc_info()[0])
try:
    with open('config.json') as cfgFile:
        Config = json.load(cfgFile)
        serverUri = Config['server']

        for pinKey in Config['pinToButtonMap']:
            GPIO.setup(int(pinKey), GPIO.IN, pull_up_down=GPIO.PUD_UP)

        if readInput == "serial":
            ser = serial.Serial(Config['serialDevice'], int(Config['serialPort']), timeout=0.5)

        while True:
            pin = 0
            if readInput == "serial":
                for pinKey in Config['pinToButtonMap']:
                    button_state = GPIO.input(int(pinKey))
                    if button_state == False:
                        pin = int(pinKey)
                        time.sleep(0.2)
            elif readInput == "cli":
                text = input("Action: ")
                pin = int(text)

            for pinKey in Config['pinToButtonMap']:
                handle_button(pin, int(pinKey), Config['pinToButtonMap'][pinKey])

except:
    GPIO.cleanup()

