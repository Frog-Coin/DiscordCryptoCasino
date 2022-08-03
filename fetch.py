from __future__ import print_function
import requests
import json
from data import *
import threading

import time, requests, json

class RPCHost(object):
    def __init__(self, url):
        self._session = requests.Session()
        self._url = url
        self._headers = {'content-type': 'application/json'}
    def call(self, rpcMethod, *params):
        payload = json.dumps({"method": rpcMethod, "params": list(params), "jsonrpc": "2.0"})
        tries = 5
        hadConnectionFailures = False
        while True:
            try:
                response = self._session.post(self._url, headers=self._headers, data=payload)
            except requests.exceptions.ConnectionError:
                tries -= 1
                if tries == 0:
                    raise Exception('Failed to connect for remote procedure call.')
                hadFailedConnections = True
                print("Couldn't connect for remote procedure call, will sleep for five seconds and then try again ({} more tries)".format(tries))
                time.sleep(10)
            else:
                if hadConnectionFailures:
                    print('Connected for remote procedure call after retry.')
                break
        if not response.status_code in (200, 500):
            raise Exception('RPC connection failure: ' + str(response.status_code) + ' ' + response.reason)
        responseJSON = response.json()
        if 'error' in responseJSON and responseJSON['error'] != None:
            raise Exception('Error in RPC call: ' + str(responseJSON['error']))
        return responseJSON['result']


# The RPC username and RPC password MUST match the one in your bitcoin.conf file

serverURL = 'http://rpcuser:rpcpassword@127.0.0.1:rpcport'


#Using the class defined in the bitcoin_rpc_class.py

host = RPCHost(serverURL)

# Gets a new address

def getAddress(userId):
 
    WalletResponse = host.call('getnewaddress', userId)
    print(WalletResponse)
    return WalletResponse

# Gets user balance


def getBalance(userId):
    WalletBalance = host.call('getbalance', userId)
    print(WalletBalance)
    return WalletBalance
    
# Gets Main Wallet Balance balance


def getMainBalance():
    WalletBalance = host.call('getbalance', 'CHANGEME-PayoutWALLETACCOUNT')
    print(WalletBalance)
    return WalletBalance

# Assigns an address to an account based on discord ID


def getNewAddy(userId):
    NewAddy = host.call('getaccountaddress', userId)
    print(NewAddy)
    return NewAddy

# Send coins functionality


def sendCoins(uid, toAddress, amount):
    #sendTx = host.call('sendfrom', [uid, toAddress, amount])
    sendTx = host.call('sendfrom', uid, toAddress, float(amount))
    print(sendTx)
    return sendTx

# Updates balances


def updateBalances():
    updateWallets = host.call('listaccounts')
    # print(json.dumps(updateWallets['result'], indent=4))
    newBalance = updateWallets['result']
    for i in updateWallets['result']:
        c.execute("SELECT * FROM users WHERE userid=:i",
                  {'i': i})
        getWallets = c.fetchall()
        if getWallets != []:
            c.execute("UPDATE users SET balance=:b WHERE userid=:i",
                      {'i': i, 'b': newBalance[i]})
            con.commit()
    print("balances updated")

# Updates data to database


def sendToDB():
    updateBalances()

# Gets value of cards for blackjack


def getCardValue(Draw):
    global cardValue
    if Draw.startswith("Ace"):
        cardValue = 1
    elif Draw.startswith("Two"):
        cardValue = 2
    elif Draw.startswith("Three"):
        cardValue = 3
    elif Draw.startswith("Four"):
        cardValue = 4
    elif Draw.startswith("Five"):
        cardValue = 5
    elif Draw.startswith("Six"):
        cardValue = 6
    elif Draw.startswith("Seven"):
        cardValue = 7
    elif Draw.startswith("Eight"):
        cardValue = 8
    elif Draw.startswith("Nine"):
        cardValue = 9
    elif Draw.startswith("Ten"):
        cardValue = 10
    elif Draw.startswith("Jack"):
        cardValue = 10
    elif Draw.startswith("Queen"):
        cardValue = 10
    elif Draw.startswith("King"):
        cardValue = 10
    return cardValue

# Set interval function


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


# set_interval(sendToDB, 60)
# getAddress()
# getBalance("417504362231758858")
