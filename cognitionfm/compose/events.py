from dataclasses import dataclass, field

# Ceiling on Event.dur, enforced by every generator; render.py sizes its carry
# buffer against this so an event always fits entirely within one buffer.
MAX_EVENT_S = 90.0


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
