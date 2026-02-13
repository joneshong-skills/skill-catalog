---
name: skill-catalog
description: >-
  This skill should be used when the user asks to "list all skills", "skill catalog",
  "skill inventory", "show skill overview", "export skill list", "skill 清單",
  "skill 總覽", "列出所有 skill", "匯出 skill 資料", "技能盤點",
  "visualize skill graph", "interactive skill map", "skill 視覺化",
  mentions skill cataloging, or discusses exporting structured skill metadata,
  viewing an interactive skill relationship graph, or generating a skill inventory report.
version: 0.3.1
tools: Read, Bash, Glob, Grep
---

# Skill Catalog

Extract structured metadata from all installed skills and generate an interactive
Neo4j-style graph explorer. Produces both a data export (JSON/CSV) and a self-contained
HTML visualization with D3.js force-directed graph.

## Workflow

### Step 1: Extract Structured Catalog

Run the extraction script to build the catalog:

```bash
python3 ~/.claude/skills/skill-catalog/scripts/extract_catalog.py \
  -o ~/Downloads/skill-catalog.json
```

Options:
- `--format csv` for CSV output (default: json)
- `--skill <name>` for a single skill
- `--output <path>` to specify output location

Each skill entry contains:

| Field | Description |
|-------|-------------|
| name | Skill identifier |
| version | Current version |
| **domain** | **Primary classification (mutually exclusive, exactly one per skill)** |
| **tags** | **Cross-cutting labels (multiple per skill, sorted alphabetically)** |
| strengths | Derived capabilities (from tools + domain signals) |
| pain_point | Purpose statement from the first body paragraph |
| triggers | Quoted trigger phrases from the description |
| tools | Declared tool dependencies |
| body_lines | SKILL.md line count |
| resources | Script/reference/asset counts |

#### Domain vs Tags

| Dimension | Cardinality | Purpose |
|-----------|-------------|---------|
| **domain** | Exactly 1 | "What domain does this skill belong to?" — used for grouping and filtering |
| **tags** | 0 to many | "What cross-cutting concerns does it touch?" — used for discovery and search |

Present a summary table to the user after extraction.

### Step 2: Build Relationship Graph

Use skill-graph's scanner to generate the edge data:

```bash
python3 ~/.claude/skills/skill-graph/scripts/scan_skills.py \
  --json -o ~/Downloads/skill-graph.json
```

This produces nodes, edges (pipeline / enhancement / shares-domain), compositions,
and graph statistics. The graph data complements the catalog with relationship info.

### Step 3: Generate Interactive Viewer

Combine catalog and graph data into a self-contained HTML file:

```bash
python3 ~/.claude/skills/skill-catalog/scripts/generate_viewer.py \
  --graph ~/Downloads/skill-graph.json \
  --catalog ~/Downloads/skill-catalog.json \
  -o ~/Downloads/skill-graph-viewer.html
```

The viewer provides a Neo4j-style interface:
- **Force-directed graph** — drag, zoom, pan nodes
- **Domain color coding** — each domain has a distinct color
- **Node size** — proportional to connection count
- **Click node** — detail panel with strengths, triggers, connections
- **Search** — filter by skill name
- **Domain filters** — toggle domain pills to focus on subsets
- **Edge types** — solid (pipeline), dashed green (enhancement), dotted gray (shared domain)
- **Legend** — edge types and domain colors

Open the HTML file in any browser — no server needed.

### Step 4: Present Results

After generating, provide the user with:

1. **Summary stats** — total skills, edges, compositions, hub skills
2. **File locations** — paths to catalog JSON, graph JSON, and HTML viewer
3. **Quick open** — `open ~/Downloads/skill-graph-viewer.html`

If the user wants a specific export format (xlsx, etc.), delegate to the appropriate
skill (e.g., `/xlsx` for spreadsheet output) using the catalog JSON as the data source.

## Quick Reference

### One-Liner: Full Pipeline

```bash
python3 ~/.claude/skills/skill-catalog/scripts/extract_catalog.py -o ~/Downloads/skill-catalog.json && \
python3 ~/.claude/skills/skill-graph/scripts/scan_skills.py --json -o ~/Downloads/skill-graph.json && \
python3 ~/.claude/skills/skill-catalog/scripts/generate_viewer.py \
  --graph ~/Downloads/skill-graph.json \
  --catalog ~/Downloads/skill-catalog.json \
  -o ~/Downloads/skill-graph-viewer.html && \
open ~/Downloads/skill-graph-viewer.html
```

### Domain Reference (mutually exclusive)

| Domain | Description | Example Skills |
|--------|-------------|----------------|
| orchestration | Multi-agent/multi-CLI coordination | maestro, team-tasks |
| dev-tooling | CLI automation, headless execution, MCP | claude-code-headless, codex-headless, mcp-builder |
| document-output | Producing formatted documents | pdf, docx, pptx, xlsx |
| visual-design | Visual artifacts: diagrams, images, UI | diagram-gen, image-gen, canvas-design, frontend-design |
| content-creation | Writing and drafting text content | marketing-copy, content-writer |
| knowledge-mgmt | Research, search, knowledge bases | smart-search, notebookllm-mentor, notebook-bridge |
| analysis | Data/competitor/meeting analysis | competitive-intel, meeting-insights |
| ideation | Brainstorming, planning, model selection | brainstorming, model-mentor |
| skill-meta | Managing skills themselves | create-skill, skill-optimizer, skill-curator, skill-publisher |
| general | Fallback when no signal matches | (rare) |

Priority: When multiple domain signals match, the domain is chosen by specificity
(orchestration > dev-tooling > document-output > visual-design > ... > skill-meta).

### Tag Reference (cross-cutting, multiple per skill)

| Tag | Matches when description/pain_point contains |
|-----|----------------------------------------------|
| browser | browser, playwright, chrome, web page |
| headless | headless, -p, pipe, programmatic, cron, ci/cd |
| notebooklm | notebooklm, notebook, audio overview |
| github | github, git, pull request, pr, repo |
| mermaid | mermaid, flowchart, sequence diagram |
| ai-image | image gen, generate an image, grok, dall-e, midjourney, flux, stable diffusion |
| multi-agent | multi-agent, orchestrate, dispatch, parallel, team, coordinate, pipeline |
| search | search, research, look up, documentation, query |
| writing | write, draft, article, blog, copy, content, newsletter |
| code | code, debug, review, cli, codex, sdk, mcp |
| data | csv, xlsx, spreadsheet, data, chart, formula |
| design | design, ui, ux, frontend, landing page, theme, brand, poster, canvas, visual |
| pdf | pdf, merge, split, watermark, ocr |
| slides | pptx, presentation, slide, deck, pitch |
| chinese | 繁體, 中文, zh-tw, 台灣 |
| llm | model, recommend, llm, gpt, claude, gemini |
| spec | spec, specification, sdd, implementation plan |
| marketing | marketing, ad copy, competitor, positioning, campaign |

### Domain Color Map

| Domain | Color | Skills |
|--------|-------|--------|
| content-creation | Green | marketing-copy, content-writer, ... |
| document-output | Orange | pdf, docx, pptx, xlsx |
| visual-design | Purple | diagram-gen, image-gen, canvas-design, frontend-design |
| dev-tooling | Blue | claude-code-headless, codex-headless, gemini-cli-headless, mcp-builder |
| orchestration | Teal | maestro, team-tasks |
| knowledge-mgmt | Yellow | smart-search, notebookllm-mentor, notebook-bridge |
| skill-meta | Gray | create-skill, skill-optimizer, skill-curator, skill-publisher |
| analysis | Red | competitive-intel, meeting-insights |
| ideation | Gold | brainstorming, model-mentor |

### Viewer Features

| Feature | How |
|---------|-----|
| Zoom | Scroll wheel or pinch |
| Pan | Click and drag on background |
| Move node | Click and drag on node |
| Select node | Click on node or sidebar item |
| Filter by domain | Click domain pills in sidebar |
| Search | Type in search box |
| See connections | Click node → detail panel shows all edges |
| Navigate | Click connection name in detail panel |

## Continuous Improvement

This skill evolves with each use. After every invocation:

1. **Reflect** — Identify what worked, what caused friction, and any unexpected issues
2. **Record** — Append a concise lesson to `lessons.md` in this skill's directory
3. **Refine** — When a pattern recurs (2+ times), update SKILL.md directly

### lessons.md Entry Format

```
### YYYY-MM-DD — Brief title
- **Friction**: What went wrong or was suboptimal
- **Fix**: How it was resolved
- **Rule**: Generalizable takeaway for future invocations
```

Accumulated lessons signal when to run `/skill-optimizer` for a deeper structural review.

## Additional Resources

### Scripts
- **`scripts/extract_catalog.py`** — Extract structured metadata from all skills.
  Usage: `python3 extract_catalog.py [--skills-dir DIR] [--output FILE] [--format json|csv] [--skill NAME]`
- **`scripts/generate_viewer.py`** — Generate interactive HTML graph viewer.
  Usage: `python3 generate_viewer.py --graph GRAPH_JSON --catalog CATALOG_JSON [-o OUTPUT_HTML]`

### Assets
- **`assets/viewer-template.html`** — D3.js Neo4j-style graph template.
  Data is injected at generation time via placeholder replacement.
