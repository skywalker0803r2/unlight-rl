from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GameConfig:
    max_hp: int = 10
    starting_distance: int = 2
    max_hand_size: int = 6
    max_phase_index: int = 3
    action_space_size: int = 16
    observation_dim: int = 10


CONFIG = GameConfig()
