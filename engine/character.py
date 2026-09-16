from __future__ import annotations

from collections import Counter

from .card import Card, CardType


class Character:
    def __init__(self, name: str, max_hp: int = 10) -> None:
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.hand: list[Card] = []

    def copy_hand_counts(self) -> Counter:
        counter = Counter()
        for card in self.hand:
            counter[card.card_type] += 1
        return counter

    def can_trigger_skill_one(self, counts: Counter | None = None) -> bool:
        counts = counts or self.copy_hand_counts()
        return counts.get(CardType.SPECIAL, 0) >= 1 and counts.get(CardType.GUN, 0) >= 2

    def can_trigger_skill_two(self, counts: Counter | None = None) -> bool:
        counts = counts or self.copy_hand_counts()
        return counts.get(CardType.GUN, 0) >= 3 and counts.get(CardType.SWORD, 0) >= 1

    def reset(self) -> None:
        self.hp = self.max_hp
        self.hand.clear()
