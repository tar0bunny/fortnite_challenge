import json
import random
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.align import Align


COMBAT_PATH = "./challenges/combat.json"
DROP_PATH = "./challenges/drop.json"
LOADOUT_PATH = "./challenges/loadout.json"


def build_challenge_list(path):
    with open(f"{path}", "r") as f:
        data = json.load(f)

    challenges = data["challenges"]
    return challenges


if __name__ == "__main__":
    console = Console()
    all_challenges = build_challenge_list(COMBAT_PATH) \
                    + build_challenge_list(DROP_PATH) \
                    + build_challenge_list(LOADOUT_PATH)
    challenge = random.choice(all_challenges)

    with console.status(
        "[bold cyan]GENERATING CHALLENGE[/bold cyan]...",
        spinner="dots"
    ):
        sleep(2)

    panel = Panel(
        f"\nID:\t\t{challenge['id']}\nChallenge:\t{challenge['text']}\nDifficulty:\t{challenge['difficulty']}\n",
        title="[bold red]ACTIVE CHALLENGE[/bold red]",
        title_align="left",
        border_style="red"
    )

    console.print(panel)