from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import click
from click.shell_completion import CompletionItem


PROJECT_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = PROJECT_ROOT / "Scripts"


def available_scripts() -> list[Path]:
    if not SCRIPTS_DIR.exists():
        return []
    return sorted(path for path in SCRIPTS_DIR.glob("*.py") if path.is_file())


def resolve_script(script_name: str) -> Path:
    script_path = Path(script_name)
    if script_path.suffix != ".py":
        script_path = script_path.with_suffix(".py")

    if script_path.name != str(script_path):
        raise click.ClickException("Use a script name only, not a path.")

    resolved = (SCRIPTS_DIR / script_path.name).resolve()
    scripts_root = SCRIPTS_DIR.resolve()

    if scripts_root not in resolved.parents:
        raise click.ClickException("Script path must stay inside the Scripts directory.")
    if not resolved.exists():
        raise click.ClickException(f"Script not found: {script_path.name}")
    if not resolved.is_file():
        raise click.ClickException(f"Not a file: {script_path.name}")

    return resolved


def complete_script_names(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[CompletionItem]:
    return [
        CompletionItem(script.stem)
        for script in available_scripts()
        if script.stem.startswith(incomplete) or script.name.startswith(incomplete)
    ]


@click.group()
def cli() -> None:
    """Run class weather scripts from the Scripts directory."""


@cli.command("list")
def list_scripts() -> None:
    """Show available scripts."""
    scripts = available_scripts()
    if not scripts:
        click.echo("No scripts found in Scripts.")
        return

    for script in scripts:
        click.echo(script.stem)


@cli.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    }
)
@click.argument("script_name", shell_complete=complete_script_names)
@click.pass_context
def run(ctx: click.Context, script_name: str) -> None:
    """Run a script from Scripts."""
    script = resolve_script(script_name)
    command = [sys.executable, str(script), *ctx.args]
    result = subprocess.run(command, cwd=PROJECT_ROOT, check=False)

    if result.returncode != 0:
        raise click.exceptions.Exit(result.returncode)


if __name__ == "__main__":
    cli(complete_var="_MAIN_PY_COMPLETE")
