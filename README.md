# pi_pizza
Checks api to see if there is an unconfirmed order and turns on a light if there is.

## Setup

### Download The Code:
Form the home directory on the pi

`git clone https://github.com/pastorhudson/pi_pizza.git`

### Edit the config.ini

```ini
[DEFAULT]
# The PIN to toggle
PIN = 14
# How Many Seconds to Wait between Checking Email
SECONDS = 10
# URL To Check
URL = 'https://redacted/wp-json/hp/stores-info'
# Store Name must match the json
STORE_NAME = "My Awesome Store"
```

### Update the startup script
`check_orders.sh`

### Rpi.GPIO Errors
Install Rpi.GPIO if it's not already installed.
- `sudo apt-get update`
- `sudo apt-get install rpi.gpio`