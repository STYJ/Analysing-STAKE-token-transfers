from dotenv import load_dotenv
import os

# Environtment variables
load_dotenv()

PATHS = {
    'ethereum': f'wss://eth-mainnet.ws.alchemyapi.io/v2/{os.getenv("ALCHEMY_KEY")}',
    'xdai': 'wss://rpc.xdaichain.com/wss'
}

# For balancer events, the tokenAmount(In/Out) tells you how many tokens
# For uniswap events, amount0 represents tokens, amount1 represents eth
TOKEN_DETAILS = {
    'ethereum': {
        'stake': {
            'token': {
                'address': '0x0Ae055097C6d159879521C384F1D2123D1f195e6',
                'start': 9877400,
                'interval': 2500,
            },
            'balancer': {
                'address': '0x1DDF0976Ac842C696d01a86b39d25b067Ed8C7ff',
                'start': 11281200,
                'interval': 100000,
            },
            'uniswap': {
                'address': '0x3B3d4EeFDc603b232907a7f3d0Ed1Eea5C62b5f7',
                'start': 10113100,
                'interval': 50000,
            },
        }
    },
    'xdai': {
        'stake': {
            'token': {
                'address': '0xb7D311E2Eb55F2f68a9440da38e7989210b9A05e',
                'start': 11582200,
                'interval': 5000,
            }
        }
    }
}
