import json
import random
import sys
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.align import Align


COMBAT_PATH = "./challenges/combat.json"
DROP_PATH = "./challenges/drop.json"
LOADOUT_PATH = "./challenges/loadout.json"
STATS_PATH = "./stats.json"


def build_challenge_list(path):
    with open(f"{path}", "r") as f:
        data = json.load(f)

    challenges = data["challenges"]
    return challenges


def load_stats():
    with open(STATS_PATH, "r") as f:
        return json.load(f)


def save_stats(stats):
    with open(STATS_PATH, "w") as f:
        json.dump(stats, f, indent=4)


if __name__ == "__main__":
    console = Console()

    # Build challenge pool
    all_challenges = (
        build_challenge_list(COMBAT_PATH)
        + build_challenge_list(DROP_PATH)
        + build_challenge_list(LOADOUT_PATH)
    )

    challenge = random.choice(all_challenges)

    # Loading animation
    with console.status(
        "[bold cyan]GENERATING CHALLENGE[/bold cyan]...",
        spinner="dots"
    ):
        sleep(2)


    # Active Challenge Panel
    challenge_panel = Panel(
        f"\n[bold yellow]CATEGORY[/bold yellow]     [cyan]{challenge['id']}[/cyan]\n"
        f"[bold yellow]CHALLENGE[/bold yellow]    [white]{challenge['text']}[/white]\n"
        f"[bold yellow]DIFFICULTY[/bold yellow]   "
        f"[bold yellow]{'★ ' * challenge['difficulty']}[bold yellow]\n",
        title="[bold red]⚠ ACTIVE CHALLENGE ⚠[/bold red]",
        title_align="center",
        border_style="bold red",
        padding=(1, 2)
    )

    console.print(challenge_panel)

    # Load stats
    stats = load_stats()

    # Stats Panel
    stats_panel = Panel(
        f"\n[bold green]🏆 Wins:[/bold green]   {stats['wins']}\n"
        f"[bold red]💀 Losses:[/bold red] {stats['losses']}\n",
        title="[bold cyan]📊 RECORD[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )

    console.print(stats_panel)

    # Ask for result
    result = input("\nDid you win? (y/n/c): ").strip().lower()

    if result == "y":
        stats["wins"] += 1
        console.print("[bold green]WIN RECORDED![/bold green]")
    elif result == "n":
        stats["losses"] += 1
        console.print("[bold red]LOSS RECORDED![/bold red]")
    elif result == "c":
        console.print("[bold yellow]Challenge cancelled. No changes made.[/bold yellow]")
        sys.exit()
    else:
        console.print("[yellow]Invalid input. No result recorded.[/yellow]")

    save_stats(stats)

    # Reload + Display Updated Stats
    updated_stats = load_stats()

    updated_panel = Panel(
        f"\n[bold green]🏆 Wins:[/bold green]   {updated_stats['wins']}\n"
        f"[bold red]💀 Losses:[/bold red] {updated_stats['losses']}\n",
        title="[bold cyan]📊 UPDATED RECORD[/bold cyan]",
        border_style="bold cyan",
        padding=(1, 2)
    )

    console.print(updated_panel)
