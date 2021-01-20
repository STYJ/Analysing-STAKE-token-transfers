from web3 import Web3
from dotenv import load_dotenv
import os
import json
from token_details import TOKEN_DETAILS as td
import csv
import pandas as pd

# Environtment variables
load_dotenv()

# Infura Path
PATH = 'wss://mainnet.infura.io/ws/v3/'


def connect_to_web3():
    KEY = os.getenv("INFURA_KEY")
    w3 = Web3(Web3.WebsocketProvider(PATH + KEY))
    try:
        w3.isConnected()
        return w3
    except:
        print('Failed to connect to web3 provider.')
        exit(1)


def get_latest_block(w3):
    return w3.eth.blockNumber


def get_erc20_abi():
    with open('contracts/IERC20.json') as f:
        return json.load(f)


def get_token_instance(w3, name):
    address = td.get(name.lower(), False)
    if address:
        address = address.get('address')
        abi = get_erc20_abi()
        return w3.eth.contract(address=address, abi=abi)
    else:
        print(f'"{name}" is not a valid token symbol')
        exit(1)


def save_to_csv(nameOfFile, data):
    with open(nameOfFile, 'a', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=data[0].keys())
        fc.writeheader()
        fc.writerows(data)


def extract_info(txn):
    retVal = dict(txn.args)
    retVal['block'] = txn.blockNumber
    return retVal

def get_historical_transfers(w3, name, start=0, end=0):
    tokenInstance = get_token_instance(w3, name)
    details = td.get(name.lower())
    interval = details.get('interval')

    if not start:
        start = details.get('start')

    if not end:
        end = get_latest_block(w3) - 15

    fromBlock = start
    endBlock = end
    toBlock = fromBlock + interval
    txns = []

    while fromBlock < endBlock:
        if(toBlock > endBlock):
            toBlock = endBlock
        print(fromBlock, toBlock)
        event_filter = tokenInstance.events.Transfer.createFilter(
            fromBlock=fromBlock,
            toBlock=toBlock
        )
        txns.extend([extract_info(x) for x in event_filter.get_all_entries()])
        fromBlock += interval
        toBlock += interval

    save_to_csv(f'{name}_{start}_{end}.csv', txns)


w3 = connect_to_web3()
# get_historical_transfers(w3, 'stake')
