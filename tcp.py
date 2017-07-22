import sys
import socket

def connect(serv_addr, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serv_addr, int(port)))
    return (s, s.makefile('rw', 1))

s, exchange = connect("test-exch-KPCBTRAPHOUSE",25000)
json_string = '{"type": "hello", "team":"KPCBTRAPHOUSE"}'
print(json_string, file=exchange)

while True:
    hello_from_exchange = exchange.readline().strip()
    print("The exchange replied: %s" % str(hello_from_exchange),file = sys.stderr)
