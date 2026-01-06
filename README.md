# resume-gen

A CLI tool for generating beautifully formatted PDF resumes from Markdown files, paired with an AI agent workflow for creating targeted, company-specific resumes.

## Features

- **Markdown to PDF** - Write your resume in Markdown, get a professional PDF
- **Multiple Styles** - Built-in presets: `modern`, `classic`, `minimal`
- **Custom CSS** - Use your own stylesheets for complete control
- **Live Reload** - Preview changes in real-time as you edit
- **Agent Workflow** - Structured process for generating company-targeted resumes (see `AGENT_FLOW.md`)

## Installation

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/).

```bash
# Clone the repository
git clone <repo-url>
cd resume-gen

# Install dependencies
uv sync
```

## Quick Start

```bash
# Generate a PDF with the default (modern) style
uv run resume-gen generate resume.md

# Specify output path
uv run resume-gen generate resume.md -o my-resume.pdf

# Use a different style
uv run resume-gen generate resume.md --style classic

# Use custom CSS
uv run resume-gen generate resume.md --style ./assets/modern.css
```

## CLI Commands

### `generate` - Create a PDF

```bash
uv run resume-gen generate INPUT_FILE [OPTIONS]

Options:
  -o, --output PATH    Output PDF path (default: input name with .pdf)
  -s, --style TEXT     Style preset or path to CSS file (default: modern)
```

### `serve` - Live Preview with Hot Reload

Start a local server that watches your Markdown and CSS files, automatically refreshing the browser when changes are detected:

```bash
uv run resume-gen serve resume.md

Options:
  -s, --style TEXT     Style preset or path to CSS file (default: modern)
  -p, --port INTEGER   Port to serve on (default: 8000)
  --no-browser         Don't open browser automatically
```

### `preview` - Output HTML

```bash
uv run resume-gen preview resume.md --style modern
```

### `styles` - List Available Styles

```bash
uv run resume-gen styles
```

## Styling

### Built-in Styles

| Style | Description |
|-------|-------------|
| `modern` | Clean sans-serif with blue accents |
| `classic` | Traditional serif, black and white |
| `minimal` | Light, airy with subtle styling |

### Custom CSS

Point to any CSS file:

```bash
uv run resume-gen generate resume.md --style ./my-custom-style.css
uv run resume-gen serve resume.md --style ./assets/modern.css
```

CSS files support `@page` rules for print-specific styling:

```css
@page {
    size: letter;
    margin: 0.5in 0.6in;
}

body {
    font-family: "Helvetica Neue", sans-serif;
    font-size: 10pt;
}

h1 {
    font-size: 22pt;
    color: #1a1a1a;
}

h2 {
    color: #2c5282;
    border-bottom: 1.5pt solid #2c5282;
}
```

## Markdown Format

The tool expects standard Markdown with this general structure:

```markdown
# Your Name

**email@example.com | github.com/you | City, State | (555) 123-4567**

---

## Professional Experience

### Job Title, Company Name (Year - Year)

- Achievement with quantified impact
- Another accomplishment

---

## Education

**University Name** — Degree, Major, Year

---

## Skills

- Skill category: specific skills
```

## Agent Workflow

This repository includes an AI agent workflow for generating targeted, company-specific resumes. See **`AGENT_FLOW.md`** for the complete workflow, which covers:

1. Generating a master resume from context files
2. Researching target companies
3. Customizing resumes for specific roles
4. Generating final PDFs

## Project Structure

```
resume-gen/
├── AGENT_FLOW.md        # AI agent workflow instructions
├── README.md            # This file
├── assets/              # CSS style presets
│   ├── modern.css
│   ├── classic.css
│   └── minimal.css
├── context/             # Supporting documents (not committed)
│   └── *.md             # Past resumes, accomplishments, notes
├── resume-base.md       # Generated master resume (not committed)
├── target/              # Company-specific outputs (not committed)
│   └── {company}/
│       ├── research.md
│       └── resume.md/pdf
├── src/resume_gen/      # Python package
│   ├── __init__.py
│   ├── cli.py           # Typer CLI
│   ├── converter.py     # Markdown → PDF
│   ├── server.py        # Live reload server
│   └── styles.py        # Style loading
└── pyproject.toml
```

## Development

```bash
# Install in development mode
uv sync

# Run CLI
uv run resume-gen --help
```

## Dependencies

- [Typer](https://typer.tiangolo.com/) - CLI framework
- [WeasyPrint](https://weasyprint.org/) - HTML/CSS to PDF
- [Markdown](https://python-markdown.github.io/) - Markdown parsing
- [watchfiles](https://watchfiles.helpmanual.io/) - File watching for live reload

## License

MIT
