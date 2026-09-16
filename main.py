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
          --bg: #050b14;
          --bg-2: #0d1b2a;
          --panel: rgba(15, 23, 42, 0.96);
          --panel-2: rgba(21, 33, 53, 0.96);
          --line: rgba(148, 163, 184, 0.2);
          --text: #e5eefc;
          --muted: #9fb5d1;
          --blue: #4ecbff;
          --cyan: #7dd3fc;
          --violet: #9b8cff;
          --gold: #f7c866;
          --red: #ff6b6b;
          --green: #66d9a6;
          --shadow: rgba(0,0,0,0.45);
        }
        * { box-sizing: border-box; }
        html, body {
          margin: 0;
          min-height: 100%;
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          color: var(--text);
          background: radial-gradient(circle at top, #12233e 0%, #081320 32%, #040a12 100%);
        }
        body {
          padding: 24px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .game-shell {
          width: min(1200px, 96vw);
          background: rgba(8, 15, 24, 0.82);
          border: 1px solid var(--line);
          border-radius: 24px;
          box-shadow: 0 28px 80px var(--shadow);
          overflow: hidden;
        }
        .topbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 20px 22px;
          background: linear-gradient(180deg, rgba(18,32,49,0.9), rgba(9,17,28,0.96));
          border-bottom: 1px solid var(--line);
        }
        .brand {
          display: flex;
          align-items: baseline;
          gap: 10px;
        }
        h1 {
          margin: 0;
          font-size: clamp(2rem, 3vw, 2.9rem);
          letter-spacing: 0.05em;
          color: var(--text);
          font-weight: 800;
        }
        .subtitle {
          color: var(--muted);
          letter-spacing: 0.18em;
          text-transform: uppercase;
          font-size: 0.75rem;
        }
        .new-duel {
          border: 1px solid rgba(125, 211, 252, 0.32);
          background: linear-gradient(180deg, rgba(78, 203, 255, 0.16), rgba(19, 85, 115, 0.14));
          color: var(--text);
          border-radius: 12px;
          padding: 10px 16px;
          font-weight: 700;
          cursor: pointer;
        }
        .board {
          padding: 20px 22px 18px;
        }
        .meters {
          display: grid;
          grid-template-columns: repeat(4, minmax(160px, 1fr));
          gap: 14px;
          margin-bottom: 18px;
        }
        .meter {
          background: linear-gradient(180deg, var(--panel), var(--panel-2));
          border: 1px solid var(--line);
          border-radius: 16px;
          padding: 14px 16px;
        }
        .meter-label {
          font-size: 0.72rem;
          text-transform: uppercase;
          letter-spacing: 0.14em;
          color: var(--muted);
        }
        .meter-value {
          margin-top: 8px;
          font-size: clamp(1.4rem, 2vw, 2rem);
          font-weight: 800;
        }
        .battlefield {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
          margin-bottom: 20px;
        }
        .fighter-panel {
          background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(17, 24, 39, 0.9));
          border: 1px solid var(--line);
          border-radius: 18px;
          padding: 16px 18px;
          min-height: 240px;
        }
        .fighter-top {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 14px;
        }
        .fighter-name {
          font-size: 1.1rem;
          font-weight: 700;
        }
        .role-badge {
          padding: 6px 10px;
          border-radius: 999px;
          background: rgba(125, 211, 252, 0.10);
          border: 1px solid rgba(125, 211, 252, 0.35);
          color: var(--blue);
          font-size: 0.72rem;
          letter-spacing: 0.12em;
          text-transform: uppercase;
        }
        .hp-bar {
          height: 18px;
          background: rgba(255,255,255,0.06);
          border-radius: 999px;
          overflow: hidden;
          border: 1px solid rgba(255,255,255,0.06);
          margin: 8px 0 18px;
        }
        .hp-fill {
          height: 100%;
          width: 100%;
          background: linear-gradient(90deg, var(--green), #8ee2b4);
          transition: width 0.25s ease;
        }
        .hp-fill.enemy { background: linear-gradient(90deg, var(--red), #ff9d9d); }
        .card-row {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          min-height: 78px;
        }
        .card-chip {
          background: linear-gradient(180deg, rgba(24, 38, 61, 0.9), rgba(12, 22, 36, 0.9));
          border: 1px solid rgba(125, 211, 252, 0.28);
          color: var(--text);
          border-radius: 12px;
          padding: 10px 12px;
          min-width: 96px;
          text-align: center;
          box-shadow: inset 0 0 18px rgba(125, 211, 252, 0.04);
        }
        .card-chip.move { border-color: rgba(125, 211, 252, 0.4); }
        .card-chip.sword { border-color: rgba(247, 200, 102, 0.45); }
        .card-chip.gun { border-color: rgba(155, 140, 255, 0.45); }
        .card-chip.special { border-color: rgba(255, 107, 107, 0.45); }
        .card-chip .type { display: block; font-size: 0.64rem; letter-spacing: 0.12em; color: var(--muted); margin-bottom: 4px; }
        .card-chip .name { font-weight: 700; }

        .battle-center {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 10px 0;
        }
        .range-indicator {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 140px;
          height: 140px;
          border-radius: 50%;
          border: 1px solid rgba(125, 211, 252, 0.3);
          background: radial-gradient(circle, rgba(78, 203, 255, 0.18), rgba(13, 27, 42, 0.6));
          position: relative;
          box-shadow: inset 0 0 38px rgba(125,211,252,0.08);
        }
        .range-indicator::before,
        .range-indicator::after {
          content: "";
          position: absolute;
          border-radius: 50%;
          border: 1px solid rgba(125, 211, 252, 0.22);
        }
        .range-indicator::before { width: 90px; height: 90px; }
        .range-indicator::after { width: 52px; height: 52px; }
        .range-value {
          position: relative;
          z-index: 1;
          font-size: 2.4rem;
          font-weight: 800;
          color: var(--blue);
        }

        .action-panel {
          background: linear-gradient(180deg, rgba(16, 24, 36, 0.96), rgba(8, 15, 24, 0.96));
          border: 1px solid var(--line);
          border-radius: 18px;
          padding: 18px;
        }
        .action-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 12px;
          margin-top: 6px;
        }
        .action-btn {
          min-height: 58px;
          border-radius: 12px;
          border: 1px solid rgba(125, 211, 252, 0.28);
          background: linear-gradient(180deg, rgba(13, 27, 42, 0.9), rgba(18, 32, 49, 0.75));
          color: var(--text);
          font-weight: 700;
          cursor: pointer;
          padding: 10px;
        }
        .action-btn:hover:not(:disabled) {
          transform: translateY(-1px);
          border-color: rgba(125, 211, 252, 0.55);
        }
        .action-btn:disabled {
          opacity: 0.28;
          cursor: not-allowed;
        }
        .logbox {
          margin-top: 18px;
          min-height: 88px;
          background: rgba(2, 8, 23, 0.7);
          border: 1px solid rgba(148, 163, 184, 0.18);
          border-radius: 14px;
          padding: 12px 14px;
          color: var(--text);
          line-height: 1.6;
        }
      </style>
    </head>
    <body>
      <div class="game-shell">
        <div class="topbar">
          <div class="brand">
            <h1>Unlight</h1>
            <span class="subtitle">RL Duel Prototype</span>
          </div>
          <button class="new-duel" id="resetBtn">New Duel</button>
        </div>

        <div class="board">
          <div class="meters">
            <div class="meter">
              <div class="meter-label">Player HP</div>
              <div class="meter-value" id="playerHp">10</div>
            </div>
            <div class="meter">
              <div class="meter-label">Enemy HP</div>
              <div class="meter-value" id="enemyHp">10</div>
            </div>
            <div class="meter">
              <div class="meter-label">Distance</div>
              <div class="meter-value" id="distance">2</div>
            </div>
            <div class="meter">
              <div class="meter-label">Round</div>
              <div class="meter-value" id="round">1</div>
            </div>
          </div>

          <div class="battlefield">
            <div class="fighter-panel">
              <div class="fighter-top">
                <div class="fighter-name">Ebert</div>
                <span class="role-badge">Player</span>
              </div>
              <div class="hp-bar"><div class="hp-fill" id="playerHpBar"></div></div>
              <div class="card-row" id="playerHand"></div>
            </div>

            <div class="fighter-panel">
              <div class="fighter-top">
                <div class="fighter-name">Ebert</div>
                <span class="role-badge">Enemy</span>
              </div>
              <div class="hp-bar"><div class="hp-fill enemy" id="enemyHpBar"></div></div>
              <div class="card-row" id="enemyHand"></div>
            </div>
          </div>

          <div class="battle-center">
            <div class="range-indicator"><div class="range-value" id="rangeValue">2</div></div>
          </div>

          <div class="action-panel">
            <div class="action-grid">
              <button class="action-btn" data-action="move_forward">Move Forward</button>
              <button class="action-btn" data-action="move_back">Move Back</button>
              <button class="action-btn" data-action="basic_attack">Basic Attack</button>
              <button class="action-btn" data-action="skill_1">Thunderbolt</button>
              <button class="action-btn" data-action="skill_2">Precision Shot</button>
              <button class="action-btn" data-action="defend">Defend</button>
              <button class="action-btn" data-action="pass">Pass</button>
            </div>
            <div class="logbox" id="log">Round 1. Your turn. Select an action.</div>
          </div>
        </div>
      </div>

      <script>
        const cardTypes = ['Move', 'Sword', 'Gun', 'Special'];

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
            const idx = Math.floor(Math.random() * deck.length);
            target.push(deck.splice(idx, 1)[0]);
          }
        }

        function setLog(msg) {
          state.log = msg;
          document.getElementById('log').textContent = msg;
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
          setLog('Round 1. Your turn. Select an action.');
          render();
        }

        function removeCardByType(hand, type) {
          const idx = hand.indexOf(type);
          if (idx >= 0) hand.splice(idx, 1);
        }

        function isActionAllowed(action) {
          const hand = state.playerHand;
          if (action === 'move_forward' || action === 'move_back') return countHand(hand, 'Move') > 0;
          if (action === 'basic_attack') return countHand(hand, 'Sword') > 0 || countHand(hand, 'Gun') > 0;
          if (action === 'skill_1') return countHand(hand, 'Special') > 0 && countHand(hand, 'Gun') >= 2;
          if (action === 'skill_2') return countHand(hand, 'Gun') >= 3 && countHand(hand, 'Sword') > 0;
          return true;
        }

        function makeCardNode(type, index) {
          const el = document.createElement('div');
          const cls = type.toLowerCase();
          el.className = `card-chip ${cls}`;
          el.innerHTML = `<span class="type">${type}</span><span class="name">${type === 'Move' ? 'MOVE' : type === 'Sword' ? 'SWORD' : type === 'Gun' ? 'GUN' : 'SPECIAL'}</span>`;
          return el;
        }

        function renderHand(containerId, hand) {
          const container = document.getElementById(containerId);
          container.innerHTML = '';
          if (!hand.length) {
            const empty = document.createElement('div');
            empty.className = 'card-chip';
            empty.innerHTML = '<span class="type">EMPTY</span><span class="name">-</span>';
            container.appendChild(empty);
            return;
          }
          hand.forEach((card) => container.appendChild(makeCardNode(card, 1)));
        }

        function render() {
          document.getElementById('playerHp').textContent = state.playerHp;
          document.getElementById('enemyHp').textContent = state.enemyHp;
          document.getElementById('distance').textContent = state.distance;
          document.getElementById('round').textContent = state.round;
          document.getElementById('rangeValue').textContent = state.distance;
          document.getElementById('playerHpBar').style.width = `${(state.playerHp / 10) * 100}%`;
          document.getElementById('enemyHpBar').style.width = `${(state.enemyHp / 10) * 100}%`;

          renderHand('playerHand', state.playerHand);
          renderHand('enemyHand', state.enemyHand);

          document.querySelectorAll('.action-btn').forEach((btn) => {
            const action = btn.dataset.action;
            btn.disabled = state.lock || !isActionAllowed(action);
          });

          document.getElementById('log').textContent = state.log;
        }

        function enemyTurn() {
          if (state.playerHp <= 0 || state.enemyHp <= 0) return;

          const actions = [
            { action: 'basic_attack', label: 'Enemy attacks' },
            { action: 'move_forward', label: 'Enemy closes the distance' },
            { action: 'defend', label: 'Enemy defends' },
            { action: 'skill_1', label: 'Enemy channels Thunderbolt' }
          ];

          const choice = actions[Math.floor(Math.random() * actions.length)];
          let msg = choice.label;

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
              msg = 'Enemy uses Thunderbolt for 3 damage.';
            } else {
              state.playerHp = Math.max(0, state.playerHp - 2);
              msg = 'Enemy attacks for 2 damage.';
            }
          } else {
            state.playerHp = Math.max(0, state.playerHp - 2);
            msg = 'Enemy attacks for 2 damage.';
          }

          if (state.playerHp <= 0) {
            state.lock = true;
            setLog('Defeat! The enemy wins the duel.');
            render();
            return;
          }

          state.round += 1;
          state.lock = false;
          setLog(msg + ' Your turn.');
          render();
        }

        function applyPlayerAction(action) {
          if (state.lock || state.playerHp <= 0 || state.enemyHp <= 0) return;
          if (!isActionAllowed(action)) {
            setLog('Action unavailable.');
            render();
            return;
          }

          state.lock = true;

          if (action === 'move_forward') {
            removeCardByType(state.playerHand, 'Move');
            state.distance = Math.max(1, state.distance - 1);
            setLog('You move forward and pressure the enemy.');
          } else if (action === 'move_back') {
            removeCardByType(state.playerHand, 'Move');
            state.distance = Math.min(3, state.distance + 1);
            setLog('You reposition to gain distance.');
          } else if (action === 'basic_attack') {
            const damage = state.distance <= 1 ? 2 : 1;
            if (countHand(state.playerHand, 'Sword') > 0) removeCardByType(state.playerHand, 'Sword');
            else removeCardByType(state.playerHand, 'Gun');
            state.enemyHp = Math.max(0, state.enemyHp - damage);
            setLog(`You deal ${damage} damage.`);
          } else if (action === 'skill_1') {
            removeCardByType(state.playerHand, 'Special');
            removeCardByType(state.playerHand, 'Gun');
            removeCardByType(state.playerHand, 'Gun');
            state.enemyHp = Math.max(0, state.enemyHp - 3);
            setLog('Thunderbolt hits for 3 damage.');
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
            setLog('Victory! The enemy is down.');
            render();
            return;
          }

          render();
          setTimeout(enemyTurn, 550);
        }

        document.getElementById('resetBtn').addEventListener('click', initGame);
        document.querySelectorAll('.action-btn').forEach((button) => {
          button.addEventListener('click', () => applyPlayerAction(button.dataset.action));
        });

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
