from __future__ import annotations

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from engine.duel import Duel, DuelAction


console = Console()


def display_state(duel: Duel) -> None:
    table = Table(title="Unlight RL Duel")
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("Self HP", str(duel.state["self_hp"]))
    table.add_row("Opponent HP", str(duel.state["opponent_hp"]))
    table.add_row("Distance", str(duel.state["distance"]))
    table.add_row("Phase", duel.state["phase"])
    table.add_row("Round", str(duel.state["round"]))
    console.print(table)


def play_human_vs_ai() -> None:
    duel = Duel()
    while duel.state["winner"] is None:
        display_state(duel)
        valid = duel.get_action_mask()
        options = [
            (index, name)
            for index, name in enumerate([
                "Pass",
                "Move Forward",
                "Move Back",
                "Basic Attack",
                "Trigger Skill 1",
                "Trigger Skill 2",
                "Sword Strike",
                "Gun Strike",
                "Special Strike",
                "Defend",
                "Reposition",
                "Counter",
                "Risky Attack",
                "Feint",
                "Hold",
                "Draw",
            ])
            if valid[index]
        ]
        if not options:
            action = DuelAction.PASS
        else:
            console.print("Available actions:")
            for idx, name in options:
                console.print(f"  {idx}: {name}")
            choice = Prompt.ask("Choose action", choices=[str(idx) for idx, _ in options])
            action = int(choice)
        duel.resolve_action(action)
        console.print(f"Last action: {action}")
    console.print(f"Winner: {duel.state['winner']}")
