from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response

from env.unlight_gym_env import UnlightGymEnv
from ui.cli import play_human_vs_ai

app = FastAPI(title="Unlight RL MVP")


@app.get("/", response_class=HTMLResponse)
def root() -> str:
    return """
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Unlight RL MVP</title>
      <style>
        :root {
          --bg: #0f172a;
          --panel: #111827;
          --panel-2: #1f2937;
          --text: #e5e7eb;
          --muted: #94a3b8;
          --accent: #38bdf8;
          --danger: #f87171;
          --good: #4ade80;
          --warn: #fbbf24;
        }
        * { box-sizing: border-box; }
        body {
          margin: 0;
          font-family: Arial, sans-serif;
          background: linear-gradient(180deg, #020817, var(--bg));
          color: var(--text);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .game {
          width: min(900px, 92vw);
          background: rgba(17,24,39,0.9);
          border: 1px solid rgba(148,163,184,0.3);
          border-radius: 18px;
          padding: 24px;
          box-shadow: 0 25px 70px rgba(0,0,0,0.45);
        }
        h1 {
          margin: 0 0 12px;
          font-size: clamp(2rem, 4vw, 3rem);
        }
        .status {
          display: grid;
          grid-template-columns: repeat(3, minmax(140px, 1fr));
          gap: 12px;
          margin: 18px 0;
        }
        .card {
          background: var(--panel-2);
          border-radius: 12px;
          padding: 14px;
          border: 1px solid rgba(148,163,184,0.2);
        }
        .label {
          color: var(--muted);
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 0.08em;
        }
        .value {
          font-size: clamp(1.3rem, 2vw, 2rem);
          margin-top: 6px;
          font-weight: 700;
        }
        .controls {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 10px;
          margin-top: 18px;
        }
        button {
          background: linear-gradient(180deg, #0ea5e9, #0369a1);
          border: none;
          color: white;
          border-radius: 10px;
          padding: 12px 14px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: transform 0.15s ease, opacity 0.15s ease;
        }
        button:hover { transform: translateY(-1px); }
        button:disabled {
          opacity: 0.4;
          cursor: not-allowed;
        }
        .log {
          margin-top: 20px;
          background: rgba(15, 23, 42, 0.9);
          border: 1px solid rgba(148,163,184,0.25);
          border-radius: 12px;
          min-height: 80px;
          padding: 14px;
          color: var(--text);
          white-space: pre-wrap;
        }
        .hand {
          margin-top: 18px;
          display: flex;
          gap: 10px;
          flex-wrap: wrap;
        }
        .chip {
          padding: 8px 10px;
          border-radius: 999px;
          background: rgba(56,189,248,0.12);
          border: 1px solid rgba(56,189,248,0.45);
          color: var(--accent);
          font-weight: 700;
        }
      </style>
    </head>
    <body>
      <div class="game">
        <h1>Unlight RL MVP</h1>
        <div class="status">
          <div class="card">
            <div class="label">Player HP</div>
            <div class="value" id="playerHp">10</div>
          </div>
          <div class="card">
            <div class="label">Enemy HP</div>
            <div class="value" id="enemyHp">10</div>
          </div>
          <div class="card">
            <div class="label">Distance</div>
            <div class="value" id="distance">2</div>
          </div>
        </div>
        <div class="hand" id="hand"></div>
        <div class="controls">
          <button data-action="move_forward">Move Forward</button>
          <button data-action="move_back">Move Back</button>
          <button data-action="basic_attack">Basic Attack</button>
          <button data-action="skill_1">Thunderbolt</button>
          <button data-action="skill_2">Precision Shot</button>
          <button data-action="defend">Defend</button>
          <button data-action="pass">Pass</button>
        </div>
        <div class="log" id="log">Round 1. Your turn.</div>
      </div>

      <script>
        const state = {
          playerHp: 10,
          enemyHp: 10,
          distance: 2,
          round: 1,
          hand: {
            Move: 2,
            Sword: 1,
            Gun: 2,
            Special: 1
          },
          log: "Round 1. Your turn."
        };

        const id = (key) => document.getElementById(key);
        const log = (msg) => { id('log').textContent = msg; state.log = msg; };

        function render() {
          id('playerHp').textContent = state.playerHp;
          id('enemyHp').textContent = state.enemyHp;
          id('distance').textContent = state.distance;

          const handEl = id('hand');
          handEl.innerHTML = '';
          Object.entries(state.hand).forEach(([name, count]) => {
            const chip = document.createElement('div');
            chip.className = 'chip';
            chip.textContent = `${name}: ${count}`;
            handEl.appendChild(chip);
          });
        }

        function enemyTurn() {
          const actions = [
            { name: 'basic_attack', uses: 'Sword', value: 2 },
            { name: 'move_forward', uses: 'Move', value: 1 },
            { name: 'defend', uses: 'Defend', value: 1 },
            { name: 'skill_1', uses: 'Special', value: 3 }
          ];
          const choice = actions[Math.floor(Math.random() * actions.length)];
          if (choice.name === 'move_forward') {
            state.distance = Math.max(1, state.distance - 1);
            log('Enemy moves in.');
          } else if (choice.name === 'defend') {
            state.playerHp = Math.min(10, state.playerHp + 1);
            log('Enemy defends and regains 1 HP.');
          } else if (choice.name === 'skill_1') {
            state.playerHp = Math.max(0, state.playerHp - 3);
            log('Enemy casts Thunderbolt for 3 damage.');
          } else {
            state.playerHp = Math.max(0, state.playerHp - 2);
            log('Enemy attacks for 2 damage.');
          }

          if (state.playerHp <= 0) {
            log('Defeat! Enemy wins the duel.');
            document.querySelectorAll('button').forEach(btn => btn.disabled = true);
          } else {
            state.round += 1;
            log(`Round ${state.round}. Your turn.`);
          }

          render();
        }

        function applyPlayerAction(action) {
          if (state.playerHp <= 0 || state.enemyHp <= 0) return;

          if (action === 'move_forward') {
            if (state.hand.Move > 0) {
              state.hand.Move -= 1;
              state.distance = Math.max(1, state.distance - 1);
              log('You move forward.');
            } else {
              log('No Move cards left.');
              return;
            }
          } else if (action === 'move_back') {
            if (state.hand.Move > 0) {
              state.hand.Move -= 1;
              state.distance = Math.min(3, state.distance + 1);
              log('You move back.');
            } else {
              log('No Move cards left.');
              return;
            }
          } else if (action === 'basic_attack') {
            if (state.hand.Sword > 0 || state.hand.Gun > 0) {
              state.enemyHp = Math.max(0, state.enemyHp - (state.distance <= 1 ? 2 : 1));
              if (state.hand.Sword > 0) state.hand.Sword -= 1; else state.hand.Gun -= 1;
              log('You strike the enemy.');
            } else {
              log('You need Sword or Gun cards.');
              return;
            }
          } else if (action === 'skill_1') {
            if (state.hand.Special > 0 && state.hand.Gun >= 2) {
              state.hand.Special -= 1;
              state.hand.Gun -= 2;
              state.enemyHp = Math.max(0, state.enemyHp - 3);
              log('Thunderbolt deals 3 damage.');
            } else {
              log('Thunderbolt requires 1 Special + 2 Gun.');
              return;
            }
          } else if (action === 'skill_2') {
            if (state.hand.Gun >= 3 && state.hand.Sword > 0) {
              state.hand.Gun -= 3;
              state.hand.Sword -= 1;
              state.enemyHp = Math.max(0, state.enemyHp - 2);
              log('Precision Shot deals 2 damage.');
            } else {
              log('Precision Shot requires 3 Gun + 1 Sword.');
              return;
            }
          } else if (action === 'defend') {
            state.playerHp = Math.min(10, state.playerHp + 1);
            log('You defend and recover 1 HP.');
          } else if (action === 'pass') {
            log('You pass the turn.');
          }

          if (state.enemyHp <= 0) {
            log('Victory! You win the duel.');
            document.querySelectorAll('button').forEach(btn => btn.disabled = true);
            render();
            return;
          }

          render();
          setTimeout(enemyTurn, 400);
        }

        document.querySelectorAll('button').forEach((btn) => {
          btn.addEventListener('click', () => applyPlayerAction(btn.dataset.action));
        });

        render();
      </script>
    </body>
    </html>
    """


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
