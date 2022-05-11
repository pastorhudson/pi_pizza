import urllib.request
import json
import time
import configparser
import RPi.GPIO as GPIO
from pathlib import Path

p = Path('/home/pi/pi_pizza/config.ini')
p = Path('./config.ini')
config = configparser.ConfigParser()
config.read(p.absolute())


def get_orders(url, store_name=None):
    order_url = url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    req = urllib.request.Request(url=order_url, headers=headers)
    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
    try:
        
        for store in data['stores']:
        print(store)
            if store['store_name'] == store_name:
                print(f'store {data}')
                return store['has_unconfirmed_orders']
    except Exception as e:
        print(f'exception {data}')
        return data['has_unconfirmed_orders']


def set_gpio(status):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) # tell the Pi what headers to use
    GPIO.setup(int(config['DEFAULT']['PIN']), GPIO.OUT) # tell the Pi this pin is an output

    # there are unread emails, turn light on
    GPIO.output(int(config['DEFAULT']['PIN']), status)


if __name__ == '__main__':

    while True:
        try:
            if get_orders(config['DEFAULT']['URL'], config['DEFAULT']['STORE_NAME']):
                print("set pin TRUE")
                set_gpio(True)
            else:
                print("set pin FALSE")
                set_gpio(False)
            time.sleep(int(config['DEFAULT']['SECONDS']))
        except Exception as e:
            print(e)
            pass
