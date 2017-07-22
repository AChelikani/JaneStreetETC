import json
import constants

def parse_open(msg):
    return msg["symbols"]

def parse_closed(msg):
    res = []
    for stock in constants.SYMBOLS:
        if stock not in msg["symbols"]:
            res += [stock]
    return res

def parse_books(msg):
    if (msg["symbol"] == "BOND"):
        parse_bond(msg["buy"], msg["sell"])

def parse_bond(buy, sell):
    # Base price is 1000
    

if __name__ == "__main__":
    pass
