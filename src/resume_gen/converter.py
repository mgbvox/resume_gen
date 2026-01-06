"""Markdown to PDF conversion for resumes.

This module handles the core conversion logic, transforming Markdown content
into styled HTML and then rendering it to PDF using WeasyPrint.

Example:
    Convert a Markdown file to PDF::

        from pathlib import Path
        from resume_gen.converter import markdown_to_pdf

        markdown_to_pdf(
            Path("resume.md"),
            Path("resume.pdf"),
            style="modern"
        )

    Generate HTML for inspection::

        from resume_gen.converter import markdown_to_html
        from resume_gen.styles import get_style

        css = get_style("modern")
        html = markdown_to_html("# John Doe\\n\\n**Engineer**", css)
"""

from pathlib import Path

import markdown
from weasyprint import CSS, HTML

from resume_gen.styles import get_style


def markdown_to_html(md_content: str, css: str) -> str:
    """Convert Markdown content to a complete styled HTML document.

    Parses the Markdown using Python-Markdown with extensions for
    extra syntax (tables, fenced code), smart quotes, and proper
    list handling. Wraps the result in a complete HTML5 document
    with embedded CSS.

    Args:
        md_content: Raw Markdown text to convert.
        css: CSS stylesheet content to embed in the document.

    Returns:
        Complete HTML5 document as a string, ready for rendering
        or saving to a file.

    Example:
        >>> css = "body { font-family: sans-serif; }"
        >>> html = markdown_to_html("# Hello\\n\\nWorld", css)
        >>> "<h1>Hello</h1>" in html
        True
        >>> "font-family: sans-serif" in html
        True
    """
    md = markdown.Markdown(
        extensions=["extra", "smarty", "sane_lists"],
        output_format="html5",
    )
    body_html = md.convert(md_content)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
    <style>
{css}
    </style>
</head>
<body>
{body_html}
</body>
</html>"""
    return html


def markdown_to_pdf(
    input_path: Path,
    output_path: Path,
    *,
    style: str = "modern",
) -> None:
    """Convert a Markdown file to a styled PDF resume.

    Reads the Markdown file, applies the specified style, and renders
    the result to a PDF file using WeasyPrint.

    Args:
        input_path: Path to the input Markdown file.
        output_path: Path where the output PDF will be written.
        style: Style preset name ("modern", "classic", "minimal") or
            path to a custom CSS file. Defaults to "modern".

    Raises:
        FileNotFoundError: If the input Markdown file doesn't exist.
        ValueError: If the style name is not recognized and isn't a
            valid file path.

    Example:
        >>> from pathlib import Path
        >>> from tempfile import NamedTemporaryFile
        >>> md_file = Path("/tmp/test_resume.md")
        >>> md_file.write_text("# Test\\n\\nHello")  # doctest: +SKIP
        >>> markdown_to_pdf(md_file, Path("/tmp/test.pdf"))  # doctest: +SKIP
    """
    if not input_path.exists():
        msg = f"Input file not found: {input_path}"
        raise FileNotFoundError(msg)

    css = get_style(style)
    md_content = input_path.read_text(encoding="utf-8")
    html_content = markdown_to_html(md_content, css)

    html_doc = HTML(string=html_content, base_url=str(input_path.parent))
    html_doc.write_pdf(output_path, stylesheets=[CSS(string=css)])
