from __future__ import annotations

from engine.duel import DuelAction


class RuleAgent:
    def __init__(self) -> None:
        self.name = "RuleBot"

    def act(self, observation, action_mask=None):
        if action_mask is None:
            return DuelAction.PASS
        if action_mask[DuelAction.TRIGGER_SKILL_1]:
            return DuelAction.TRIGGER_SKILL_1
        if action_mask[DuelAction.TRIGGER_SKILL_2]:
            return DuelAction.TRIGGER_SKILL_2
        if action_mask[DuelAction.BASIC_ATTACK]:
            return DuelAction.BASIC_ATTACK
        if action_mask[DuelAction.MOVE_FORWARD]:
            return DuelAction.MOVE_FORWARD
        if action_mask[DuelAction.DEFEND]:
            return DuelAction.DEFEND
        return DuelAction.PASS
