from dataclasses import dataclass, field


@dataclass
class Event:
    """One sound event. `timbre` selects the synth patch in render.py."""
    t: float            # start time, seconds
    dur: float          # seconds, envelope included
    freq: float         # Hz
    amp: float          # linear, pre-master
    pan: float = 0.0    # -1..1
    timbre: str = "pad"
    attack_s: float = 2.0
    release_s: float = 4.0
    params: dict = field(default_factory=dict)
