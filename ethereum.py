from web3 import Web3
from dotenv import load_dotenv
import os
import json
from constants import TOKEN_DETAILS as td
import csv
import pandas as pd

# Environtment variables
load_dotenv()

# ALCHEMY Path
PATH = 'wss://eth-mainnet.ws.alchemyapi.io/v2/'


def connect_to_web3():
    KEY = os.getenv("ALCHEMY_KEY")
    w3 = Web3(Web3.WebsocketProvider(PATH + KEY))
    try:
        w3.isConnected()
        return w3
    except:
        print('Failed to connect to web3 provider.')
        exit(1)


def get_latest_block(w3):
    return w3.eth.blockNumber


def get_abi(name):
    with open('ABIs/' + name) as f:
        return json.load(f)

def get_contract_instance(w3, address, abi):
    return w3.eth.contract(address=address, abi=abi)


def get_last_block(name_of_file):
    df = pd.read_csv(name_of_file)
    return df.at[df.index[-1], 'block']


def save_to_csv(name_of_file, mode, data, write_header=False):
    with open(name_of_file, mode, encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=data[0].keys())
        if write_header:
            fc.writeheader()
        fc.writerows(data)


def extract_info(txn):
    retVal = dict(txn.args)
    retVal['block'] = txn.blockNumber
    retVal['tx_hash'] = txn.transactionHash.hex()
    return retVal

def get_events(instance, event_name, from_block, to_block):
    event_filter = instance.events[event_name].createFilter(
        fromBlock=from_block,
        toBlock=to_block
    )
    return [extract_info(x) for x in event_filter.get_all_entries()]

def get_token_balance(instance, address):
    return instance.functions.balanceOf(address).call()

# When you want to query historical transactions for the first time, you should specify
# the start_block and is_new = true
def get_historical_txns(w3, contract, path, event_name, start=0, end=0, interval=1000, is_new=False):

    # If file is not new, get the latest row and extract the last block.
    if not is_new:
        start = int(get_last_block(path) + 1)

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
        txns.extend(get_events(contract, event_name, from_block, to_block))
        from_block += interval
        to_block += interval

    if len(txns) > 0:
        save_to_csv(path, 'a', txns, write_header=is_new)


w3 = connect_to_web3()

token_name = 'stake'
token_details = td.get(token_name)

abi = get_abi('IERC20.json')
token_address = token_details.get('token').get('address')
token_instance = get_contract_instance(w3, token_address, abi)
balances = []

for k, v in token_details.items():
    address = v.get('address')
    instance = get_contract_instance(w3, address, abi)
    print(f'Getting {k} transfer events')
    get_historical_txns(w3=w3,
                        contract=instance,
                        path=f'./stake/{k}_transfers.csv',
                        event_name='Transfer',
                        interval=v.get('interval'))

    balances.append({'who': k,
                     'address': address,
                     'qty': get_token_balance(token_instance, address),
                     'total_supply': instance.functions.totalSupply().call()})
    # If you want to create all .csv from scratch
    # get_historical_txns(w3=w3,
    #                     contract=instance,
    #                     path=f'./stake/{k}_transfers.csv',
    #                     start=v.get('start'),
    #                     event_name='Transfer',
    #                     interval=v.get('interval'),
    #                     is_new=True)
    print('done')

# If balances.csv does not exist, you need to use 'a' instead of 'w'
save_to_csv('./stake/balances.csv', 'w', balances, write_header=True)
