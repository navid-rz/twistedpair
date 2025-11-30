# NRZ/PAM4 mapping, Gray tables, optional 64b/66b stub

def map_nrz(bits):
    """Map bits to NRZ symbols (-1, +1)."""
    return [1 if b else -1 for b in bits]

def map_pam4(bits):
    """Map bits to PAM4 symbols using Gray code."""
    gray_map = {(0,0): -3, (0,1): -1, (1,1): 1, (1,0): 3}
    symbols = []
    for i in range(0, len(bits), 2):
        pair = (bits[i], bits[i+1])
        symbols.append(gray_map[pair])
    return symbols
