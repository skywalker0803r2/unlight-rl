import math

from engine.card import Card, CardType
from engine.duel import Duel, DuelAction
from env.unlight_gym_env import UnlightGymEnv


def test_card_and_action_values():
    assert CardType.MOVE.value == "M"
    assert CardType.SWORD.value == "S"
    assert CardType.GUN.value == "G"
    assert CardType.SPECIAL.value == "Sp"
    assert DuelAction.PASS.value == 0
    assert DuelAction.MOVE_FORWARD.value == 1


def test_duel_starts_with_valid_state():
    duel = Duel()
    assert duel.state["distance"] == 2
    assert duel.state["phase"] == "move"
    assert duel.state["round"] == 1
    assert duel.state["winner"] is None


def test_gym_env_observation_shape_and_mask():
    env = UnlightGymEnv()
    obs, info = env.reset()
    assert len(obs) == 10
    assert isinstance(info.get("action_mask"), list)
    assert len(info["action_mask"]) == 16
    assert all(isinstance(v, bool) for v in info["action_mask"])
    assert abs(obs[0]) <= 1.0
    assert abs(obs[1]) <= 1.0


def test_env_step_returns_valid_transition():
    env = UnlightGymEnv()
    env.reset()
    action = 0
    obs, reward, terminated, truncated, info = env.step(action)
    assert isinstance(obs, list)
    assert isinstance(reward, (int, float))
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert isinstance(info, dict)
    assert len(obs) == 10
    assert math.isfinite(reward)
