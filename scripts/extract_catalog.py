#!/usr/bin/env python3
"""Extract structured catalog from all installed skills.

Usage:
    python3 extract_catalog.py [--skills-dir DIR] [--output FILE] [--format json|csv]

Output fields per skill:
    name, version, domain, tags, strengths, pain_point, triggers, tools, body_lines, resources
"""

import argparse
import csv
import io
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_SKILLS_DIR = os.path.expanduser("~/.claude/skills")

# Import cold-skill description fallback
sys.path.insert(0, os.path.expanduser("~/.claude/data/skill-index"))
try:
    from resolve_description import resolve_from_frontmatter
except ImportError:

    def resolve_from_frontmatter(fm, name):
        return fm.get("description", "")


# Tool → strength mapping
TOOL_STRENGTHS = {
    "Bash": "system operations",
    "WebSearch": "web research",
    "Read": "file analysis",
    "Write": "file generation",
    "Edit": "code editing",
    "Glob": "file discovery",
    "Grep": "content search",
    "Task": "agent orchestration",
}

DOMAIN_KEYWORDS = {
    "content-creation": [
        "write",
        "draft",
        "article",
        "blog",
        "copy",
        "content",
        "newsletter",
        "marketing",
        "email",
        "ad copy",
        "social media",
    ],
    "document-output": [
        "pdf",
        "docx",
        "pptx",
        "xlsx",
        "word",
        "excel",
        "powerpoint",
        "spreadsheet",
        "presentation",
        "slides",
        "document",
        "merge",
        "split",
        "watermark",
    ],
    "visual-design": [
        "diagram",
        "image",
        "canvas",
        "poster",
        "visual",
        "design",
        "ui",
        "ux",
        "frontend",
        "landing page",
        "theme",
        "brand",
        "color",
        "draw",
        "art",
        "render",
        "infographic",
        "generate an image",
    ],
    "dev-tooling": [
        "headless",
        "cli",
        "codex",
        "gemini",
        "claude",
        "mcp",
        "server",
        "script",
        "pipeline",
        "ci/cd",
        "sdk",
    ],
    "orchestration": [
        "orchestrate",
        "dispatch",
        "multi-agent",
        "parallel",
        "pipeline",
        "coordinate",
        "dag",
        "conductor",
    ],
    "knowledge-mgmt": [
        "notebooklm",
        "notebook",
        "research",
        "documentation",
        "wiki",
        "audio overview",
        "knowledge base",
    ],
    "skill-meta": [
        "optimize",
        "publish",
        "curate",
        "organize",
        "catalog",
        "inventory",
        "metadata",
        "maintenance",
        "lifecycle",
        "readme",
        "spec",
    ],
    "analysis": [
        "analyze",
        "competitor",
        "meeting",
        "insights",
        "audit",
        "communication",
        "comparison",
        "competitive",
        "intel",
    ],
    "ideation": ["brainstorm", "ideation", "explore", "decide", "approach", "recommend"],
}

# --- Domain: mutually exclusive, one per skill ---
# Priority order: more specific domains win over generic ones.
# visual-design before document-output (canvas-design is visual, not doc)
# analysis before knowledge-mgmt (competitive-intel is analysis, not knowledge)
# skill-meta near end to avoid over-matching
DOMAIN_PRIORITY = [
    "orchestration",
    "dev-tooling",
    "visual-design",
    "document-output",
    "analysis",
    "content-creation",
    "knowledge-mgmt",
    "ideation",
    "skill-meta",
]

# --- Tags: cross-cutting, multiple per skill ---
TAG_KEYWORDS = {
    "browser": ["browser", "playwright", "chrome", "web page"],
    "headless": ["headless", "-p", "pipe", "programmatic", "cron", "ci/cd"],
    "notebooklm": ["notebooklm", "notebook", "audio overview"],
    "github": ["github", "git", "pull request", "pr", "repo"],
    "mermaid": ["mermaid", "flowchart", "sequence diagram"],
    "ai-image": [
        "image gen",
        "generate an image",
        "grok",
        "dall-e",
        "midjourney",
        "flux",
        "stable diffusion",
    ],
    "multi-agent": [
        "multi-agent",
        "orchestrate",
        "dispatch",
        "parallel",
        "team",
        "coordinate",
        "pipeline",
    ],
    "search": ["search", "research", "look up", "documentation", "query"],
    "writing": ["write", "draft", "article", "blog", "copy", "content", "newsletter"],
    "code": ["code", "debug", "review", "cli", "codex", "sdk", "mcp"],
    "data": ["csv", "xlsx", "spreadsheet", "data", "chart", "formula"],
    "design": [
        "design",
        "ui",
        "ux",
        "frontend",
        "landing page",
        "theme",
        "brand",
        "poster",
        "canvas",
        "visual",
    ],
    "pdf": ["pdf", "merge", "split", "watermark", "ocr"],
    "slides": ["pptx", "presentation", "slide", "deck", "pitch"],
    "chinese": ["繁體", "中文", "zh-tw", "台灣"],
    "llm": ["model", "recommend", "llm", "gpt", "claude", "gemini"],
    "spec": ["spec", "specification", "sdd", "implementation plan"],
    "marketing": ["marketing", "ad copy", "competitor", "positioning", "campaign"],
}


def _strip_boilerplate(desc: str) -> str:
    """Strip common boilerplate prefixes from skill descriptions.

    Most descriptions start with 'This skill should be used when the user asks to ...'
    or 'Use this skill when/whenever ...' which pollutes keyword matching.
    """
    patterns = [
        r"^This skill should be used when(?:\s+the user\s+(?:asks?\s+to|wants?\s+to|mentions?|discusses?))?\s*",
        r"^Use this skill\s+(?:when(?:ever)?|any\s+time)\s+",
        r"^You should use this skill when\s+",
    ]
    for pat in patterns:
        stripped = re.sub(pat, "", desc, flags=re.IGNORECASE)
        if stripped != desc:
            return stripped
    return desc


def _kw_matches(kw: str, text: str) -> bool:
    """Match keyword in text with word-boundary awareness.

    Single words use \\b word boundaries to avoid partial matches
    (e.g., 'art' won't match 'watermark', 'ui' won't match 'build').
    Multi-word phrases use substring matching (already specific enough).
    """
    if " " in kw or "/" in kw or "-" in kw:
        return kw in text
    return bool(re.search(r"\b" + re.escape(kw) + r"\b", text))


def parse_frontmatter(skill_path: Path) -> dict:
    """Parse YAML frontmatter from SKILL.md."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {}

    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}

    fm = {}
    raw = match.group(1)
    current_key = None
    current_val = []

    for line in raw.split("\n"):
        kv = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if kv:
            if current_key and current_val:
                fm[current_key] = " ".join(current_val).strip()
            current_key = kv.group(1)
            val = kv.group(2).strip()
            if val and val != ">-":
                current_val = [val]
            else:
                current_val = []
        elif current_key and line.strip():
            current_val.append(line.strip())

    if current_key and current_val:
        fm[current_key] = " ".join(current_val).strip()

    return fm


def extract_triggers(description: str) -> list:
    """Extract quoted trigger phrases from description."""
    return re.findall(r'"([^"]+)"', description)


def extract_pain_point(skill_path: Path) -> str:
    """Extract the purpose/pain-point from the first paragraph after H1."""
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")

    # Strip frontmatter
    content = re.sub(r"^---.*?---\s*", "", content, flags=re.DOTALL)

    # Find first paragraph after H1
    lines = content.strip().split("\n")
    past_h1 = False
    para = []
    for line in lines:
        if line.startswith("# "):
            past_h1 = True
            continue
        if past_h1:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                para.append(stripped)
            elif para:
                break

    return " ".join(para)[:300] if para else ""


def classify_domains(description: str, pain_point: str = "") -> dict:
    """Classify skill into domains with scores.

    Uses stripped description (no boilerplate) + pain_point for matching.
    Returns dict of {domain: score} for domains with score >= 2.
    """
    clean_desc = _strip_boilerplate(description)
    combined = (clean_desc + " " + pain_point).lower()
    scored = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if _kw_matches(kw, combined))
        if score >= 2:
            scored[domain] = score
    return scored or {"general": 0}


def classify_domain(scored: dict) -> str:
    """Pick a single primary domain from scored signals.

    Highest score wins. DOMAIN_PRIORITY is used only as a tiebreaker
    when two domains have the same score.
    If no signal matched, returns 'general'.
    """
    if not scored or scored == {"general": 0}:
        return "general"

    max_score = max(scored.values())
    top = [d for d, s in scored.items() if s == max_score]

    if len(top) == 1:
        return top[0]

    # Tiebreak by priority
    for d in DOMAIN_PRIORITY:
        if d in top:
            return d
    return top[0]


def extract_tags(description: str, pain_point: str) -> list:
    """Extract cross-cutting tags from description + pain_point (multi-label)."""
    combined = (description + " " + pain_point).lower()
    tags = []
    for tag, keywords in TAG_KEYWORDS.items():
        if any(_kw_matches(kw, combined) for kw in keywords):
            tags.append(tag)
    return sorted(tags)


def derive_strengths(tools: list, scored_domains: dict) -> list:
    """Derive skill strengths from tools and matched domains."""
    strengths = []
    for tool in tools:
        if tool in TOOL_STRENGTHS:
            strengths.append(TOOL_STRENGTHS[tool])
    # Add domain-based strengths
    domain_strength = {
        "content-creation": "content writing",
        "document-output": "document generation",
        "visual-design": "visual design",
        "dev-tooling": "developer tooling",
        "orchestration": "workflow orchestration",
        "knowledge-mgmt": "knowledge management",
        "skill-meta": "skill management",
        "analysis": "data analysis",
        "ideation": "creative ideation",
    }
    for d in scored_domains:
        if d in domain_strength and domain_strength[d] not in strengths:
            strengths.append(domain_strength[d])
    return strengths


def extract_skill(skill_path: Path, guides_dir: Path = None):
    """Extract structured metadata from a single skill."""
    fm = parse_frontmatter(skill_path)
    if not fm:
        return None

    name = fm.get("name", skill_path.name)
    description = resolve_from_frontmatter(fm, skill_path.name)
    tools = [t.strip() for t in fm.get("tools", "").split(",") if t.strip()]
    version = fm.get("version", "")
    triggers = extract_triggers(description)
    pain_point = extract_pain_point(skill_path)
    _scored = classify_domains(description, pain_point)
    domain = classify_domain(_scored)
    tags = extract_tags(description, pain_point)
    strengths = derive_strengths(tools, _scored)

    # Count resources
    scripts_dir = skill_path / "scripts"
    refs_dir = skill_path / "references"
    assets_dir = skill_path / "assets"
    scripts = (
        [f for f in scripts_dir.glob("*") if f.name != ".gitkeep"] if scripts_dir.exists() else []
    )
    refs = (
        [f for f in refs_dir.glob("*") if f.name not in (".gitkeep", "guide.md")]
        if refs_dir.exists()
        else []
    )
    assets = (
        [f for f in assets_dir.glob("*") if f.name != ".gitkeep"] if assets_dir.exists() else []
    )

    body_lines = len((skill_path / "SKILL.md").read_text(encoding="utf-8").splitlines())

    # Guide content (Traditional Chinese documentation)
    guide = ""
    if guides_dir:
        guide_file = guides_dir / f"{skill_path.name}.md"
        if guide_file.exists():
            guide = guide_file.read_text(encoding="utf-8")

    return {
        "name": name,
        "version": version,
        "domain": domain,
        "tags": tags,
        "strengths": strengths,
        "pain_point": pain_point,
        "triggers": triggers,
        "tools": tools,
        "body_lines": body_lines,
        "resources": {
            "scripts": len(scripts),
            "references": len(refs),
            "assets": len(assets),
        },
        "guide": guide,
    }


def main():
    parser = argparse.ArgumentParser(description="Extract skill catalog")
    parser.add_argument("--skills-dir", default=DEFAULT_SKILLS_DIR)
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_argument("--skill", help="Single skill name to extract")
    parser.add_argument(
        "--guides-dir",
        default=str(Path(__file__).parent.parent / "guides"),
        help="Directory containing per-skill guide .md files",
    )
    args = parser.parse_args()

    skills_path = Path(args.skills_dir)
    guides_path = Path(args.guides_dir)
    catalog = []

    for d in sorted(skills_path.iterdir()):
        if not d.is_dir() or d.name.startswith("."):
            continue
        if args.skill and d.name != args.skill:
            continue
        entry = extract_skill(d, guides_dir=guides_path)
        if entry:
            catalog.append(entry)

    if args.format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(
            [
                "name",
                "version",
                "domain",
                "tags",
                "strengths",
                "pain_point",
                "triggers",
                "tools",
                "body_lines",
                "scripts",
                "references",
                "assets",
            ]
        )
        for e in catalog:
            writer.writerow(
                [
                    e["name"],
                    e["version"],
                    e["domain"],
                    "; ".join(e["tags"]),
                    "; ".join(e["strengths"]),
                    e["pain_point"],
                    "; ".join(e["triggers"]),
                    "; ".join(e["tools"]),
                    e["body_lines"],
                    e["resources"]["scripts"],
                    e["resources"]["references"],
                    e["resources"]["assets"],
                ]
            )
        result = output.getvalue()
    else:
        result = json.dumps(catalog, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Catalog written to {args.output} ({len(catalog)} skills)", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
