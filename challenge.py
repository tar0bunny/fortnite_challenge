import random
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

drop_challenges = [
    "Land at named location only",
    "Edge of map landing",
    "Pop glider immediately",
    "Land at closest named location from bus starting point",
]

combat_challenges = [
    "No healing allowed",
    "Must reload after each elimination",
    "No sprinting unless in the storm",
    "No aiming down sights"
]

loadout_challenges = [
    "No shotguns",
    "SMGs only",
    "Gray guns only",
    "Shotguns only",
    "Must carry 2 heals at all times",
    "No movement items"
]


if __name__ == "__main__":
    console = Console()
    all_challenges = drop_challenges + combat_challenges + loadout_challenges
    challenge = random.choice(all_challenges)

    with console.status(
        "[bold cyan]GENERATING CHALLENGE[/bold cyan]...",
        spinner="dots"
    ):
        sleep(2)

    panel = Panel(
        Align.left(f"[bold]\n{challenge}\n[/bold]", vertical="middle"),
        title="[bold red]ACTIVE CHALLENGE[/bold red]",
        title_align="left",
        border_style="red"
    )

    console.print(panel)