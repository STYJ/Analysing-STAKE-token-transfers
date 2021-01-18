from web3 import Web3
from dotenv import load_dotenv
import os

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

w3 = connect_to_web3()
print(get_latest_block(w3))


{
  "language": "Solidity",
  "sources":
  {
    "IERC20.sol":
    {
      "urls":
      [
        "bzzr://56ab...",
        "ipfs://Qma...",
        "./contracts/IERC20.sol"
      ]
    },
  },
}