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


def get_last_block(name_of_file):
    df = pd.read_csv(name_of_file)
    return df.at[df.index[-1], 'block']


def save_to_csv(name_of_file, data, write_header=False):
    with open(name_of_file, 'a', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=data[0].keys())
        if write_header:
            fc.writeheader()
        fc.writerows(data)


def extract_info(txn):
    retVal = dict(txn.args)
    retVal['block'] = txn.blockNumber
    return retVal


def get_transfers(instance, from_block, to_block):
    event_filter = instance.events.Transfer.createFilter(
        fromBlock=from_block,
        toBlock=to_block
    )
    return [extract_info(x) for x in event_filter.get_all_entries()]


def get_all_transfers(w3, name, end=0, is_new=False):
    token_instance = get_token_instance(w3, name)
    details = td.get(name)
    interval = details.get('interval')

    # If file is not new, get the latest row and extract the last block.
    # Else get the start block from event_details.py
    start = 0
    if not is_new:
        start = int(get_last_block('./stake/transfers.csv') + 1)
    else:
        start = details.get('start')

    # Check if end block is provided.
    if not end:
        end = get_latest_block(w3) - 15

    from_block = start
    end_block = end
    to_block = from_block + interval
    txns = []

    while from_block < end_block:
        if(to_block > end_block):
            to_block = end_block
        print(from_block, to_block)
        txns.extend(get_transfers(token_instance, from_block, to_block))
        from_block += interval
        to_block += interval

    save_to_csv('./stake/transfers.csv', txns, write_header=is_new)


w3 = connect_to_web3()
get_all_transfers(w3, 'stake')
