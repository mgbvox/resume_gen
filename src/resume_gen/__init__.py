"""Resume generator - Convert Markdown to formatted PDF resumes.

This package provides a CLI tool and Python API for converting Markdown-formatted
resumes into professionally styled PDF documents.

Example:
    CLI usage::

        $ uv run resume-gen generate resume.md
        $ uv run resume-gen generate resume.md --style classic
        $ uv run resume-gen serve resume.md  # live preview

    Python API::

        from pathlib import Path
        from resume_gen import markdown_to_pdf, get_style

        # Generate PDF with default style
        markdown_to_pdf(Path("resume.md"), Path("resume.pdf"))

        # Get CSS content for a style
        css = get_style("modern")

Attributes:
    app: The Typer CLI application instance.
    BUILTIN_STYLES: List of available style presets ("modern", "classic", "minimal").
"""

from resume_gen.cli import app
from resume_gen.converter import markdown_to_html, markdown_to_pdf
from resume_gen.styles import get_assets_dir, get_style, list_styles

__all__ = [
    "app",
    "get_assets_dir",
    "get_style",
    "list_styles",
    "main",
    "markdown_to_html",
    "markdown_to_pdf",
]


def main() -> None:
    """Entry point for the CLI.

    This function is called when running ``uv run resume-gen`` or
    invoking the package as a script.
    """
    app()
