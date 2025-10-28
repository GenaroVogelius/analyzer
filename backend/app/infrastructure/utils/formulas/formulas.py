

def calculate_tna(buy_price: float, sell_price: float, t: int) -> float:
    """
    Calculate the TNA (Tasa Nominal Anual)
    """
    return ( sell_price / buy_price - 1 ) * 365 / t *100
    

def calculate_nominal_profit(buy_price: float, sell_price: float, amount: int) -> float:
    """
    Calculate the nominal profit
    """
    return (sell_price - buy_price) * amount

def calculate_percentage_gain(buy_price: float, sell_price: float) -> float:
    """
    Calculate the percentage gain
    """
    return (sell_price / buy_price - 1) * 100

