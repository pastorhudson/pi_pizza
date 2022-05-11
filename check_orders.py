import urllib.request
import json
import time
import configparser
import RPi.GPIO as GPIO
from pathlib import Path
import logging

l = Path('./check_orders.log')

logging.basicConfig(handlers=[logging.FileHandler(filename=l.absolute(),
                                                 encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%F %A %T",
                    level=logging.INFO)


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
            if store['store_name'] == store_name:
                logging.info(store)
                return store['has_unconfirmed_orders']
    except Exception as e:
        logging.debug(f'exception {data}')
        return data['has_unconfirmed_orders']


def set_gpio(status):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) # tell the Pi what headers to use
    GPIO.setup(int(config['DEFAULT']['PIN']), GPIO.OUT) # tell the Pi this pin is an output

    # there are unconfirmed orders, turn light on
    GPIO.output(int(config['DEFAULT']['PIN']), status)


if __name__ == '__main__':
    print("Running & Output is stored in check_orders.log")
    while True:
        try:
            if get_orders(config['DEFAULT']['URL'], config['DEFAULT']['STORE_NAME']):
                logging.info("set pin TRUE")
                set_gpio(True)
            else:
                logging.info("set pin FALSE")
                set_gpio(False)
            time.sleep(int(config['DEFAULT']['SECONDS']))
        except Exception as e:
            logging.debug(f'exception {e}')

            pass
