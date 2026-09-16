# Unlight RL MVP

A browser-playable RL card duel prototype inspired by Unlight, built for fast local testing and CPU-friendly experimentation in Codespaces.

This project includes:

- A playable HTML duel interface at the root route
- Turn-based combat with HP, distance, and round tracking
- Card-based actions: Move, Sword, Gun, Special
- Two skill actions: Thunderbolt and Precision Shot
- Gymnasium-style environment scaffold for RL development
- Baseline AI and PPO training wrapper structure
- FastAPI health/state endpoints

## What’s Included

- Browser duel page with buttons and turn flow
- Simple enemy AI response loop
- Card count tracking and hand display
- Action gating to model valid moves
- Minimal RL-ready environment for future training iteration

## How to Run

```bash
cd /workspaces/unlight-rl
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open:

```text
http://localhost:8000/
```

You will see a playable mini duel page where you can:

- move forward/backward
- attack
- use special skills
- defend
- pass the turn

## API Endpoints

- GET / : playable browser game page
- GET /health : returns server health state
- GET /state : returns the RL observation state
- POST /step : sends an action to the environment

## Project Structure

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
├── .gitignore
└── .venv/
```

## Quick Start

### 1) Create environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Start the game

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4) Run tests

```bash
python -m pytest -q
```

## Notes

- This is a lean MVP for fast iteration.
- It is built to align with the PRD while remaining lightweight enough for local CPU-only experimentation.
- It is intentionally modular so the logic can be expanded into deeper card effects, richer AI, and full RL training later.

## License

For internal prototype and educational/demo use.
