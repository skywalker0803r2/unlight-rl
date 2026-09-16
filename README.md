# Unlight RL AI MVP

A lean Reinforcement Learning card-duel MVP inspired by Unlight, built for fast CPU-only execution in GitHub Codespaces.

This project includes:

- A simplified turn-based 1v1 duel engine
- Gymnasium environment integration
- Action-masked PPO training scaffolding
- Rule-based baseline bot
- Rich terminal CLI
- FastAPI health and state endpoints

## Project Goals

This repository follows the PRD in Unlight_RL_AI_MVP_PRD.pdf and focuses on a minimal but runnable MVP with a small footprint suitable for CPU training and local experimentation.

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
└── Unlight_RL_AI_MVP_PRD.pdf
```

## Quick Start

### 1) Create and activate a Python environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the CLI demo

```bash
python main.py
```

### 4) Run the API locally

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open:

- http://localhost:8000/health
- http://localhost:8000/state

## Sample API

```bash
curl http://localhost:8000/health
curl http://localhost:8000/state
```

## Testing

```bash
python -m pytest -q
```

## Notes

- Training is intentionally lightweight for CPU-only Codespace usage.
- The environment exposes a simple action mask for fast PPO-compatible training.
- The project is intentionally a design-first MVP and can be extended with deeper duel logic, richer card effects, and stronger self-play training.

## License

This project is intended for internal MVP development and experimentation.
