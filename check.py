import requests
import json
import time
import os
from datetime import datetime


### Functions ###
# Define clearConsole()
def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

# Define getPoolData()
def getPoolData():
    response = requests.get('https://api.nanopool.org/v1/eth/user/' + address)
    return response.json()

# Define getETHPrice()
def getETHPrice():
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD')
    return response.json()


### Code ###

# Clear console
clearConsole()

# Get Timeout
timeout = int(input("Enter update time (in seconds): "))

if(timeout == 0):
    print('Invalid timeout number!')
    exit()

# Wallet
address = ''

# Get ETH Price
ethPrice = getETHPrice()

count = 0
while True:
    toDisplay = "=================" + str(datetime.now()) + "=================" + "\n"

    # Get Wallet JSON data
    json = getPoolData()

    # Check if everything is good
    if json['status'] == False:
        time.sleep(timeout / 2)
        continue
    
    # Every 10 iterations update ETH price
    if count > 10:
        # Save old ETH Price
        oldPrice = ethPrice
        # Get new ETH Price
        ethPrice = getETHPrice()

        toDisplay += 'Updating ETH price: %s => %s' % (oldPrice['USD'], ethPrice['USD']) + "\n"
        count = 0

    # Print Info
    toDisplay += "ETH Price: $%s \n" % (str(ethPrice['USD']))
    toDisplay += "Current stats for " + json['data']['account'] + "\n"
    toDisplay += "Balance: " + json['data']['balance'] + "ETH | " + str( round(float(json['data']['balance']) * float(ethPrice['USD']), 2) ) + "USD" + "\n"
    toDisplay += "Workers: " + "\n"

    # Print all workers
    for worker in json['data']['workers']:
        toDisplay += " > " + worker['id'] + " - " + worker['h24'] + "Mh/s (24h average) \n"
    
    toDisplay += "============================================================"

    # Clear Terminal
    clearConsole()

    # Print all Text
    print(toDisplay)

    # Wait for n amount of seconds
    time.sleep(timeout)

    # Count +1
    count = count + 1