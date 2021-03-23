import requests
import json
import time
import os
from datetime import datetime

# Clear Terminal
os.system('clear')

timeout = int(input("Enter update time (in seconds): "))

if(timeout == 0):
    print('Invalid timeout number!')
    exit()

# Wallet
address = ''

# Get ETH Price
ethResponse = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
ethPrice = ethResponse.json()

count = 0
while True:
    toDisplay = "=================" + str(datetime.now()) + "=================" + "\n"
    response = requests.get('https://api.nanopool.org/v1/eth/user/' + address)

    # Get Wallet JSON data
    json = response.json()

    # Check if everything is good
    status = json['status']
    if status == False:
        time.sleep(timeout / 2)
        continue
    
    # Every 10 iterations update ETH price
    if count > 10:
        # Save old ETH Price
        oldPrice = ethPrice
        # Get new ETH Price5
        ethResponse = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
        ethPrice = ethResponse.json()

        toDisplay += 'Updating ETH price: %s => %s' % (oldPrice['USD'], ethPrice['USD']) + "\n"
        count = 0

    # Print Info
    toDisplay += "Current stats for " + json['data']['account'] + "\n"
    toDisplay += "Balance: " + json['data']['balance'] + "ETH | " + str( round(float(json['data']['balance']) * float(ethPrice['USD']), 2) ) + "USD" + "\n"
    toDisplay += "Workers: " + "\n"

    # Print all workers
    for worker in json['data']['workers']:
        toDisplay += " >" + worker['id'] + " - " + worker['h24'] + "Mh/s (24h average)" + "\n"
    
    toDisplay += "============================================================"

    # Clear Terminal
    os.system('clear')

    # Print all Text
    print(toDisplay)

    # Wait for n amount of seconds
    time.sleep(timeout)

    # Count +1
    count = count + 1