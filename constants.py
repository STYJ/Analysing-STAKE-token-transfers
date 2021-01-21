# For balancer events, the tokenAmount(In/Out) tells you how many tokens
# For uniswap events, amount0 represents tokens, amount1 represents eth
TOKEN_DETAILS = {
    'stake': {
        'erc20': {
            'address': '0x0Ae055097C6d159879521C384F1D2123D1f195e6',
            'start': 9877421,
            'interval': 2500,
            'event_name': 'Transfer',
        },
        'balancer': {
            'address': '0x1DDF0976Ac842C696d01a86b39d25b067Ed8C7ff',
            'start': 11281296,
            'interval': 100000,
            'event_name': ['LOG_JOIN', 'LOG_EXIT'],
        },
        'uniswap': {
            'address': '0x3B3d4EeFDc603b232907a7f3d0Ed1Eea5C62b5f7',
            'start': 10113195,
            'interval': 50000,
            'event_name': ['Mint', 'Burn'],
        },
    }
}
