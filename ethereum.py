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
    address=td.get(name.lower(), False)
    if address:
        address=address.get('address')
        abi = get_erc20_abi()
        return w3.eth.contract(address=address, abi=abi)
    else:
        print(f'"{name}" is not a valid token symbol')
        exit(1)

# TODO: Maybe next time you don't have to save as CSV.
# Just parse directly with pandas
# TODO: Should also include block number in file name
def save_to_csv(nameOfFile, data):
    with open(nameOfFile, 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=data[0].keys())
        fc.writeheader()
        fc.writerows(data)




w3 = connect_to_web3()
tokenName = 'stake'
tokenInstance = get_token_instance(w3, tokenName)
decimals = 10 ** tokenInstance.functions.decimals().call()
# fromBlock = td.get(tokenName.lower()).get('start')
# toBlock = get_latest_block(w3)
fromBlock = 11685382
toBlock = 11685500

event_filter = tokenInstance.events.Transfer.createFilter(
    fromBlock=fromBlock,
    toBlock=toBlock
)

txns = [x.args for x in event_filter.get_all_entries()]
df = pd.DataFrame(txns)
print(df.head())

# save_to_csv('txns.csv', txns)



# print(get_latest_block(w3))
