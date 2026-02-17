def rolling_average(values, window):
    if len(values) < window:
        return None
    return sum(values[-window:]) / window

def last_n(values, n):
    return values[-n:] if len(values) >= n else values

def safe_div(a, b):
    if b == 0:
        return 0
    return a / b