"""CLI for resume-gen using Typer.

This module provides the command-line interface for the resume generator,
including commands for generating PDFs, previewing HTML output, and
running a live-reload development server.

Example:
    Generate a PDF::

        $ uv run resume-gen generate resume.md
        $ uv run resume-gen generate resume.md -o output.pdf --style classic

    Preview HTML::

        $ uv run resume-gen preview resume.md

    Live reload server::

        $ uv run resume-gen serve resume.md --style ./assets/modern.css
"""

from pathlib import Path
from typing import Annotated

import typer

from resume_gen.converter import markdown_to_pdf
from resume_gen.styles import get_assets_dir, list_styles

app = typer.Typer(
    name="resume-gen",
    help="Generate formatted PDF resumes from Markdown files.",
    no_args_is_help=True,
)


def resolve_css_path(style: str) -> Path:
    """Resolve style name or path to an actual CSS file path.

    Determines whether the input is a preset name (e.g., "modern") or
    a file path (e.g., "./custom.css") and returns the resolved path.

    Args:
        style: Either a preset name ("modern", "classic", "minimal") or
            a path to a CSS file.

    Returns:
        Absolute path to the CSS file.

    Example:
        >>> resolve_css_path("modern")  # doctest: +SKIP
        PosixPath('/path/to/assets/modern.css')
        >>> resolve_css_path("./custom.css")  # doctest: +SKIP
        PosixPath('/absolute/path/to/custom.css')
    """
    path = Path(style)
    if path.suffix == ".css" or "/" in style or "\\" in style:
        return path.resolve()
    return get_assets_dir() / f"{style}.css"


@app.command()
def generate(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the input Markdown file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Output PDF file path. Defaults to input filename with .pdf extension.",
        ),
    ] = None,
    style: Annotated[
        str,
        typer.Option(
            "--style",
            "-s",
            help="Style preset (modern/classic/minimal) or path to CSS file.",
        ),
    ] = "modern",
) -> None:
    """Generate a formatted PDF resume from a Markdown file.

    Converts the input Markdown file to a styled PDF using the specified
    style preset or custom CSS file.

    Example:
        $ uv run resume-gen generate resume.md
        $ uv run resume-gen generate resume.md -o my-resume.pdf
        $ uv run resume-gen generate resume.md --style classic
    """
    if output is None:
        output = input_file.with_suffix(".pdf")

    typer.echo(f"Converting {input_file.name} -> {output.name}")

    try:
        markdown_to_pdf(input_file, output, style=style)
        typer.echo(f"Success! Resume saved to {output}")
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def preview(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the input Markdown file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    style: Annotated[
        str,
        typer.Option(
            "--style",
            "-s",
            help="Style preset (modern/classic/minimal) or path to CSS file.",
        ),
    ] = "modern",
) -> None:
    """Preview the HTML output without generating PDF.

    Outputs the complete HTML document to stdout, useful for debugging
    or piping to other tools.

    Example:
        $ uv run resume-gen preview resume.md
        $ uv run resume-gen preview resume.md --style minimal > preview.html
    """
    from resume_gen.converter import markdown_to_html
    from resume_gen.styles import get_style

    markdown_content = input_file.read_text(encoding="utf-8")
    html = markdown_to_html(markdown_content, get_style(style))
    typer.echo(html)


@app.command()
def serve(
    input_file: Annotated[
        Path,
        typer.Argument(
            help="Path to the input Markdown file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
        ),
    ],
    style: Annotated[
        str,
        typer.Option(
            "--style",
            "-s",
            help="Style preset (modern/classic/minimal) or path to CSS file.",
        ),
    ] = "modern",
    port: Annotated[
        int,
        typer.Option(
            "--port",
            "-p",
            help="Port to serve on.",
        ),
    ] = 8000,
    no_browser: Annotated[
        bool,
        typer.Option(
            "--no-browser",
            help="Don't open browser automatically.",
        ),
    ] = False,
) -> None:
    """Start a live-reload server for previewing your resume.

    Launches a local HTTP server that serves the resume preview and
    automatically refreshes the browser when the Markdown or CSS files
    are modified. Useful for iterating on styles.

    Example:
        $ uv run resume-gen serve resume.md
        $ uv run resume-gen serve resume.md --style ./assets/modern.css
        $ uv run resume-gen serve resume.md --port 3000 --no-browser
    """
    from resume_gen.server import run_server

    css_path = resolve_css_path(style)

    if not css_path.exists():
        typer.echo(f"Error: CSS file not found: {css_path}", err=True)
        raise typer.Exit(code=1)

    run_server(
        md_path=input_file,
        css_path=css_path,
        port=port,
        open_browser=not no_browser,
    )


@app.command()
def styles() -> None:
    """List available style presets.

    Displays all built-in style presets and their file paths.
    Custom CSS files can be used with the --style option.

    Example:
        $ uv run resume-gen styles
        Available style presets:
          modern       -> /path/to/assets/modern.css
          classic      -> /path/to/assets/classic.css
          minimal      -> /path/to/assets/minimal.css
    """
    typer.echo("Available style presets:")
    for name in list_styles():
        css_path = get_assets_dir() / f"{name}.css"
        typer.echo(f"  {name:12} -> {css_path}")
    typer.echo("\nYou can also pass a path to any .css file with --style")


if __name__ == "__main__":
    app()
