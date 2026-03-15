---
name: skill-catalog
description: "Skill Catalog"
version: 0.6.0
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

**Primary (Bash mode)** — extract + summarize in one call, ~99% less context:

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
- `--health` for health/quality report
- `--pipeline` for pipeline compatibility matrix

Each skill entry contains:

| Field | Description |
|-------|-------------|
| name | Skill identifier |
| version | Current version |
| **domain** | **Primary classification (3-tier: frontmatter > override > keyword)** |
| **tags** | **Cross-cutting labels (multiple per skill)** |
| **io_schema** | **MIME-based input/output declaration for pipeline discovery** |
| **health_score** | **0-100 quality score (version, io, tools, domain, tags, etc.)** |
| **health_details** | **Per-criterion breakdown with pass/fail and reasons** |
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

## Domain Reference (14 domains, 0% "general")

| Domain | Count | Description | Example Skills |
|--------|-------|-------------|----------------|
| dev-tooling | 20 | CLI, headless, MCP, git, tmux, specs | claude-code-headless, mcp-builder, blueprint, git-worktrees |
| workshop-ops | 13 | Workshop module/station management | anvil, sentinel, finance, memvault, envkit |
| skill-meta | 12 | Managing skills themselves | create-skill, skill-optimizer, skill-curator |
| visual-design | 11 | Diagrams, images, UI, design | diagram-gen, image-gen, frontend-design, theme-factory |
| media | 11 | Audio, video, screen, 3D | stt, tts, video-core, screen-record, live3d |
| content-creation | 6 | Writing and drafting text | content-writer, marketing-copy, readme-gen |
| analysis | 5 | Data/competitor/meeting analysis | competitive-intel, meeting-insights, cannibalize |
| debugging | 4 | Debugging, testing, review | four-step-debug, tdd, systematic-debugging |
| document-output | 4 | Formatted documents | pdf, docx, pptx, xlsx |
| knowledge-mgmt | 4 | Research, search, knowledge | notebookllm, explain-visual, openclaw-mentor |
| communication | 4 | Messaging, social, quotes | message-polish, quote-builder, social-content |
| orchestration | 3 | Multi-agent coordination | forge, maestro, team-tasks |
| ideation | 3 | Brainstorming, model selection | brainstorming, divergent-thinking, model-mentor |
| reference | 2 | Embedded reference materials | _ref-review-criteria, _ref-workshop-patterns |

### Domain Classification Precedence
1. **Frontmatter `domain:`** — explicit declaration in SKILL.md (highest priority)
2. **DOMAIN_OVERRIDES** — manually curated mapping in extract_catalog.py
3. **Keyword matching** — fallback based on description + pain_point text

## Tag Reference (21 tags)

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
| audio | audio, speech, voice, transcription, sound |
| video | video, screen record, subtitle, caption |
| workshop | workshop, station, module, sentinel, envkit |

## Health Score (0-100)

Each skill gets a quality score based on 9 criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| has_version | 10 | Version declared in frontmatter |
| has_io_schema | 15 | `io:` MIME schema for pipeline discovery |
| has_tools | 10 | Tools list declared |
| classified_domain | 15 | Not falling into "general" |
| has_tags | 10 | At least one tag matched |
| has_pain_point | 10 | Purpose extracted after H1 |
| body_lines_ok | 10 | Between 20-500 lines |
| has_scripts | 10 | Has content in scripts/ |
| has_guide | 10 | Has guide in guides/ |

Run `--health` to see the full report with distribution, critical skills, and top gaps.

## Pipeline Compatibility (IO Schema)

Skills declaring `io:` in frontmatter enable MIME-based pipeline discovery:

```yaml
io:
  input:
    - mime: "text/markdown"
      description: "Research query"
  output:
    - mime: "application/json"
      description: "Structured report"
```

**Rule**: Skill B can follow Skill A if `A.output[].mime ∩ B.input[].mime ≠ ∅`

Run `--pipeline` to see the compatibility matrix and hub analysis.

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

This skill is **sandbox-optimized**. Batch operations run inside `sandbox_execute`:

- **Catalog extraction**: Import `scripts/extract_catalog.py` in sandbox to scan all skills and return structured JSON — `~/.claude/` imports are now supported
- **Summary generation**: Sandbox saves full JSON to `~/Claude/` and returns only the grouped summary (~100 tokens); LLM formats the table for the user

Fallback (Bash):
- `python3 ~/.claude/skills/skill-catalog/scripts/extract_catalog.py` — run extraction via Bash when sandbox is unavailable

The key principle: **deterministic batch work → sandbox; presentation logic → LLM.**

## Continuous Improvement

After every invocation:

1. **Reflect** — What worked, what caused friction
2. **Record** — Append to `lessons.md`
3. **Refine** — Update SKILL.md when a pattern recurs (2+ times)

## Additional Resources

### Scripts
- **`scripts/extract_catalog.py`** — Extract structured metadata from all skills.
  Usage: `python3 extract_catalog.py [--skills-dir DIR] [--output FILE] [--format json|csv] [--skill NAME] [--health] [--pipeline]`
