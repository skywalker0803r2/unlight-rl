# Unlight RL MVP

A lightweight turn-based duel game and RL prototype inspired by Unlight, designed for CPU-only execution in GitHub Codespaces and local development.

This repository now includes:

- A playable browser-based duel page at the root route
- A simplified duel engine with HP, distance, and round flow
- Gymnasium environment and action-masking scaffold
- Rule-based baseline AI and PPO trainer wrapper
- Rich terminal CLI as a fallback game mode
- FastAPI endpoints for health/state checks

## Features

- 1v1 mini duel gameplay
- Basic card types: Move, Sword, Gun, Special
- Skill checks: Thunderbolt and Precision Shot
- Simple action mask compatible with RL training
- Minimal CPU-friendly architecture for fast local testing

## Live Game

Run the app:

```bash
cd /workspaces/unlight-rl
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open in browser:

```text
http://localhost:8000/
```

The homepage contains a playable HTML mini-game where you can:

- move forward/backward
- attack
- use skills
- defend
- pass

## API Endpoints

- GET / : playable game page
- GET /health : health check
- GET /state : environment observation snapshot
- POST /step : step the RL environment with an action

Example:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/state
```

## Repository Structure

```text
.
├── README.md
├── requirements.txt
├── main.py
├── config.py
├── engine/
│   ├── __init__.py
│   ├── card.py
│   ├── character.py
│   └── duel.py
├── env/
│   ├── __init__.py
│   └── unlight_gym_env.py
├── agents/
│   ├── __init__.py
│   ├── rule_agent.py
│   └── ppo_agent.py
├── ui/
│   ├── __init__.py
│   └── cli.py
├── tests/
│   └── test_core.py
├── Unlight_RL_AI_MVP_PRD.pdf
└── .gitignore
```

## Quick Start

### 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the game server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4) Run tests

```bash
python -m pytest -q
```

## Notes

- This is an MVP for rapid prototyping, not a full commercial card game.
- The design follows the provided PRD and intentionally keeps CPU usage low.
- The environment is suitable for iterative RL experimentation and UI validation.

## License

For internal prototype and learning use.
