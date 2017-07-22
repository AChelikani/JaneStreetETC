import sys
import socket
import json
import bot
env = sys.argv[1]

if str(env) == "p":
    env = "production"
else:
    env = "test-exch-KPCBTRAPHOUSE"



def connect(serv_addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serv_addr, int(port)))
    return (s, s.makefile('rw', 1))

s, exchange = connect(env, 25000)
json_string = '{"type": "hello", "team":"KPCBTRAPHOUSE"}'
print(json_string, file=exchange)

f = open('log.txt', 'w')

trade_counter = 1
owned_bond_shares = 0

buy_dict = {}
sell_dict = {}

def Convert(NOKUS_PRICE, NOKUS_QUANT, NOKFH_PRICE, NOKFH_QUANT):
    PRICE_DIFF = NOKUS_PRICE - NOKFH_PRICE
    MIN_QUANT = min(NOKUS_QUANT, NOKFH_QUANT)
    MONEY_DIFF = MIN_QUANT * PRICE_DIFF
    if MONEY_DIFF > 11:
        # TODO: meaning NOKFH is cheaper! buy in NOKFH and sell NOKUS with the minimum quantity
        return 1
    elif MONEY_DIFF < -11:
        # TODO: meaning NOKUS is cheaper! buy in NOKUS and sell NOKFH with the minimum quantity
        return 0

while (True):
    hello_from_exchange = exchange.readline().strip()
    msg = json.loads(hello_from_exchange)
    if (msg["type"] == "book"):
        try:
            buy_dict[msg["symbol"]] = msg["buy"][0][0]
            sell_dict[msg["symbol"]] = msg["sell"][0][0]
        except IndexError:
            pass
        # print(buy_dict)
        # print(sell_dict)

    if (msg["type"] == "book" and msg["symbol"] == "BOND"):
        if (msg["sell"] and sell_dict['BOND'] < 1000 and owned_bond_shares + msg["sell"][0][1] < 100):
            json_string = {"type" : "add", "order_id" : trade_counter, "symbol" : "BOND", "dir" : "BUY", "price" : sell_dict['BOND'], "size" : msg["sell"][0][1]}
            owned_bond_shares += msg["sell"][0][1]
            print(json.dumps(json_string), file=exchange)
            f.write("bought " + str(trade_counter) + " " + str(sell_dict['BOND']) + " " + str(msg["sell"][0][1]) + "\n")
            trade_counter += 1
        if (msg["buy"] and buy_dict["BOND"] > 1000 and owned_bond_shares > 0):
            json_string = {"type" : "add", "order_id" : trade_counter, "symbol" : "BOND", "dir" : "SELL", "price" : msg["buy"][0][0], "size" : msg["buy"][0][1]}
            owned_bond_shares -= msg["buy"][0][1]
            print(json.dumps(json_string), file=exchange)
            f.write("sold " + str(trade_counter) + " " + str(buy_dict["BOND"]) + " " + str(msg["buy"][0][1]) + "\n")
            trade_counter += 1

    print(msg, file = sys.stderr)
