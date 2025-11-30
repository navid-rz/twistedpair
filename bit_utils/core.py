import numpy as np
from typing import Sequence

def prbs(order: int, n_bits: int, seed: int = None) -> np.ndarray:
    """
    Generate PRBS sequence using LFSR.
    Args:
        order: LFSR order (number of bits in register)
        n_bits: Number of bits to generate
        seed: Initial value for the shift register (if None, random)
    Returns:
        Numpy array of bits (0/1)
    """
    taps = {
        7: [7, 6],
        9: [9, 5],
        15: [15, 14],
        23: [23, 18],
        31: [31, 28],
    }
    if seed is None:
        max_seed = min(2**order, 2**31 - 1)
        seed = np.random.randint(1, max_seed)
    reg = [int(x) for x in bin(seed)[2:].zfill(order)]
    seq = []
    for _ in range(n_bits):
        out = reg[-1]
        seq.append(out)
        feedback = 0
        for t in taps.get(order, [order, order-1]):
            feedback ^= reg[-t]
        reg = [feedback] + reg[:-1]
    return np.array(seq)

def random_bits(n_bits: int, seed: int = None) -> np.ndarray:
    """
    Generate true random bits.
    Args:
        n_bits: Number of bits to generate
        seed: Optional seed for reproducibility
    Returns:
        Numpy array of bits (0/1)
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.randint(0, 2, size=n_bits)

def correlate(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Compute cross-correlation of two bit sequences.
    Args:
        a: First bit sequence (array)
        b: Second bit sequence (array)
    Returns:
        Cross-correlation array
    """
    return np.correlate(a, b, mode='full')

def gold_code(order: int, n_bits: int, seed1: int = None, seed2: int = None) -> np.ndarray:
    """
    Generate Gold code sequence by XORing two LFSRs (PRBS).
    Args:
        order: LFSR order
        n_bits: Number of bits
        seed1: Seed for first LFSR
        seed2: Seed for second LFSR
    Returns:
        Gold code sequence
    """
    seq1 = prbs(order, n_bits, seed=seed1)
    seq2 = prbs(order, n_bits, seed=seed2)
    return np.bitwise_xor(seq1, seq2)

def gray_code(n_bits: int) -> np.ndarray:
    """
    Generate Gray code sequence of n_bits length.
    Args:
        n_bits: Number of bits
    Returns:
        Gray code sequence
    """
    nums = np.arange(n_bits)
    return np.bitwise_xor(nums, nums >> 1) % 2

def repeat(pattern: Sequence[int], n_bits: int) -> np.ndarray:
    """
    Repeat a bit pattern to fill n_bits.
    Args:
        pattern: Sequence of bits to repeat
        n_bits: Total length
    Returns:
        Repeated bit sequence
    """
    pattern = np.array(pattern)
    reps = int(np.ceil(n_bits / len(pattern)))
    return np.tile(pattern, reps)[:n_bits]

def alternating(n_bits: int, start: int = 0) -> np.ndarray:
    """
    Generate alternating 0/1 pattern.
    Args:
        n_bits: Number of bits
        start: 0 or 1
    Returns:
        Alternating bit sequence
    """
    return np.array([(i + start) % 2 for i in range(n_bits)])

def from_file(filepath: str) -> np.ndarray:
    """
    Load bit sequence from a file (expects 0/1 per line or as a string).
    Args:
        filepath: Path to file
    Returns:
        Bit sequence as numpy array
    """
    with open(filepath, 'r') as f:
        content = f.read().replace('\n', '').replace(' ', '')
    return np.array([int(c) for c in content if c in '01'])

def scramble(bits: np.ndarray, seed: int = None) -> np.ndarray:
    """
    Scramble a bit sequence using a random XOR mask.
    Args:
        bits: Input bit sequence
        seed: Optional seed
    Returns:
        Scrambled bit sequence
    """
    if seed is not None:
        np.random.seed(seed)
    mask = np.random.randint(0, 2, size=len(bits))
    return np.bitwise_xor(bits, mask)

def invert(bits: np.ndarray) -> np.ndarray:
    """
    Invert all bits in a sequence.
    Args:
        bits: Input bit sequence
    Returns:
        Inverted bit sequence
    """
    return np.bitwise_xor(bits, 1)

def shift(bits: np.ndarray, k: int) -> np.ndarray:
    """
    Circularly shift a bit sequence by k positions.
    Args:
        bits: Input bit sequence
        k: Number of positions to shift
    Returns:
        Shifted bit sequence
    """
    k = k % len(bits)
    return np.roll(bits, k)
