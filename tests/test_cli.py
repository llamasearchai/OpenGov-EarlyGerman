"""CLI integration tests using Typer's CliRunner."""

from pathlib import Path
from typing import Any

from typer.testing import CliRunner

from opengov_earlygerman.cli import app


runner = CliRunner()


def test_cli_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "OpenGov-EarlyGerman version" in result.stdout


def test_cli_case() -> None:
    result = runner.invoke(app, ["case", "nominative"])
    assert result.exit_code == 0
    assert "German Case: Nominative" in result.stdout


def test_cli_articles() -> None:
    result = runner.invoke(app, ["articles", "Hund", "--gender", "masculine"])
    assert result.exit_code == 0
    assert "Declension of 'Hund' (masculine)" in result.stdout


def test_cli_conjugate_alias_past() -> None:
    result = runner.invoke(app, ["conjugate", "machen", "--tense", "past"])
    assert result.exit_code == 0
    # The title should normalize to preterite
    assert "(preterite)" in result.stdout


def test_cli_scenario_list_and_pick(tmp_path: Path) -> None:
    # Create a minimal scenarios file
    scenarios = tmp_path / "scenarios.json"
    scenarios.write_text(
        """
{
  "Testplatz": {
    "setting": "Test setting",
    "starter": "Hallo!",
    "english": "Hello!",
    "vocabulary": {"das Test": "test"},
    "useful_phrases": ["Das ist ein Test."]
  }
}
""".strip(),
        encoding="utf-8",
    )

    # List should include our scenario
    res_list = runner.invoke(app, ["scenario", "--list", "--scenarios-file", str(scenarios)])
    assert res_list.exit_code == 0
    assert "Testplatz" in res_list.stdout

    # Running the scenario should print its title and content
    res_run = runner.invoke(
        app, ["scenario", "Testplatz", "--scenarios-file", str(scenarios)]
    )
    assert res_run.exit_code == 0
    assert "Scenario: Testplatz" in res_run.stdout
    assert "Hallo!" in res_run.stdout


def test_cli_scenario_case_insensitive() -> None:
    # Uses default scenarios file in repo
    res = runner.invoke(app, ["scenario", "supermarkt"])
    assert res.exit_code == 0
    assert "Scenario: Supermarkt" in res.stdout


def test_cli_scenario_suggestion() -> None:
    res = runner.invoke(app, ["scenario", "Restauran"])
    assert res.exit_code == 0
    assert "Did you mean: Restaurant?" in res.stdout


def test_cli_case_invalid() -> None:
    res = runner.invoke(app, ["case", "invalid"])
    assert res.exit_code == 0
    assert "Error:" in res.stdout


def test_cli_separable_error() -> None:
    res = runner.invoke(app, ["separable", "machen"])
    assert res.exit_code == 0
    assert "Error:" in res.stdout


def test_cli_wordorder() -> None:
    res = runner.invoke(app, ["wordorder"])
    assert res.exit_code == 0
    assert "V2 Rule - Verb Second Position" in res.stdout


def test_cli_separable_success() -> None:
    res = runner.invoke(app, ["separable", "aufstehen"])
    assert res.exit_code == 0
    assert "Separable Verb: aufstehen" in res.stdout


def test_cli_articles_error_path(monkeypatch) -> None:
    # Force error branch by mocking underlying teacher method
    import opengov_earlygerman.cli as cli_mod

    def fake_practice(noun: str, gender: str):  # type: ignore[override]
        return {"error": "boom"}

    monkeypatch.setattr(cli_mod.CasesTeacher, "practice_articles", lambda self, n, g: fake_practice(n, g))
    res = runner.invoke(app, ["articles", "Haus", "--gender", "neuter"])
    assert res.exit_code == 0
    assert "Error:" in res.stdout


def test_cli_scenario_template(tmp_path: Path) -> None:
    from opengov_earlygerman.cli import app as cli_app
    runner_local = CliRunner()
    out = tmp_path / "tmpl.json"
    res = runner_local.invoke(cli_app, ["scenario-template", "Cafe", "--out", str(out)])
    assert res.exit_code == 0
    txt = out.read_text(encoding="utf-8")
    assert "Cafe" in txt and "vocabulary" in txt


def test_cli_scenarios_merge(tmp_path: Path) -> None:
    from opengov_earlygerman.cli import app as cli_app
    runner_local = CliRunner()
    src = tmp_path / "src.json"
    dst = tmp_path / "dst.json"
    src.write_text(
        '{"X": {"setting": "X place", "starter": "Hi", "english": "Hi", "vocabulary": {"x": "x"}, "useful_phrases": ["x"]}}',
        encoding="utf-8",
    )
    # Seed destination with one scenario
    dst.write_text(
        '{"Y": {"setting": "Y place", "starter": "Yo", "english": "Yo", "vocabulary": {"y": "y"}, "useful_phrases": ["y"]}}',
        encoding="utf-8",
    )
    res = runner_local.invoke(cli_app, [
        "scenarios-merge", "--from", str(src), "--to", str(dst), "--append-lists"
    ])
    assert res.exit_code == 0
    out = dst.read_text(encoding="utf-8")
    assert "X" in out and "Y" in out


def test_cli_scenario_merge_defaults(tmp_path: Path) -> None:
    # Override default Bäckerei starter and extend vocabulary, add new scenario
    data = {
        "Bäckerei": {
            "starter": "Guten Morgen! Haben Sie Roggenbrot?",
            "vocabulary": {"das Roggenbrot": "rye bread"},
            "useful_phrases": ["Kann ich mit Karte zahlen? - Can I pay by card?"]
        },
        "Post": {
            "setting": "You're at a post office",
            "starter": "Ich möchte dieses Paket verschicken.",
            "english": "I would like to send this package.",
            "vocabulary": {"das Paket": "package"},
            "useful_phrases": ["Per Luftpost, bitte. - By airmail, please."]
        }
    }
    scenarios = tmp_path / "scenarios.json"
    scenarios.write_text(__import__("json").dumps(data, ensure_ascii=False), encoding="utf-8")

    # Listing includes both default and new scenarios
    res_list = runner.invoke(app, ["scenario", "--list", "--scenarios-file", str(scenarios)])
    assert res_list.exit_code == 0
    out = res_list.stdout
    assert "Bäckerei" in out and "Post" in out

    # Running Bäckerei uses overridden starter and contains merged vocabulary (default replace lists)
    res_run = runner.invoke(app, ["scenario", "Bäckerei", "--scenarios-file", str(scenarios)])
    assert res_run.exit_code == 0
    txt = res_run.stdout
    assert "Guten Morgen! Haben Sie Roggenbrot?" in txt
    # Merged vocab includes a default item and the new one
    assert "das Brötchen - bread roll" in txt
    assert "das Roggenbrot - rye bread" in txt

    # With append-lists flag, useful_phrases are appended rather than replaced
    res_append = runner.invoke(
        app,
        [
            "scenario",
            "Bäckerei",
            "--scenarios-file",
            str(scenarios),
            "--append-lists",
        ],
    )
    assert res_append.exit_code == 0
    atxt = res_append.stdout
    # Original default phrase should still appear
    assert "Ich hätte gern... - I would like..." in atxt
    # And the new one
    assert "Kann ich mit Karte zahlen? - Can I pay by card?" in atxt


def test_cli_scenario_show_json() -> None:
    res = runner.invoke(app, ["scenario", "Bäckerei", "--show"])
    assert res.exit_code == 0
    # JSON output should contain keys and be braces-delimited
    out = res.stdout.strip()
    assert out.startswith("{") and out.endswith("}")
    assert '"setting"' in out and '"vocabulary"' in out


def test_cli_scenario_export(tmp_path: Path) -> None:
    target = tmp_path / "one.json"
    res = runner.invoke(app, ["scenario", "Apotheke", "--export", str(target)])
    assert res.exit_code == 0
    assert target.exists()
    data = target.read_text(encoding="utf-8")
    assert "Apotheke" not in data  # single scenario JSON
    assert '"setting"' in data


def test_cli_scenario_export_all(tmp_path: Path) -> None:
    target = tmp_path / "all.json"
    res = runner.invoke(app, ["scenario", "--export-all", str(target)])
    assert res.exit_code == 0
    assert target.exists()
    data = target.read_text(encoding="utf-8")
    # all scenarios should include at least these keys
    assert "Bäckerei" in data and "Apotheke" in data
