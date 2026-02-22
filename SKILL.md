---
name: skill-catalog
description: >-
  This skill should be used when the user asks to "list all skills", "skill catalog",
  "skill inventory", "show skill overview", "export skill list", "skill 清單",
  "skill 總覽", "列出所有 skill", "匯出 skill 資料", "技能盤點",
  mentions skill cataloging, or discusses exporting structured skill metadata
  or generating a skill inventory report.
version: 0.5.0
tools: Read, Bash, Glob, Grep, sandbox_execute
---

# Skill Catalog

Extract structured metadata from all installed skills and present a clear,
practical inventory. Produces a JSON/CSV data export and a terminal summary table.

## Agent Delegation

Delegate skill scanning and metadata extraction to `explorer` agent.

```
explorer (Haiku, maxTurns=10, tools: Read, Grep, Glob)
```

## Workflow

### Step 1: Extract Catalog

**Preferred (Sandbox mode)** — extract + summarize in one call, ~99% less context:

```python
# sandbox_execute (python)
import os, sys, json
from pathlib import Path
sys.path.insert(0, os.path.expanduser("~/.claude/skills/skill-catalog/scripts"))
from extract_catalog import extract_skill

skills_dir = Path(os.path.expanduser("~/.claude/skills"))
guides_dir = skills_dir / "skill-catalog" / "guides"
catalog = []
for d in sorted(skills_dir.iterdir()):
    if not d.is_dir() or d.name.startswith("."):
        continue
    entry = extract_skill(d, guides_dir=guides_dir)
    if entry:
        catalog.append(entry)

# Save full JSON to file (NOT returned to context)
out = os.path.expanduser("~/Claude/skills/skill-catalog/skill-catalog.json")
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

# Group by domain — return only summary
grouped = {}
for s in catalog:
    grouped.setdefault(s["domain"], []).append(
        {"name": s["name"], "version": s["version"], "tags": s["tags"][:3]})
output({
    "total": len(catalog),
    "domains": {d: len(v) for d, v in sorted(grouped.items(), key=lambda x: -len(x[1]))},
    "saved_to": out,
})
```

**Fallback (Bash)** — when sandbox is unavailable:

```bash
python3 ~/.claude/skills/skill-catalog/scripts/extract_catalog.py \
  -o ~/Claude/skills/skill-catalog/skill-catalog.json
```

Options:
- `--format csv` for CSV output (default: json)
- `--skill <name>` for a single skill
- `--output <path>` to specify output location
- `--guides-dir <path>` directory containing per-skill guide `.md` files (default: `../guides/`)

Each skill entry contains:

| Field | Description |
|-------|-------------|
| name | Skill identifier |
| version | Current version |
| **domain** | **Primary classification (exactly one per skill)** |
| **tags** | **Cross-cutting labels (multiple per skill)** |
| **composable** | **Can be chained with other skills (pipeline/enhancement)** |
| **bundled_in** | **Parent skill if this is a sub-skill (e.g., forge bundles brainstorming)** |
| strengths | Derived capabilities (from tools + domain signals) |
| pain_point | Purpose statement |
| triggers | Trigger phrases from the description |
| tools | Declared tool dependencies |

### Step 2: Present Summary

After extraction, present results to the user as a **grouped table by domain**:

```
## Skill Inventory (N skills)

### Orchestration (2)
| Skill | Description | Composable | Tags |
|-------|-------------|------------|------|
| maestro | Multi-CLI task orchestrator | Yes (bundles: team-tasks) | multi-agent, llm |
| team-tasks | Agent team coordination | Yes | multi-agent |

### Dev Tooling (5)
...
```

Key information to highlight:
1. **Total count** — how many skills are installed
2. **By domain** — grouped table with description, composability, tags
3. **Bundled skills** — which skills are composed inside others (e.g., forge = brainstorming + spec-kit + blueprint + executor + verification)
4. **File location** — path to the exported JSON/CSV

If the user wants a different format (xlsx, HTML table, etc.), delegate to the
appropriate skill (e.g., `/xlsx`) using the catalog JSON as the data source.

## Domain Reference

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

## Tag Reference

| Tag | Matches when description contains |
|-----|-----------------------------------|
| browser | browser, playwright, chrome, web page |
| headless | headless, -p, pipe, programmatic |
| notebooklm | notebooklm, notebook, audio overview |
| github | github, git, pull request, pr, repo |
| mermaid | mermaid, flowchart, sequence diagram |
| ai-image | image gen, grok, dall-e, midjourney |
| multi-agent | multi-agent, orchestrate, dispatch, parallel, team |
| search | search, research, look up, documentation |
| writing | write, draft, article, blog, copy, content |
| code | code, debug, review, cli, codex, sdk, mcp |
| data | csv, xlsx, spreadsheet, data, chart |
| design | design, ui, ux, frontend, landing page, theme |
| pdf | pdf, merge, split, watermark, ocr |
| slides | pptx, presentation, slide, deck |
| chinese | 繁體, 中文, zh-tw |
| llm | model, recommend, llm, gpt, claude, gemini |
| spec | spec, specification, sdd, implementation plan |
| marketing | marketing, ad copy, competitor, positioning |

## Composability Markers

Skills can relate to each other in these ways:

| Relation | Meaning | Example |
|----------|---------|---------|
| **pipeline** | Output of A feeds into B | smart-search → content-writer |
| **enhancement** | B improves A's output | skill-optimizer enhances any skill |
| **bundled** | A orchestrates B as a sub-step | forge bundles brainstorming, spec-kit, blueprint, executor, verification |

Mark each skill with:
- `composable: true/false` — can it be meaningfully chained?
- `bundled_in: [parent]` — is it a sub-step of a larger skill?

## Guides

Per-skill guides live in `guides/{skill-name}.md`. Template:

```markdown
# {skill-name}

## When to use
## When NOT to use (use another skill instead)
## Core features
## Common combinations
```

Guides are embedded into the catalog JSON at extraction time.
Currently available: `maestro.md`, `team-tasks.md`.

## Note on KAS Galaxy

The 3D galaxy visualization (Knowledge-Attitude-Skill framework) has moved to the
**KAS Memory** project (`~/Claude/kas-memory/`). It visualizes the broader KAS
framework including knowledge and attitude dimensions — beyond the scope of this
skill catalog. See `~/Claude/kas-memory/KAS-GALAXY.md` for details.

## Sandbox Optimization

This skill is **sandbox-optimized**. The extraction + summarization runs inside
`sandbox_execute`, which means:

- **Full JSON** → saved to file (`~/Claude/skills/skill-catalog/`)
- **Summary only** → returned to context (~150 tokens vs ~18,400 tokens)
- **1 tool call** instead of Bash + Read (2 calls)

The key principle: **deterministic batch work stays in sandbox; presentation
logic stays with the LLM.** The sandbox extracts and aggregates data, then
the LLM formats the grouped table for the user.

## Continuous Improvement

After every invocation:

1. **Reflect** — What worked, what caused friction
2. **Record** — Append to `lessons.md`
3. **Refine** — Update SKILL.md when a pattern recurs (2+ times)

## Additional Resources

### Scripts
- **`scripts/extract_catalog.py`** — Extract structured metadata from all skills.
  Usage: `python3 extract_catalog.py [--skills-dir DIR] [--output FILE] [--format json|csv] [--skill NAME]`

### Legacy (archived, not part of current workflow)
- **`scripts/generate_viewer.py`** — HTML graph viewer generator (superseded by KAS Galaxy)
- **`assets/viewer-template-3d.html`** — 3D template (moved to KAS Memory scope)
- **`assets/viewer-template.html`** — Legacy 2D template
