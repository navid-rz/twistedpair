import yaml
from .schema import MainCfg, LinkCfg, TxCfg, ChannelCfg, RxCfg, SimCfg

def load_main_cfg(path: str) -> MainCfg:
    with open(path, 'r') as f:
        cfg_dict = yaml.safe_load(f)
    # Support two layouts:
    # 1) top-level 'link' dict containing tx/channel/rx/sim
    # 2) flat top-level keys: tx, channel, rx, sim
    if 'link' in cfg_dict and cfg_dict['link'] is not None:
        link_cfg = cfg_dict['link']
    else:
        # build a link-like dict from top-level keys
        link_cfg = {
            'tx': cfg_dict.get('tx', {}),
            'channel': cfg_dict.get('channel', {}),
            'rx': cfg_dict.get('rx', {}),
            'sim': cfg_dict.get('sim', {}),
        }

    tx = TxCfg(**(link_cfg.get('tx') or {}))
    channel = ChannelCfg(**(link_cfg.get('channel') or {}))
    rx = RxCfg(**(link_cfg.get('rx') or {}))
    sim = SimCfg(**(link_cfg.get('sim') or {}))
    link = LinkCfg(tx=tx, channel=channel, rx=rx, sim=sim)
    return MainCfg(link=link)
