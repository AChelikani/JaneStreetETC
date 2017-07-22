import json
import constants
import parser

class Bot(object):
    def __init__(self):
        self.parser = parser.Parser()
        self.holdings =  {}
        self.open = {}
        for stock in constants.SYMBOLS:
            self.positions[stock] = 0

    def process_line(self, line):
        if (line["type"] == "hello"):
            pass
        elif (line["type"] == "open"):
            self.open = parser.parse_open(line)
        elif (line["type"] == "close"):
            self.open = parse.parse_closed(line)
        elif (line["type"] == "book"):
            pass
        elif (line["type"] == "trade"):
            pass
