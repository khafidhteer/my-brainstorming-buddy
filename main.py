#!/usr/bin/env python3
"""CLI entry point for the Chain-of-Thought Reasoning Engine.

Provides command-line interface for running framework-based analysis.
"""

import asyncio
import logging
import sys
from typing import Optional

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

from src.llm_adapter import LLMAdapter
from src.orchestrator import Orchestrator
from src.framework_selector import list_frameworks

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

console = Console()


@click.group()
def cli():
    """🤔 My Brainstorming Buddy - Chain-of-Thought Reasoning Engine."""
    pass


@cli.command()
@click.argument("question")
@click.option(
    "--framework", "-f",
    default=None,
    help="Framework to use (override auto-detect). "
         "Options: fishbone, fault_tree, iceberg, apollo_rca, "
         "stamp, swiss_cheese, cynefin, dmaic",
)
@click.option(
    "--api-key", "-k",
    default=None,
    envvar="SUMODOP_API_KEY",
    help="API key (or set SUMODOP_API_KEY env var)",
)
@click.option(
    "--base-url",
    default="https://api.sumopod.com/v1",
    envvar="SUMODOP_BASE_URL",
    help="API base URL",
)
@click.option(
    "--model", "-m",
    default="gpt-4o-mini",
    envvar="SUMODOP_MODEL",
    help="Model name",
)
@click.option(
    "--json", "-j",
    "output_json",
    is_flag=True,
    default=False,
    help="Output as JSON",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    default=False,
    help="Show detailed step information",
)
def analyze(
    question: str,
    framework: Optional[str],
    api_key: Optional[str],
    base_url: str,
    model: str,
    output_json: bool,
    verbose: bool,
):
    """Analyze a question using chain-of-thought reasoning.

    QUESTION: The question or problem to analyze.
    """
    if not api_key:
        console.print(
            "[red]Error:[/red] API key is required. "
            "Set SUMODOP_API_KEY environment variable or use --api-key.",
        )
        sys.exit(1)

    try:
        result = asyncio.run(
            _run_analysis(
                question=question,
                framework=framework,
                api_key=api_key,
                base_url=base_url,
                model=model,
                verbose=verbose,
            )
        )

        if output_json:
            console.print(result.to_json())
        else:
            _display_result(result, verbose)

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.exception("Analysis failed")
        sys.exit(1)


@cli.command()
def frameworks():
    """List all available frameworks."""
    table = Table(title="Available Frameworks")
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    table.add_column("Description", style="white")

    for fw in list_frameworks():
        table.add_row(fw["key"], fw["name"], fw["description"])

    console.print(table)


async def _run_analysis(
    question: str,
    framework: Optional[str],
    api_key: str,
    base_url: str,
    model: str,
    verbose: bool,
):
    """Run the analysis with progress display."""
    llm = LLMAdapter(
        api_key=api_key,
        base_url=base_url,
        model=model,
    )
    orchestrator = Orchestrator(llm=llm)

    # Show auto-detect message
    if not framework:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(
                description="[yellow]Detecting best framework...[/yellow]",
                total=None,
            )
            result = await orchestrator.analyze(
                question=question,
                verbose=verbose,
            )
    else:
        result = await orchestrator.analyze(
            question=question,
            preferred_framework=framework,
            verbose=verbose,
        )

    return result


def _display_result(result, verbose: bool = False):
    """Display the analysis result in the terminal."""
    # Header
    console.print()
    console.print(
        Panel.fit(
            f"[bold blue]🤔 My Brainstorming Buddy - Analysis Result[/bold blue]\n\n"
            f"[bold]Question:[/bold] {result.question}\n"
            f"[bold]Framework:[/bold] {result.framework_name} "
            f"({result.framework_key})\n"
            f"[bold]Steps:[/bold] {len(result.steps)}/{result.total_steps}\n"
            f"[italic]{result.framework_description}[/italic]",
            border_style="blue",
        )
    )
    console.print()

    # Display each step
    for step in result.steps:
        step_title = f"Step {step.step_index + 1}: {step.step_name}"
        console.print(
            Panel(
                Markdown(step.output),
                title=f"[bold green]{step_title}[/bold green]",
                subtitle=f"[italic]{step.step_description}[/italic]",
                border_style="green",
                padding=(1, 2),
            )
        )
        console.print()

    # Summary
    console.print(
        Panel(
            f"[bold]Analysis Complete[/bold]\n\n"
            f"Completed [green]{len(result.steps)}[/green] of "
            f"[green]{result.total_steps}[/green] steps\n"
            f"Framework: [blue]{result.framework_name}[/blue]\n\n"
            f"Export options available: use --json flag for JSON output.",
            border_style="yellow",
        )
    )


if __name__ == "__main__":
    cli()