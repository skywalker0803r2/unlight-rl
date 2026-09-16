from __future__ import annotations

from typing import Any

import gymnasium as gym
import numpy as np

from config import CONFIG
from engine.duel import Duel


class UnlightGymEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}

    def __init__(self, render_mode: str | None = None) -> None:
        self.render_mode = render_mode
        self.action_space = gym.spaces.Discrete(CONFIG.action_space_size)
        self.observation_space = gym.spaces.Box(
            low=0.0,
            high=1.0,
            shape=(CONFIG.observation_dim,),
            dtype=np.float32,
        )
        self.duel = Duel()

    def _observation(self) -> list[float]:
        self_hp = self.duel.state["self_hp"] / CONFIG.max_hp
        opp_hp = self.duel.state["opponent_hp"] / CONFIG.max_hp
        distance = self.duel.state["distance"] / 3.0
        phase_map = {"move": 0.0, "attack": 1.0, "defense": 2.0, "round_end": 3.0}
        phase = phase_map.get(self.duel.state["phase"], 0.0) / CONFIG.max_phase_index
        self_counts = self.duel.list_hand_counts("self")
        hand = [self_counts.get(card_type, 0) / CONFIG.max_hand_size for card_type in ["M", "S", "G", "Sp"]]
        opp_cards = min(len(self.duel.opponent_char.hand), CONFIG.max_hand_size) / CONFIG.max_hand_size
        round_norm = self.duel.state["round"] / 20.0
        return [self_hp, opp_hp, distance, phase, *hand, opp_cards, round_norm]

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None):
        super().reset(seed=seed)
        self.duel.reset()
        obs = self._observation()
        info = {"action_mask": self.duel.get_action_mask()}
        return obs, info

    def step(self, action: int):
        reward, terminated, info = self.duel.resolve_action(action)
        obs = self._observation()
        info = {"action_mask": self.duel.get_action_mask(), "winner": self.duel.state["winner"]}
        return obs, float(reward), bool(terminated), False, info

    def render(self) -> None:
        print(self.duel.state)
