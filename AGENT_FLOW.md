# Resume Generation Agent Flow

A guide for generating targeted resumes for specific companies/roles.

> **Prerequisites:** Read `README.md` first for CLI installation and usage details.

## Project Structure

```
resume_gen/
├── resume-base.md          # Generated master resume (not committed)
├── context/                # Supporting documents (not committed)
│   └── *.md                # Detailed accomplishments, past resumes, notes
├── target/                 # Company-specific outputs
│   └── {company}/
│       ├── research.md     # Company research
│       └── resume.md/pdf   # Customized resume
└── assets/                 # CSS styles for PDF generation
```

## Workflow

### 1. Generate or Update resume-base.md

Read all files in `context/` to understand the candidate's full background, then generate (or update) `resume-base.md` as a comprehensive master resume containing:

- All professional experience with detailed bullet points
- Education and certifications
- Honors and awards
- Any additional experience (side projects, volunteer work, etc.)

This file serves as the source of truth for all company-specific resumes. If `resume-base.md` already exists, update it with any new information from `context/`.

### 2. Create Target Directory

```bash
mkdir -p target/{company-name}
```

### 3. Research the Company

Use `WebSearch` to gather:
- What the company does (product/service)
- Leadership team (CEO, CTO, engineering leads)
- Technology stack (inferred from job posts, engineering blogs)
- Funding stage and scale
- Company culture and values
- Current job openings and requirements

**Search queries that work well:**
- `"{company}" what they do product`
- `"{company}" founders team leadership`
- `"{company}" engineering technology stack`
- `"{company}" careers jobs engineer {current_date}`
- `"{company}" funding series crunchbase`

Use `WebFetch` for specific pages:
- Company about/careers pages
- Job postings (Lever, Greenhouse, etc.)
- Press releases and funding announcements

### 4. Write research.md

Create `target/{company}/research.md` with:

```markdown
# {Company} - Company Research

## Overview
- What they do (1-2 sentences)
- Website, tagline, HQ, size

## Leadership
- Key people with backgrounds

## What They Do
- Core product/service
- Business model

## Technology (if known)
- Stack, infrastructure, practices

## Funding/Scale
- Funding rounds, metrics

## Careers
- Open roles, hiring focus

## Resume Alignment Opportunities
- How the candidate's experience maps to their needs
- Specific bullet points to emphasize
- Unique angles (e.g., arts background for entertainment companies, biology degree for biotech)

## Sources
- Links to all referenced materials
```

### 5. Understand the Specific Role

Get details on the target role:
- Job title and level
- Core responsibilities
- Required technologies
- Team structure

If user provides context (like "they need someone for X"), note the specific requirements.

### 6. Customize the Resume

Create `target/{company}/resume.md` by adapting `resume-base.md`:

**Reorder bullets** to lead with most relevant experience:
- Match their tech stack (e.g., if they use AWS, lead with AWS projects)
- Match their domain (fintech? music? healthcare?)
- Match their stage (startup? enterprise?)

**Emphasize relevant skills:**
- Bold key technologies that match their stack
- Quantify metrics that matter to them (throughput, scale, speed)
- Add Technical Skills section if role is technical

**Leverage unique angles:**
- Non-traditional backgrounds that align with company domain
- Academic credentials relevant to their industry
- Prior industry experience that transfers

**Adjust contact info** if location matters (e.g., emphasize proximity to company HQ)

### 7. Generate PDF

```bash
uv run resume-gen generate target/{company}/resume.md
```

Or with custom styling:
```bash
uv run resume-gen generate target/{company}/resume.md --style ./assets/modern.css
```

### 8. Review with Live Reload (Optional)

```bash
uv run resume-gen serve target/{company}/resume.md
```

Edit CSS/markdown and see changes live in browser.

---

## Quick Reference

### Key Files to Read First
- `context/*` - Detailed accomplishments, past resumes, and supporting materials
- `resume-base.md` - Generated master resume (create from context if missing)
---

## CLI Commands

See `README.md` for full CLI documentation. Quick reference:

```bash
uv run resume-gen generate input.md           # Generate PDF
uv run resume-gen generate input.md -o out.pdf  # Custom output path
uv run resume-gen generate input.md --style minimal  # Different style
uv run resume-gen serve input.md              # Live preview
uv run resume-gen styles                      # List styles
```
