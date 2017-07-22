import sys
import socket
import json
import bot

def connect(serv_addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serv_addr, int(port)))
    return (s, s.makefile('rw', 1))

s, exchange = connect("production",25000)
json_string = '{"type": "hello", "team":"KPCBTRAPHOUSE"}'
print(json_string, file=exchange)

f = open('log_bond_test.txt', 'w')
#b = open('bond_prices.txt', 'w')


trade_counter = 1
owned_bond_shares = 0

while (True):
    hello_from_exchange = exchange.readline().strip()
    msg = json.loads(hello_from_exchange)
    if (msg["type"] == "book" and msg["symbol"] == "BOND"):
        #b.write(str(msg) + "\n")
        if (msg["sell"]):
            for val in msg["sell"]:
                if (val[0] < 1000 and owned_bond_shares + val[1] <= 100):
                    json_string = {"type" : "add", "order_id" : trade_counter, "symbol" : "BOND", "dir" : "BUY", "price" : val[0], "size" : val[1]}
                    owned_bond_shares += val[1]
                    print(json.dumps(json_string), file=exchange)
                    f.write("bought " + str(trade_counter) + " " + str(val[0]) + " " + str(val[1]) + "\n")
                    trade_counter += 1
        if (msg["buy"]):
            for val in msg["buy"]:
                if (val[0] > 1000 and owned_bond_shares > 0):
                    json_string = {"type" : "add", "order_id" : trade_counter, "symbol" : "BOND", "dir" : "SELL", "price" : val[0], "size" : min(val[1], owned_bond_shares)}
                    owned_bond_shares -= val[1]
                    print(json.dumps(json_string), file=exchange)
                    f.write("sold " + str(trade_counter) + " " + str(val[0]) + " " + str(val[1]) + "\n")
                    trade_counter += 1
    if (msg["type"] == "ack"):
        f.write("trade " + str(msg["order_id"]) + "\n")
    print(msg, file = sys.stderr)
