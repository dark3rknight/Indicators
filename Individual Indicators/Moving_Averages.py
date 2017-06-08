import math

def sma(data, window):
    if len(data) < window:
        return 0
    return sum(data[-window:])/float(window)

def calc_ema(data, window):
    if len(data) <= 2 * window:
        return sma(data[-window:],window)
    multiplier = 2.0 / (window + 1)
    current_ema = sma(data[-window*2:-window], window)
    for value in data[-window:]:
        current_ema = (multiplier * value) + ((1 - multiplier) * current_ema)
    return current_ema

def get_all_EMAs(data, window):
    EMA = [None] * ((window))
    for i in range(window, len(data)):
        EMA.append(calc_ema(data[:i], window))
    return EMA
