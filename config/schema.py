from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class TxCfg:
    data_rate: float  # Gbps
    modulation: str   # 'NRZ' or 'PAM4'
    ffe_taps: Optional[List[float]] = None
    jitter: Optional[dict] = None
    swing: Optional[float] = None
    vcm: Optional[float] = None
    symbol_duration: Optional[float] = None  # Symbol duration in seconds

@dataclass
class ChannelCfg:
    type: str         # 'simple', 'sparam', or 'copper'
    fixed_loss_db: float    # Fixed dB loss
    isi_taps: Optional[List[float]] = None
    awgn_sigma: Optional[float] = None
    delay: Optional[float] = None
    # Copper channel loss profile
    alpha_db_per_in_ghz: Optional[float] = 0.5  # typical value
    length_in: Optional[float] = 20.0           # inches
    f_ref_ghz: Optional[float] = 10.0           # reference frequency
    gauge: Optional[int] = 28                   # AWG
    temperature: Optional[float] = 25.0         # Celsius
    skin_effect: Optional[bool] = True
    dielectric_loss: Optional[float] = 0.0005   # loss tangent
    profile: Optional[str] = None               # cable type/profile

@dataclass
class RxCfg:
    ctle_params: Optional[dict] = None
    dfe_taps: Optional[List[float]] = None
    slicer_type: str = 'NRZ'
    cdr_type: str = 'ideal'  # Possible values: 'ideal', 'bbpd', 'hogge', 'bangbang', 'pi', 'pll', 'oversampled', 'baudrate', 'phase_interpolator'

@dataclass
class SimCfg:
    n_symbols: int
    sps: int
    bit_mode: str = 'random'  # 'random', 'prbs', etc.
    prbs_order: int = 7  # PRBS order (default 7)
    random_seed: Optional[int] = None

@dataclass
class LinkCfg:
    tx: TxCfg
    channel: ChannelCfg
    rx: RxCfg
    sim: SimCfg

@dataclass
class MainCfg:
    link: LinkCfg
    # Add more top-level config as needed
