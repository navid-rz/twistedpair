from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Symbols:
    values: List[int]
    modulation: str  # 'NRZ' or 'PAM4'

@dataclass
class Trace:
    time: List[float]
    voltage: List[float]
    sps: int

@dataclass
class Results:
    eye_height: Optional[float] = None
    eye_width: Optional[float] = None
    ber: Optional[float] = None
    snr: Optional[float] = None
