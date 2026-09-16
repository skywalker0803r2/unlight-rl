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
          --bg: #07111f;
          --panel: #0f172a;
          --panel-2: #172033;
          --panel-3: #1e293b;
          --text: #e2e8f0;
          --muted: #94a3b8;
          --accent: #38bdf8;
          --good: #4ade80;
          --danger: #f87171;
          --warn: #fbbf24;
          --shadow: rgba(0,0,0,0.35);
        }
        * { box-sizing: border-box; }
        html, body {
          margin: 0;
          min-height: 100%;
          font-family: Arial, sans-serif;
          background: radial-gradient(circle at top, #12253d 0%, #07111f 40%, #020817 100%);
          color: var(--text);
        }
        body {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 24px;
        }
        .game {
          width: min(1100px, 95vw);
          background: rgba(15, 23, 42, 0.94);
          border: 1px solid rgba(148, 163, 184, 0.25);
          border-radius: 22px;
          padding: 24px;
          box-shadow: 0 30px 80px var(--shadow);
        }
        .topbar {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 12px;
          margin-bottom: 18px;
          flex-wrap: wrap;
        }
        h1 {
          margin: 0;
          font-size: clamp(2rem, 3vw, 2.7rem);
          letter-spacing: 0.04em;
        }
        button {
          border: none;
          border-radius: 10px;
          padding: 12px 16px;
          font-weight: 700;
          cursor: pointer;
          background: linear-gradient(180deg, var(--accent), #0369a1);
          color: white;
          transition: transform 0.15s ease, opacity 0.15s ease;
        }
        button:hover { transform: translateY(-2px); }
        button:disabled { opacity: 0.4; pointer-events: none; }
        .status-row {
          display: grid;
          grid-template-columns: repeat(4, minmax(140px, 1fr));
          gap: 12px;
          margin-bottom: 18px;
        }
        .panel {
          background: linear-gradient(180deg, var(--panel-2), var(--panel-3));
          border: 1px solid rgba(148, 163, 184, 0.28);
          border-radius: 14px;
          padding: 14px;
        }
        .label {
          font-size: 12px;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--muted);
          margin-bottom: 6px;
        }
        .value {
          font-weight: 800;
          font-size: clamp(1.4rem, 2vw, 2.1rem);
        }
        .battlefield {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 18px;
          margin-top: 8px;
        }
        .arena {
          background: rgba(15, 23, 42, 0.7);
          border: 1px solid rgba(148, 163, 184, 0.22);
          border-radius: 16px;
          padding: 18px;
        }
        .fighter {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 18px;
          font-size: 1rem;
        }
        .badge {
          display: inline-block;
          padding: 6px 10px;
          border-radius: 999px;
          background: rgba(56,189,248,0.12);
          color: var(--accent);
          border: 1px solid rgba(56,189,248,0.3);
          font-size: 0.72rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.08em;
        }
        .hand {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          min-height: 52px;
          margin: 10px 0 18px;
        }
        .chip {
          background: rgba(56,189,248,0.06);
          border: 1px solid rgba(56,189,248,0.38);
          color: var(--accent);
          border-radius: 999px;
          padding: 8px 12px;
          font-weight: 700;
        }
        .controls {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 10px;
          margin-top: 16px;
        }
        .log {
          margin-top: 20px;
          background: rgba(2, 8, 23, 0.7);
          border-radius: 12px;
          border: 1px solid rgba(148, 163, 184, 0.25);
          min-height: 92px;
          padding: 14px;
          color: var(--text);
          white-space: pre-wrap;
        }
        .small { color: var(--muted); font-size: 0.82rem; }
      </style>
    </head>
    <body>
      <div class="game">
        <div class="topbar">
          <h1>Unlight RL MVP</h1>
          <button id="resetBtn">New Duel</button>
        </div>

        <div class="status-row">
          <div class="panel">
            <div class="label">Player HP</div>
            <div class="value" id="playerHp">10</div>
          </div>
          <div class="panel">
            <div class="label">Enemy HP</div>
            <div class="value" id="enemyHp">10</div>
          </div>
          <div class="panel">
            <div class="label">Distance</div>
            <div class="value" id="distance">2</div>
          </div>
          <div class="panel">
            <div class="label">Round</div>
            <div class="value" id="round">1</div>
          </div>
        </div>

        <div class="battlefield">
          <div class="arena">
            <div class="fighter">
              <strong>Player</strong>
              <span class="badge">YOU</span>
            </div>
            <div class="small">Hand:</div>
            <div class="hand" id="playerHand"></div>
          </div>

          <div class="arena">
            <div class="fighter">
              <strong>Enemy</strong>
              <span class="badge">BOT</span>
            </div>
            <div class="small">Enemy cards in hand:</div>
            <div class="hand" id="enemyHand"></div>
          </div>
        </div>

        <div class="controls">
          <button data-action="move_forward">Move Forward</button>
          <button data-action="move_back">Move Back</button>
          <button data-action="basic_attack">Basic Attack</button>
          <button data-action="skill_1">Thunderbolt</button>
          <button data-action="skill_2">Precision Shot</button>
          <button data-action="defend">Defend</button>
          <button data-action="pass">Pass</button>
        </div>

        <div class="log" id="log">Round 1. Your turn. Select an action.</div>
      </div>

      <script>
        const deckTypes = ['Move', 'Sword', 'Gun', 'Special'];

        const state = {
          playerHp: 10,
          enemyHp: 10,
          distance: 2,
          round: 1,
          playerHand: [],
          enemyHand: [],
          log: 'Round 1. Your turn. Select an action.',
          lock: false
        };

        function getRandomCard() {
          return deckTypes[Math.floor(Math.random() * deckTypes.length)];
        }

        function countHand(hand, type) {
          return hand.filter(card => card === type).length;
        }

        function makeDeck() {
          const deck = [];
          for (let i = 0; i < 5; i++) deck.push('Move');
          for (let i = 0; i < 3; i++) deck.push('Sword');
          for (let i = 0; i < 3; i++) deck.push('Gun');
          for (let i = 0; i < 2; i++) deck.push('Special');
          return deck;
        }

        function drawToHand(target, deck) {
          while (target.length < 6 && deck.length > 0) {
            const index = Math.floor(Math.random() * deck.length);
            target.push(deck.splice(index, 1)[0]);
          }
        }

        function initGame() {
          const deck = makeDeck();
          state.playerHp = 10;
          state.enemyHp = 10;
          state.distance = 2;
          state.round = 1;
          state.playerHand = [];
          state.enemyHand = [];
          state.lock = false;
          drawToHand(state.playerHand, deck);
          drawToHand(state.enemyHand, deck);
          state.log = 'Round 1. Your turn. Select an action.';
          render();
        }

        function id(key) { return document.getElementById(key); }

        function setLog(msg) {
          state.log = msg;
          id('log').textContent = msg;
        }

        function isActionAllowed(action) {
          const hand = state.playerHand;
          if (action === 'move_forward' || action === 'move_back') return countHand(hand, 'Move') > 0;
          if (action === 'basic_attack') return countHand(hand, 'Sword') > 0 || countHand(hand, 'Gun') > 0;
          if (action === 'skill_1') return countHand(hand, 'Special') > 0 && countHand(hand, 'Gun') >= 2;
          if (action === 'skill_2') return countHand(hand, 'Gun') >= 3 && countHand(hand, 'Sword') > 0;
          if (action === 'defend') return true;
          if (action === 'pass') return true;
          return false;
        }

        function removeCard(type) {
          const idx = state.playerHand.indexOf(type);
          if (idx >= 0) state.playerHand.splice(idx, 1);
        }

        function enemyTurn() {
          if (state.playerHp <= 0 || state.enemyHp <= 0) return;

          const enemyActions = [
            { action: 'basic_attack', label: 'Enemy attacks' },
            { action: 'move_forward', label: 'Enemy advances' },
            { action: 'skill_1', label: 'Enemy uses Thunderbolt' },
            { action: 'defend', label: 'Enemy defends' }
          ];

          const choice = enemyActions[Math.floor(Math.random() * enemyActions.length)];
          let message = choice.label;

          if (choice.action === 'move_forward') {
            state.distance = Math.max(1, state.distance - 1);
          } else if (choice.action === 'defend') {
            state.enemyHp = Math.min(10, state.enemyHp + 1);
          } else if (choice.action === 'skill_1') {
            if (countHand(state.enemyHand, 'Special') > 0 && countHand(state.enemyHand, 'Gun') >= 2) {
              removeCardByType(state.enemyHand, 'Special');
              removeCardByType(state.enemyHand, 'Gun');
              removeCardByType(state.enemyHand, 'Gun');
              state.playerHp = Math.max(0, state.playerHp - 3);
              message = 'Enemy uses Thunderbolt for 3 damage.';
            } else {
              state.playerHp = Math.max(0, state.playerHp - 2);
              message = 'Enemy attacks for 2 damage.';
            }
          } else {
            state.playerHp = Math.max(0, state.playerHp - 2);
            message = 'Enemy attacks for 2 damage.';
          }

          if (state.playerHp <= 0) {
            setLog('Defeat! Enemy wins the duel.');
            state.lock = true;
            render();
            return;
          }

          state.round += 1;
          setLog(message + ' Your turn.');
          state.lock = false;
          render();
        }

        function removeCardByType(hand, type) {
          const idx = hand.indexOf(type);
          if (idx >= 0) hand.splice(idx, 1);
        }

        function render() {
          id('playerHp').textContent = state.playerHp;
          id('enemyHp').textContent = state.enemyHp;
          id('distance').textContent = state.distance;
          id('round').textContent = state.round;
          id('log').textContent = state.log;

          renderHand('playerHand', state.playerHand);
          renderHand('enemyHand', state.enemyHand);

          document.querySelectorAll('[data-action]').forEach(button => {
            const action = button.dataset.action;
            button.disabled = state.lock || !isActionAllowed(action);
          });
        }

        function renderHand(elementId, hand) {
          const el = id(elementId);
          el.innerHTML = '';
          if (!hand.length) {
            const noCard = document.createElement('div');
            noCard.className = 'chip';
            noCard.textContent = 'Empty';
            el.appendChild(noCard);
            return;
          }
          hand.forEach((card, index) => {
            const chip = document.createElement('div');
            chip.className = 'chip';
            chip.textContent = `${card} #${index + 1}`;
            el.appendChild(chip);
          });
        }

        function applyPlayerAction(action) {
          if (state.lock || state.playerHp <= 0 || state.enemyHp <= 0) return;
          if (!isActionAllowed(action)) {
            setLog('That action is not available right now.');
            render();
            return;
          }

          state.lock = true;

          if (action === 'move_forward') {
            removeCardByType(state.playerHand, 'Move');
            state.distance = Math.max(1, state.distance - 1);
            setLog('You move forward and close the gap.');
          } else if (action === 'move_back') {
            removeCardByType(state.playerHand, 'Move');
            state.distance = Math.min(3, state.distance + 1);
            setLog('You step back to create space.');
          } else if (action === 'basic_attack') {
            const damage = state.distance <= 1 ? 2 : 1;
            if (countHand(state.playerHand, 'Sword') > 0) {
              removeCardByType(state.playerHand, 'Sword');
            } else {
              removeCardByType(state.playerHand, 'Gun');
            }
            state.enemyHp = Math.max(0, state.enemyHp - damage);
            setLog(`You attack for ${damage} damage.`);
          } else if (action === 'skill_1') {
            removeCardByType(state.playerHand, 'Special');
            removeCardByType(state.playerHand, 'Gun');
            removeCardByType(state.playerHand, 'Gun');
            state.enemyHp = Math.max(0, state.enemyHp - 3);
            setLog('Thunderbolt lands for 3 damage.');
          } else if (action === 'skill_2') {
            removeCardByType(state.playerHand, 'Gun');
            removeCardByType(state.playerHand, 'Gun');
            removeCardByType(state.playerHand, 'Gun');
            removeCardByType(state.playerHand, 'Sword');
            state.enemyHp = Math.max(0, state.enemyHp - 2);
            setLog('Precision Shot lands for 2 damage.');
          } else if (action === 'defend') {
            state.playerHp = Math.min(10, state.playerHp + 1);
            setLog('You defend and recover 1 HP.');
          } else if (action === 'pass') {
            setLog('You pass the turn.');
          }

          if (state.enemyHp <= 0) {
            setLog('Victory! You defeat the enemy.');
            render();
            return;
          }

          render();
          setTimeout(enemyTurn, 500);
        }

        document.querySelectorAll('[data-action]').forEach(button => {
          button.addEventListener('click', () => applyPlayerAction(button.dataset.action));
        });

        document.getElementById('resetBtn').addEventListener('click', initGame);
        initGame();
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
