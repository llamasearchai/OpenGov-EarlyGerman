"""Command-line interface for OpenGov-EarlyGerman."""

from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from pathlib import Path

from opengov_earlygerman import __version__
from opengov_earlygerman.ai.conversation import AIConversationPartner
from opengov_earlygerman.core.cases_teacher import CasesTeacher
from opengov_earlygerman.core.verb_conjugator import VerbConjugator
from opengov_earlygerman.core.word_order import WordOrderTeacher

app = typer.Typer(help="OpenGov-EarlyGerman - AI-powered German language learning")
console = Console()


# Enums for validated choices
from enum import Enum


class Gender(str, Enum):
    masculine = "masculine"
    feminine = "feminine"
    neuter = "neuter"


class Tense(str, Enum):
    present = "present"
    preterite = "preterite"
    past = "past"  # alias for preterite


class Scenario(str, Enum):
    pass  # dynamic scenarios now supported; enum kept for compatibility


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"OpenGov-EarlyGerman version {__version__}", style="bold green")


@app.command()
def case(case_name: str) -> None:
    """Explain a German grammatical case."""
    teacher = CasesTeacher()
    explanation = teacher.explain_case(case_name)

    if "error" in explanation:
        console.print(f"[red]Error: {explanation['error']}[/red]")
        return

    console.print(
        Panel(
            f"[bold]{explanation['explanation']}[/bold]\n\n"
            f"Function: {explanation['function']}\n"
            f"Question: {explanation['question']}",
            title=f"German Case: {case_name.title()}",
            border_style="green",
        )
    )

    console.print("\n[bold cyan]Examples:[/bold cyan]")
    for example in explanation["examples"]:
        console.print(f"  [yellow]{example['german']}[/yellow]")
        console.print(f"  {example['english']}\n")

    console.print("[bold cyan]Tips:[/bold cyan]")
    for tip in explanation["tips"]:
        console.print(f"  - {tip}")


@app.command()
def articles(
    noun: str,
    gender: Gender = typer.Option(Gender.masculine, "--gender", "-g", help="Grammatical gender"),
) -> None:
    """Practice article declension for a noun."""
    teacher = CasesTeacher()
    practice = teacher.practice_articles(noun, gender.value)

    if "error" in practice:
        console.print(f"[red]Error: {practice['error']}[/red]")
        return

    table = Table(title=f"Declension of '{noun}' ({gender.value})")
    table.add_column("Case", style="cyan", no_wrap=True)
    table.add_column("Definite", style="magenta")
    table.add_column("Indefinite", style="green")

    for case, forms in practice["declension_table"].items():
        table.add_row(case.title(), forms["definite"], forms["indefinite"])

    console.print(table)
    console.print(f"\n[italic]{practice['tip']}[/italic]")


@app.command()
def conjugate(
    verb: str,
    tense: Tense = typer.Option(Tense.present, "--tense", help="Tense: present or preterite (alias: past)"),
) -> None:
    """Conjugate a German verb.

    Tense options: present, preterite (alias: past)
    """
    conjugator = VerbConjugator()

    # Accept common alias
    tense_aliases = {"past": "preterite"}
    normalized_tense = tense_aliases.get(tense.value, tense.value)

    result = conjugator.conjugate(verb, normalized_tense)

    table = Table(title=f"Conjugation of '{verb}' ({normalized_tense})")
    table.add_column("Pronoun", style="cyan", no_wrap=True)
    table.add_column("Form", style="magenta")

    for pronoun, form in result["forms"].items():
        table.add_row(pronoun, form)

    console.print(table)
    console.print(f"\n[italic]Type: {result['type']}[/italic]")
    if "auxiliary" in result:
        console.print(f"[italic]Auxiliary: {result['auxiliary']}[/italic]")
    if "participle" in result:
        console.print(f"[italic]Past Participle: {result['participle']}[/italic]")


@app.command()
def separable(verb: str) -> None:
    """Explain separable verb usage."""
    conjugator = VerbConjugator()
    result = conjugator.handle_separable(verb)

    if "error" in result:
        console.print(f"[red]Error: {result['error']}[/red]")
        return

    console.print(
        Panel(
            f"Prefix: [bold]{result['prefix']}[/bold]\n"
            f"Base Verb: [bold]{result['base_verb']}[/bold]\n\n"
            f"{result['rule']}",
            title=f"Separable Verb: {verb}",
            border_style="green",
        )
    )

    console.print("\n[bold cyan]Examples:[/bold cyan]")
    for example in result["examples"]:
        console.print(f"  [yellow]{example['example']}[/yellow]")
        console.print(f"  {example['english']}\n")


@app.command()
def wordorder() -> None:
    """Explain German word order rules."""
    teacher = WordOrderTeacher()
    v2 = teacher.explain_v2_rule()

    console.print(
        Panel(
            v2["rule"]["explanation"],
            title="V2 Rule - Verb Second Position",
            border_style="green",
        )
    )

    console.print("\n[bold cyan]Examples:[/bold cyan]")
    for example in v2["rule"]["examples"]:
        console.print(f"  [yellow]{example['german']}[/yellow]")
        console.print(f"  Structure: {example['structure']}")
        console.print(f"  {example['english']}\n")


@app.command()
def chat(level: str = "A1") -> None:  # pragma: no cover - interactive
    """Start a conversation with AI partner."""
    partner = AIConversationPartner(level=level)

    console.print(
        Panel(
            f"Starting conversation at level [bold]{level}[/bold]\n"
            "Type 'exit' to quit, 'switch' to change formality",
            title="AI Conversation Partner",
            border_style="green",
        )
    )

    console.print("\n[yellow]AI: Guten Tag! Wie geht es Ihnen?[/yellow]\n")

    while True:
        user_input = console.input("[cyan]You: [/cyan]")

        if user_input.lower() == "exit":
            console.print("[green]Auf Wiedersehen![/green]")
            break

        if user_input.lower() == "switch":
            result = partner.switch_formality(to_informal=True)
            console.print(f"\n[green]{result['explanation']}[/green]\n")
            continue

        response = partner.chat(user_input)

        console.print(f"\n[yellow]AI: {response['german']}[/yellow]")
        if response.get("english"):
            console.print(f"[dim]{response['english']}[/dim]")

        if response.get("grammar_notes"):
            console.print(f"[cyan]Grammar: {', '.join(response['grammar_notes'])}[/cyan]")

        console.print()


@app.command()
def scenario(
    scenario_type: str = typer.Argument("Bäckerei", help="Scenario type (dynamic)"),
    list_scenarios: bool = typer.Option(False, "--list", help="List available scenarios"),
    scenarios_file: Optional[Path] = typer.Option(
        None, "--scenarios-file", help="Path to scenarios JSON file"
    ),
    show: bool = typer.Option(False, "--show", help="Show raw scenario JSON and exit"),
    append_lists: bool = typer.Option(
        False, "--append-lists/--replace-lists", help="Merge behavior for list fields"
    ),
    export: Optional[Path] = typer.Option(None, "--export", help="Export selected scenario to file"),
    export_all: Optional[Path] = typer.Option(
        None, "--export-all", help="Export all merged scenarios to file"
    ),
) -> None:
    """Start a conversation scenario."""
    partner = AIConversationPartner(scenarios_file=scenarios_file, append_lists=append_lists)

    if list_scenarios:
        names = partner.available_scenarios()
        table = Table(title="Available Scenarios")
        table.add_column("Name", style="cyan")
        for n in names:
            table.add_row(n)
        console.print(table)
        return

    if export_all:
        import json as _json

        data = partner.get_all_scenarios()
        export_all.parent.mkdir(parents=True, exist_ok=True)
        export_all.write_text(_json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        console.print(f"[green]Exported all scenarios to {export_all}[/green]")
        return

    # Validate requested scenario (case-insensitive + fuzzy suggestion)
    avail = partner.available_scenarios()
    chosen = scenario_type

    if chosen not in set(avail):
        lower_map = {n.lower(): n for n in avail}
        key_lower = chosen.lower()
        if key_lower in lower_map:
            chosen = lower_map[key_lower]
        else:
            import difflib as _difflib

            matches = _difflib.get_close_matches(key_lower, list(lower_map.keys()), n=1, cutoff=0.6)
            suggestion = f" Did you mean: {lower_map[matches[0]]}?" if matches else ""
            console.print(
                Panel(
                    f"Unknown scenario: {scenario_type}{suggestion}\nAvailable: {', '.join(sorted(avail))}",
                    title="Scenario Error",
                    border_style="red",
                )
            )
            return

    scenario = partner.scenario(chosen)

    if show:
        import json as _json
        console.print(_json.dumps(scenario, ensure_ascii=False, indent=2))
        return

    if export:
        import json as _json
        export.parent.mkdir(parents=True, exist_ok=True)
        export.write_text(_json.dumps(scenario, ensure_ascii=False, indent=2), encoding="utf-8")
        console.print(f"[green]Exported {chosen} to {export}[/green]")
        return

    console.print(
        Panel(
            scenario["setting"], title=f"Scenario: {chosen}", border_style="green"
        )
    )

    console.print(f"\n[yellow]{scenario['dialogue']}[/yellow]")
    console.print(f"[dim]{scenario['english']}[/dim]\n")

    console.print("[bold cyan]Useful Vocabulary:[/bold cyan]")
    for word, translation in scenario["vocabulary"].items():
        console.print(f"  {word} - {translation}")

    console.print("\n[bold cyan]Useful Phrases:[/bold cyan]")
    for phrase in scenario["useful_phrases"]:
        console.print(f"  - {phrase}")


@app.command(name="scenario-template")
def scenario_template(
    name: str = typer.Argument("Café", help="Name of the scenario to scaffold"),
    out: Path = typer.Option(
        Path("scenario_template.json"), "--out", help="Output path for the template JSON"
    ),
) -> None:
    """Generate a new scenario JSON template file."""
    template = {
        name: {
            "setting": f"You're at a {name}",
            "starter": "Guten Tag!",
            "english": "Good day!",
            "vocabulary": {
                "der Kaffee": "coffee",
                "der Tee": "tea"
            },
            "useful_phrases": [
                "Ich hätte gern ... - I would like ...",
                "Die Rechnung, bitte. - The bill, please."
            ]
        }
    }

    import json as _json

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(_json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")
    console.print(f"[green]Wrote scenario template to {out}[/green]")


@app.command(name="scenarios-merge")
def scenarios_merge(
    from_file: Path = typer.Option(..., "--from", help="Path to scenarios JSON to merge"),
    to_file: Path = typer.Option(
        Path("media/scenarios.json"), "--to", help="Target scenarios JSON to update"
    ),
    append_lists: bool = typer.Option(
        False, "--append-lists/--replace-lists", help="Merge behavior for list fields"
    ),
) -> None:
    """Merge a scenarios JSON into the default scenarios file."""
    import json as _json

    if not from_file.exists():
        console.print(f"[red]Source file not found: {from_file}[/red]")
        raise typer.Exit(code=1)

    # Load existing (if any) via partner to reuse merge logic
    partner = AIConversationPartner(scenarios_file=to_file, append_lists=append_lists)
    base = partner.get_all_scenarios()

    # Load override
    try:
        data = _json.loads(from_file.read_text(encoding="utf-8"))
    except Exception as e:  # pragma: no cover - defensive
        console.print(f"[red]Failed to read {from_file}: {e}[/red]")
        raise typer.Exit(code=1)

    merged = partner._merge_scenarios(base, data)  # reuse tested merge logic

    to_file.parent.mkdir(parents=True, exist_ok=True)
    to_file.write_text(_json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    console.print(f"[green]Merged scenarios into {to_file}[/green]")
    console.print(f"Append lists: {'yes' if append_lists else 'no'}")

if __name__ == "__main__":  # pragma: no cover - module execution
    app()
