from __future__ import annotations

from fastapi import FastAPI

from env.unlight_gym_env import UnlightGymEnv
from ui.cli import play_human_vs_ai

app = FastAPI(title="Unlight RL MVP")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/state")
def get_state() -> dict[str, object]:
    env = UnlightGymEnv()
    obs, info = env.reset()
    return {"observation": obs, "action_mask": info["action_mask"]}


@app.post("/step")
def step(action: int) -> dict[str, object]:
    env = UnlightGymEnv()
    env.reset()
    obs, reward, terminated, truncated, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "terminated": terminated,
        "truncated": truncated,
        "info": info,
    }


def main() -> None:
    print("Unlight RL MVP")
    env = UnlightGymEnv()
    obs, info = env.reset()
    print("Observation:", obs)
    print("Action mask valid count:", sum(info["action_mask"]))
    play_human_vs_ai()


if __name__ == "__main__":
    main()
