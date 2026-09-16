from __future__ import annotations

from typing import Any

try:
    from stable_baselines3 import PPO
    from stable_baselines3.common.maskable.policies import MaskableActorCriticPolicy
    from stable_baselines3.common.vec_env import DummyVecEnv
except Exception:  # pragma: no cover - optional dependency for CPU-lite fallback
    PPO = None
    MaskableActorCriticPolicy = None
    DummyVecEnv = None


class MaskedPPOTrainer:
    def __init__(self, env: Any, policy: str = "MlpPolicy") -> None:
        self.env = env
        self.policy = policy
        self.model = None

    def train(self, total_timesteps: int = 1000) -> Any:
        if PPO is None:
            return None
        self.model = PPO(
            policy=self.policy,
            env=self.env,
            n_steps=128,
            batch_size=64,
            verbose=0,
            device="cpu",
        )
        self.model.learn(total_timesteps=total_timesteps)
        return self.model

    def evaluate(self, episodes: int = 3) -> float:
        if self.model is None:
            return 0.0
        wins = 0
        for _ in range(episodes):
            obs, info = self.env.reset()
            while True:
                action, _ = self.model.predict(obs, action_masks=info.get("action_mask"))
                obs, reward, terminated, truncated, info = self.env.step(int(action))
                if terminated or truncated:
                    if self.env.duel.state["winner"] == "self":
                        wins += 1
                    break
        return wins / max(1, episodes)
