

NOKUS_PRICE = 1000
NOKUS_QUANT = 10
NOKFH_PRICE = 1000
NOKFH_QUANT = 10

def ETF(NOKUS_PRICE, NOKUS_QUANT, NOKFH_PRICE, NOKFH_QUANT):
    PRICE_DIFF = NOKUS_PRICE - NOKFH_PRICE
    MIN_QUANT = min(NOKUS_QUANT, NOKFH_QUANT)
    MONEY_DIFF = MIN_QUANT * PRICE_DIFF

    if MONEY_DIFF > 15:
        # TODO: meaning NOKFH is cheaper! buy in NOKFH and sell NOKUS with the minimum quantity
        return
    elif MONEY_DIFF < -15:
        # TODO: meaning NOKUS is cheaper! buy in NOKUS and sell NOKFH with the minimum quantity
        return