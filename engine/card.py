from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CardType(str, Enum):
    MOVE = "M"
    SWORD = "S"
    GUN = "G"
    SPECIAL = "Sp"


@dataclass(frozen=True)
class Card:
    card_type: CardType
    name: str
    value: int = 0

    @property
    def label(self) -> str:
        return self.name

    def __str__(self) -> str:
        return f"{self.card_type.value}:{self.name}"


def make_deck() -> list[Card]:
    return [
        Card(CardType.MOVE, "Move", 1),
        Card(CardType.MOVE, "Move", 1),
        Card(CardType.MOVE, "Move", 1),
        Card(CardType.MOVE, "Move", 1),
        Card(CardType.SWORD, "Sword", 2),
        Card(CardType.SWORD, "Sword", 2),
        Card(CardType.GUN, "Gun", 2),
        Card(CardType.GUN, "Gun", 2),
        Card(CardType.SPECIAL, "Special", 3),
        Card(CardType.SPECIAL, "Special", 3),
    ]
