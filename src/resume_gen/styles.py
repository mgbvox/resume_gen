"""Resume styling presets and CSS file loading.

This module manages CSS stylesheets for resume formatting, including
built-in presets and custom file loading.

Built-in Styles:
    - ``modern``: Clean sans-serif with blue accents
    - ``classic``: Traditional serif, black and white
    - ``minimal``: Light, airy with subtle styling

Example:
    Get a built-in style::

        from resume_gen.styles import get_style

        css = get_style("modern")

    Load a custom CSS file::

        css = get_style("./my-custom-style.css")

    List available presets::

        from resume_gen.styles import list_styles

        for name in list_styles():
            print(name)  # modern, classic, minimal
"""

from pathlib import Path

# Default assets directory relative to package root
# styles.py -> resume_gen/ -> src/ -> resume_gen/ -> assets/
ASSETS_DIR = Path(__file__).parent.parent.parent / "assets"

BUILTIN_STYLES = ["modern", "classic", "minimal"]


def get_style(name_or_path: str | Path) -> str:
    """Get CSS content from a preset name or file path.

    Determines whether the input is a preset name or file path and
    returns the corresponding CSS content.

    Args:
        name_or_path: Either a preset name ("modern", "classic", "minimal")
            or a path to a CSS file (absolute or relative).

    Returns:
        CSS stylesheet content as a string.

    Raises:
        ValueError: If the preset name is not recognized.
        FileNotFoundError: If the CSS file doesn't exist.

    Example:
        >>> css = get_style("modern")  # doctest: +SKIP
        >>> "@page" in css  # doctest: +SKIP
        True

        >>> css = get_style("./custom.css")  # doctest: +SKIP
    """
    # Check if it's a path (contains / or \ or ends with .css)
    path = Path(name_or_path)

    if path.suffix == ".css" or "/" in str(name_or_path) or "\\" in str(name_or_path):
        # It's a file path
        if not path.exists():
            msg = f"CSS file not found: {path}"
            raise FileNotFoundError(msg)
        return path.read_text(encoding="utf-8")

    # It's a preset name - look in assets directory
    css_file = ASSETS_DIR / f"{name_or_path}.css"

    if not css_file.exists():
        available = ", ".join(BUILTIN_STYLES)
        msg = f"Unknown style '{name_or_path}'. Available presets: {available}"
        raise ValueError(msg)

    return css_file.read_text(encoding="utf-8")


def list_styles() -> list[str]:
    """Return list of available built-in style preset names.

    Returns:
        List of style names that can be passed to ``get_style()``.

    Example:
        >>> list_styles()
        ['modern', 'classic', 'minimal']
    """
    return BUILTIN_STYLES.copy()


def get_assets_dir() -> Path:
    """Return the path to the assets directory.

    The assets directory contains the built-in CSS style presets.

    Returns:
        Path to the assets directory.

    Example:
        >>> assets = get_assets_dir()  # doctest: +SKIP
        >>> (assets / "modern.css").exists()  # doctest: +SKIP
        True
    """
    return ASSETS_DIR
