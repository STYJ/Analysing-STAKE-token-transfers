from web3 import Web3
from dotenv import load_dotenv
import os
import json
from constants import TOKEN_DETAILS as td
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


def get_abi(name):
    with open('ABIs/' + name) as f:
        return json.load(f)

def get_contract_instance(w3, address, abi):
    return w3.eth.contract(address=address, abi=abi)


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

def get_events(instance, event_name, from_block, to_block):
    event_filter = instance.events[event_name].createFilter(
        fromBlock=from_block,
        toBlock=to_block
    )
    return [extract_info(x) for x in event_filter.get_all_entries()]


# When you want to query historical transactions for the first time, you should specify
# the start_block and is_new = true
def get_historical_txns(w3, name, contract, path, event_name, start=0, end=0, interval=1000, is_new=False):

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
        save_to_csv(path, txns, write_header=is_new)


w3 = connect_to_web3()

token_name = 'stake'
token_details = td.get(token_name)

# abi = get_abi('IERC20.json')
# address = token_details.get('erc20').get('address')
# instance = get_contract_instance(w3, address, abi)

# get_historical_txns(w3=w3,
#                     name=token_name,
#                     contract=instance,
#                     path='./stake/transfers.csv',
#                     event_name=token_details.get('erc20').get('event_name'),
#                     interval=token_details.get('erc20').get('interval'))

# abi = get_abi('BPool.json')
# address = token_details.get('balancer').get('address')
# instance = get_contract_instance(w3, address, abi)

# get_historical_txns(w3=w3,
#                     name=token_name,
#                     contract=instance,
#                     path='./stake/join_balancer.csv',
#                     event_name=token_details.get('balancer').get('event_name')[0],
#                     interval=token_details.get('balancer').get('interval'),
#                     is_new=False)


# get_historical_txns(w3=w3,
#                     name=token_name,
#                     contract=instance,
#                     path='./stake/exit_balancer.csv',
#                     event_name=token_details.get('balancer').get('event_name')[1],
#                     start=token_details.get('balancer').get('start'),
#                     interval=token_details.get('balancer').get('interval'),
#                     is_new=True)
                    
abi = get_abi('UniswapV2Pair.json')
address = token_details.get('uniswap').get('address')
instance = get_contract_instance(w3, address, abi)

for e in token_details.get('uniswap').get('event_name'):
    get_historical_txns(w3=w3,
                        name=token_name,
                        contract=instance,
                        path=f'./stake/{e.lower()}_uniswap.csv',
                        event_name=e,
                        interval=token_details.get('uniswap').get('interval'))

# get_historical_txns(w3=w3,
#                     name=token_name,
#                     contract=instance,
#                     path='./stake/burn_uniswap.csv',
#                     event_name=token_details.get('uniswap').get('event_name')[1],
#                     start=token_details.get('uniswap').get('start'),
#                     interval=token_details.get('uniswap').get('interval'),
#                     is_new=True)
