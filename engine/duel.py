from __future__ import annotations

import random
from collections import Counter
from enum import IntEnum

from .card import Card, CardType, make_deck
from .character import Character


class DuelAction(IntEnum):
    PASS = 0
    MOVE_FORWARD = 1
    MOVE_BACK = 2
    BASIC_ATTACK = 3
    TRIGGER_SKILL_1 = 4
    TRIGGER_SKILL_2 = 5
    SWORD_STRIKE = 6
    GUN_STRIKE = 7
    SPECIAL_STRIKE = 8
    DEFEND = 9
    REPOSITION = 10
    COUNTER = 11
    RISKY_ATTACK = 12
    FEINT = 13
    HOLD = 14
    DRAW = 15


class Duel:
    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)
        self.self_char = Character("Ebert")
        self.opponent_char = Character("Ebert")
        self.state = {
            "distance": 2,
            "phase": "move",
            "round": 1,
            "winner": None,
            "last_action": None,
            "self_hp": 10,
            "opponent_hp": 10,
        }
        self.reset()

    def reset(self) -> None:
        self.self_char.reset()
        self.opponent_char.reset()
        self.state.update({
            "distance": 2,
            "phase": "move",
            "round": 1,
            "winner": None,
            "last_action": None,
            "self_hp": 10,
            "opponent_hp": 10,
        })
        self._deal_initial_hands()

    def _deal_initial_hands(self) -> None:
        deck = make_deck()
        self.random.shuffle(deck)
        self.self_char.hand = deck[:4]
        self.opponent_char.hand = deck[4:8]

    def list_hand_counts(self, side: str) -> Counter:
        character = self.self_char if side == "self" else self.opponent_char
        counts = Counter()
        for card in character.hand:
            counts[card.card_type] += 1
        return counts

    def get_action_mask(self) -> list[bool]:
        counts = self.list_hand_counts("self")
        mask = [False] * 16
        mask[DuelAction.PASS] = True
        mask[DuelAction.MOVE_FORWARD] = counts.get(CardType.MOVE, 0) >= 1
        mask[DuelAction.MOVE_BACK] = counts.get(CardType.MOVE, 0) >= 1
        mask[DuelAction.BASIC_ATTACK] = counts.get(CardType.SWORD, 0) >= 1 or counts.get(CardType.GUN, 0) >= 1
        mask[DuelAction.TRIGGER_SKILL_1] = self.self_char.can_trigger_skill_one(counts)
        mask[DuelAction.TRIGGER_SKILL_2] = self.self_char.can_trigger_skill_two(counts)
        mask[DuelAction.SWORD_STRIKE] = counts.get(CardType.SWORD, 0) >= 1
        mask[DuelAction.GUN_STRIKE] = counts.get(CardType.GUN, 0) >= 1
        mask[DuelAction.SPECIAL_STRIKE] = counts.get(CardType.SPECIAL, 0) >= 1
        mask[DuelAction.DEFEND] = True
        mask[DuelAction.REPOSITION] = counts.get(CardType.MOVE, 0) >= 1
        mask[DuelAction.COUNTER] = counts.get(CardType.SWORD, 0) >= 1
        mask[DuelAction.RISKY_ATTACK] = counts.get(CardType.GUN, 0) >= 1 or counts.get(CardType.SWORD, 0) >= 1
        mask[DuelAction.FEINT] = counts.get(CardType.MOVE, 0) >= 1
        mask[DuelAction.HOLD] = True
        mask[DuelAction.DRAW] = len(self.self_char.hand) < 6
        return mask

    def resolve_action(self, action: int | DuelAction) -> tuple[float, bool, dict]:
        action_value = int(action)
        mask = self.get_action_mask()
        if not mask[action_value]:
            action_value = DuelAction.PASS

        self.state["last_action"] = action_value
        reward = 0.0
        terminated = False
        info = {"action": action_value}

        if action_value == DuelAction.PASS:
            reward = 0.0
        elif action_value == DuelAction.MOVE_FORWARD:
            self.state["distance"] = max(1, self.state["distance"] - 1)
            reward = 0.02
        elif action_value == DuelAction.MOVE_BACK:
            self.state["distance"] = min(3, self.state["distance"] + 1)
            reward = 0.01
        elif action_value in {DuelAction.BASIC_ATTACK, DuelAction.SWORD_STRIKE, DuelAction.GUN_STRIKE, DuelAction.RISKY_ATTACK}:
            damage = 1 if action_value in {DuelAction.BASIC_ATTACK, DuelAction.SWORD_STRIKE, DuelAction.RISKY_ATTACK} else 2
            self.state["opponent_hp"] = max(0, self.state["opponent_hp"] - damage)
            reward = 0.05 * damage
        elif action_value == DuelAction.TRIGGER_SKILL_1:
            self.state["opponent_hp"] = max(0, self.state["opponent_hp"] - 3)
            reward = 0.10
        elif action_value == DuelAction.TRIGGER_SKILL_2:
            self.state["opponent_hp"] = max(0, self.state["opponent_hp"] - 2)
            reward = 0.10
        elif action_value == DuelAction.DEFEND:
            self.state["self_hp"] = min(10, self.state["self_hp"] + 1)
            reward = 0.03
        elif action_value == DuelAction.DRAW:
            reward = 0.01

        if self.state["opponent_hp"] <= 0:
            self.state["winner"] = "self"
            reward += 1.0
            terminated = True
        elif self.state["self_hp"] <= 0:
            self.state["winner"] = "opponent"
            reward -= 1.0
            terminated = True
        else:
            self.state["phase"] = "attack" if self.state["phase"] == "move" else "move"
            self.state["round"] += 1 if self.state["phase"] == "move" else 0

        return reward, terminated, info

    def step(self, action: int | DuelAction) -> tuple[float, bool, dict]:
        return self.resolve_action(action)
