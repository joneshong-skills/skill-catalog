#!/usr/bin/env python3
"""Extract structured catalog from all installed skills.

Usage:
    python3 extract_catalog.py [--skills-dir DIR] [--output FILE] [--format json|csv]
    python3 extract_catalog.py --health           # Health report (quality scores)
    python3 extract_catalog.py --pipeline          # Pipeline compatibility matrix

Output fields per skill:
    name, version, domain, tags, strengths, pain_point, triggers, tools,
    body_lines, resources, io_schema, health_score, health_details
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


# ===== Constants =====

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

# --- Manual domain overrides ---
# Highest-effort classification for skills that keyword matching cannot resolve.
# Precedence: frontmatter domain: > DOMAIN_OVERRIDES > keyword matching
DOMAIN_OVERRIDES = {
    # media
    "stt": "media",
    "tts": "media",
    "ocr": "media",
    "ocr-claude-api": "media",
    "video-audio": "media",
    "video-core": "media",
    "video-edit": "media",
    "video-mix": "media",
    "screen-record": "media",
    "social-media-dl": "media",
    "live3d": "media",
    # workshop-ops
    "anvil": "workshop-ops",
    "capture": "workshop-ops",
    "finance": "workshop-ops",
    "intelflow": "workshop-ops",
    "memvault": "workshop-ops",
    "nodeflow": "workshop-ops",
    "scheduler": "workshop-ops",
    "sentinel": "workshop-ops",
    "envkit": "workshop-ops",
    "session-intelligence": "workshop-ops",
    "session-redactor": "workshop-ops",
    "system-map": "workshop-ops",
    "system-monitor": "workshop-ops",
    # debugging
    "four-step-debug": "debugging",
    "systematic-debugging": "debugging",
    "tdd": "debugging",
    "code-review-interceptor": "debugging",
    # communication
    "message-polish": "communication",
    "quote-builder": "communication",
    "quote-consultant": "communication",
    "social-content": "communication",
    # dev-tooling
    "claude-code-headless": "dev-tooling",
    "codex-cli-headless": "dev-tooling",
    "gemini-cli-headless": "dev-tooling",
    "mcp-builder": "dev-tooling",
    "git-worktrees": "dev-tooling",
    "github-pm": "dev-tooling",
    "tmux-expert": "dev-tooling",
    "tmux-relay": "dev-tooling",
    "playground": "dev-tooling",
    "executor": "dev-tooling",
    "sandbox-patterns": "dev-tooling",
    "macos-ui-automation": "dev-tooling",
    "webcrawl": "dev-tooling",
    "sync-config": "dev-tooling",
    "blueprint": "dev-tooling",
    "spec-kit": "dev-tooling",
    "iterative-optimize": "dev-tooling",
    "verification-before-completion": "dev-tooling",
    # orchestration
    "forge": "orchestration",
    "maestro": "orchestration",
    "team-tasks": "orchestration",
    # knowledge-mgmt
    "notebookllm": "knowledge-mgmt",
    "notebookllm-visual": "knowledge-mgmt",
    "explain-visual": "knowledge-mgmt",
    "openclaw-mentor": "knowledge-mgmt",
    # analysis
    "competitive-intel": "analysis",
    "company-intel": "analysis",
    "cannibalize": "analysis",
    "meeting-insights": "analysis",
    "synergy-weaver": "analysis",
    # ideation
    "divergent-thinking": "ideation",
    "brainstorming": "ideation",
    "model-mentor": "ideation",
    # skill-meta
    "create-skill": "skill-meta",
    "create-agent": "skill-meta",
    "create-command": "skill-meta",
    "skill-curator": "skill-meta",
    "skill-proxy": "skill-meta",
    "skill-security-scan": "skill-meta",
    "skill-tester": "skill-meta",
    "skill-publisher": "skill-meta",
    "skill-optimizer": "skill-meta",
    "skill-lifecycle": "skill-meta",
    "skill-graph": "skill-meta",
    "skill-catalog": "skill-meta",
    # visual-design
    "image-gen": "visual-design",
    "image-edit": "visual-design",
    "image-prompt": "visual-design",
    "diagram-gen": "visual-design",
    "canvas-design": "visual-design",
    "pencil-design": "visual-design",
    "frontend-design": "visual-design",
    "theme-factory": "visual-design",
    "brand-guidelines": "visual-design",
    "ui-audit": "visual-design",
    "blink-builder": "visual-design",
    # content-creation
    "content-writer": "content-creation",
    "marketing-copy": "content-creation",
    "readme-gen": "content-creation",
    "changelog-gen": "content-creation",
    "doc-coauthoring": "content-creation",
    "docs-butler": "content-creation",
    # document-output
    "pdf": "document-output",
    "docx": "document-output",
    "pptx": "document-output",
    "xlsx": "document-output",
    # reference
    "_ref-review-criteria": "reference",
    "_ref-workshop-patterns": "reference",
}

# --- Domain keyword matching (fallback when no override/frontmatter) ---
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
        "readme",
        "changelog",
        "co-author",
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
        "pencil",
        "wireframe",
        "mockup",
        "prototype",
        "icon",
        "logo",
        "avatar",
    ],
    "dev-tooling": [
        "headless",
        "codex",
        "gemini",
        "mcp",
        "server",
        "script",
        "ci/cd",
        "sdk",
        "tmux",
        "build",
        "deploy",
        "sandbox",
        "playground",
        "blueprint",
        "webcrawl",
        "crawl",
        "git worktree",
        "executor",
    ],
    "orchestration": [
        "orchestrate",
        "dispatch",
        "multi-agent",
        "parallel",
        "coordinate",
        "dag",
        "conductor",
        "forge",
        "maestro",
    ],
    "knowledge-mgmt": [
        "notebooklm",
        "notebook",
        "research",
        "wiki",
        "audio overview",
        "knowledge base",
        "semantic search",
        "recall",
        "memory",
        "explain",
        "mentor",
        "learning",
    ],
    "skill-meta": [
        "skill",
        "publish",
        "curate",
        "catalog",
        "inventory",
        "metadata",
        "maintenance",
        "lifecycle",
        "create-skill",
        "skill-graph",
        "skill-proxy",
    ],
    "analysis": [
        "analyze",
        "competitor",
        "meeting",
        "insights",
        "audit",
        "comparison",
        "competitive",
        "intel",
        "cannibalize",
        "synergy",
        "benchmark",
        "evaluate",
    ],
    "ideation": [
        "brainstorm",
        "ideation",
        "explore",
        "decide",
        "approach",
        "recommend",
        "divergent",
        "creative",
        "model selection",
    ],
    "media": [
        "audio",
        "video",
        "speech",
        "transcri",
        "voice",
        "sound",
        "recording",
        "subtitle",
        "caption",
        "screen record",
        "download",
        "3d",
        "avatar",
        "vroid",
    ],
    "workshop-ops": [
        "sentinel",
        "envkit",
        "session",
        "system monitor",
        "capture",
        "hook",
        "observatory",
        "remediation",
        "service registry",
        "finance module",
        "intelflow module",
        "memvault module",
    ],
    "debugging": [
        "debug",
        "troubleshoot",
        "diagnose",
        "error",
        "bug",
        "stack trace",
        "root cause",
        "four-step",
        "systematic",
        "test-driven",
    ],
    "communication": [
        "message",
        "polish",
        "quote",
        "social post",
        "email draft",
        "professional",
        "tone",
        "wording",
    ],
}

# Domain tiebreak priority (more specific first)
DOMAIN_PRIORITY = [
    "orchestration",
    "media",
    "workshop-ops",
    "debugging",
    "communication",
    "dev-tooling",
    "visual-design",
    "document-output",
    "analysis",
    "content-creation",
    "knowledge-mgmt",
    "ideation",
    "skill-meta",
    "reference",
]

# Cross-cutting tags (multi-label)
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
    "audio": ["audio", "speech", "voice", "transcri", "sound", "tts", "stt"],
    "video": ["video", "screen record", "subtitle", "caption", "ffmpeg"],
    "workshop": ["workshop", "station", "module", "sentinel", "envkit"],
}

# Health score weights (total = 100)
HEALTH_WEIGHTS = {
    "has_version": 10,
    "has_io_schema": 15,
    "has_tools": 10,
    "classified_domain": 15,
    "has_tags": 10,
    "has_pain_point": 10,
    "body_lines_ok": 10,
    "has_scripts": 10,
    "has_guide": 10,
}


# ===== Utility Functions =====


def _strip_boilerplate(desc: str) -> str:
    """Strip common boilerplate prefixes from skill descriptions."""
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
    """Match keyword in text with word-boundary awareness."""
    if " " in kw or "/" in kw or "-" in kw:
        return kw in text
    return bool(re.search(r"\b" + re.escape(kw) + r"\b", text))


# ===== Frontmatter Parsing =====


def parse_frontmatter(skill_path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter from SKILL.md.

    Returns (parsed_dict, raw_frontmatter_text).
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {}, ""

    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}, ""

    raw = match.group(1)
    fm = {}
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

    return fm, raw


# ===== IO Schema Extraction =====


def extract_io_schema(raw_frontmatter: str) -> dict:
    """Extract io: schema from raw frontmatter YAML.

    Parses the nested io: block into:
    {
        "input": [{"mime": "...", "description": "..."}],
        "output": [{"mime": "...", "description": "..."}]
    }
    """
    # Find io: block in raw frontmatter
    io_match = re.search(r"^io:\s*$", raw_frontmatter, re.MULTILINE)
    if not io_match:
        return {}

    # Extract indented block after io:
    lines = raw_frontmatter[io_match.end() :].split("\n")
    io_lines = []
    for line in lines:
        if line and not line[0].isspace() and line.strip():
            break  # Hit next top-level key
        io_lines.append(line)

    io_text = "\n".join(io_lines)
    result = {"input": [], "output": []}

    for direction in ("input", "output"):
        dir_match = re.search(rf"^\s+{direction}:\s*$", io_text, re.MULTILINE)
        if not dir_match:
            continue

        # Extract entries after direction:
        remaining = io_text[dir_match.end() :]
        for entry_match in re.finditer(
            r"-\s+mime:\s*[\"']?([^\"'\n]+)[\"']?\s*\n\s+description:\s*[\"']?([^\"'\n]+)[\"']?",
            remaining,
        ):
            result[direction].append(
                {
                    "mime": entry_match.group(1).strip(),
                    "description": entry_match.group(2).strip(),
                }
            )
            # Stop if we hit the other direction's section
        other = "output" if direction == "input" else "input"
        other_match = re.search(rf"^\s+{other}:", remaining, re.MULTILINE)
        if other_match:
            remaining = remaining[: other_match.start()]
            result[direction] = []
            for entry_match in re.finditer(
                r"-\s+mime:\s*[\"']?([^\"'\n]+)[\"']?\s*\n\s+description:\s*[\"']?([^\"'\n]+)[\"']?",
                remaining,
            ):
                result[direction].append(
                    {
                        "mime": entry_match.group(1).strip(),
                        "description": entry_match.group(2).strip(),
                    }
                )

    if not result["input"] and not result["output"]:
        return {}
    return result


# ===== Health Score =====


def compute_health_score(entry: dict) -> tuple[int, dict]:
    """Compute health score (0-100) for a skill entry.

    Returns (total_score, {criterion: {score, max, reason}}).
    """
    details = {}

    def _check(key, condition, reason_pass="", reason_fail=""):
        w = HEALTH_WEIGHTS[key]
        ok = bool(condition)
        details[key] = {
            "score": w if ok else 0,
            "max": w,
            "pass": ok,
            "reason": reason_pass if ok else reason_fail,
        }

    _check(
        "has_version",
        entry.get("version"),
        "version declared",
        "no version in frontmatter",
    )
    _check(
        "has_io_schema",
        entry.get("io_schema"),
        f"{len(entry.get('io_schema', {}).get('input', []))}in/{len(entry.get('io_schema', {}).get('output', []))}out",
        "no io: schema — pipeline discovery disabled",
    )
    _check(
        "has_tools",
        entry.get("tools"),
        f"{len(entry['tools'])} tools",
        "no tools declared",
    )
    _check(
        "classified_domain",
        entry.get("domain", "general") != "general",
        f"domain: {entry.get('domain')}",
        "unclassified (general)",
    )
    _check(
        "has_tags",
        entry.get("tags"),
        f"{len(entry['tags'])} tags",
        "no tags matched",
    )
    _check(
        "has_pain_point",
        entry.get("pain_point"),
        "purpose extracted",
        "no purpose/pain_point found after H1",
    )

    lines = entry.get("body_lines", 0)
    _check(
        "body_lines_ok",
        20 <= lines <= 500,
        f"{lines} lines (good)",
        f"{lines} lines ({'too short' if lines < 20 else 'over 500 limit'})",
    )
    _check(
        "has_scripts",
        entry.get("resources", {}).get("scripts", 0) > 0,
        f"{entry['resources']['scripts']} scripts",
        "no scripts/ directory content",
    )
    _check(
        "has_guide",
        entry.get("guide"),
        "guide available",
        "no guide in guides/ directory",
    )

    total = sum(d["score"] for d in details.values())
    return total, details


# ===== Pipeline Matrix =====


def _mime_compatible(output_mime: str, input_mime: str) -> bool:
    """Check if output MIME type is compatible with input MIME type.

    Supports wildcard matching: audio/* matches audio/wav, audio/mp3, etc.
    """
    if output_mime == input_mime:
        return True
    # Wildcard: audio/* matches audio/anything
    if "*" in input_mime:
        in_type = input_mime.split("/")[0]
        out_type = output_mime.split("/")[0]
        return in_type == out_type
    if "*" in output_mime:
        in_type = input_mime.split("/")[0]
        out_type = output_mime.split("/")[0]
        return in_type == out_type
    return False


def generate_pipeline_matrix(catalog: list) -> list:
    """Find compatible skill pairs based on io: MIME matching.

    Returns list of {from, to, via_mime, from_desc, to_desc} connections.
    """
    connections = []
    io_skills = [s for s in catalog if s.get("io_schema")]

    for src in io_skills:
        for out_entry in src["io_schema"].get("output", []):
            for dst in io_skills:
                if dst["name"] == src["name"]:
                    continue
                for in_entry in dst["io_schema"].get("input", []):
                    if _mime_compatible(out_entry["mime"], in_entry["mime"]):
                        connections.append(
                            {
                                "from": src["name"],
                                "to": dst["name"],
                                "via_mime": out_entry["mime"],
                                "from_desc": out_entry["description"],
                                "to_desc": in_entry["description"],
                            }
                        )
    return connections


# ===== Domain Classification =====


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


def classify_domain(
    scored: dict,
    skill_name: str = "",
    fm_domain: str = "",
    fm_category: str = "",
) -> str:
    """Pick a single primary domain.

    Precedence:
    1. frontmatter domain: / category: (explicit declaration)
    2. DOMAIN_OVERRIDES (manual curation)
    3. Keyword matching (scored dict)
    """
    # 1. Frontmatter explicit declaration
    if fm_domain and fm_domain in DOMAIN_PRIORITY:
        return fm_domain
    if fm_category and fm_category in DOMAIN_PRIORITY:
        return fm_category

    # 2. Manual override
    if skill_name in DOMAIN_OVERRIDES:
        return DOMAIN_OVERRIDES[skill_name]

    # 3. Keyword matching
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


# ===== Extraction =====


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
        "media": "media processing",
        "workshop-ops": "workshop operations",
        "debugging": "debugging & testing",
        "communication": "professional communication",
    }
    for d in scored_domains:
        if d in domain_strength and domain_strength[d] not in strengths:
            strengths.append(domain_strength[d])
    return strengths


def extract_skill(skill_path: Path, guides_dir: Path = None):
    """Extract structured metadata from a single skill."""
    fm, raw_fm = parse_frontmatter(skill_path)
    if not fm:
        return None

    name = fm.get("name", skill_path.name)
    description = resolve_from_frontmatter(fm, skill_path.name)
    tools = [t.strip() for t in fm.get("tools", "").split(",") if t.strip()]
    version = fm.get("version", "")
    triggers = extract_triggers(description)
    pain_point = extract_pain_point(skill_path)

    # Domain classification (3-tier: frontmatter > override > keyword)
    _scored = classify_domains(description, pain_point)
    fm_domain = fm.get("domain", "").strip().strip('"').strip("'")
    fm_category = fm.get("category", "").strip().strip('"').strip("'")
    domain = classify_domain(
        _scored,
        skill_name=skill_path.name,
        fm_domain=fm_domain,
        fm_category=fm_category,
    )

    tags = extract_tags(description, pain_point)
    strengths = derive_strengths(tools, _scored)

    # IO schema
    io_schema = extract_io_schema(raw_fm)

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

    # Guide content
    guide = ""
    if guides_dir:
        guide_file = guides_dir / f"{skill_path.name}.md"
        if guide_file.exists():
            guide = guide_file.read_text(encoding="utf-8")

    entry = {
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
        "io_schema": io_schema,
        "guide": guide,
    }

    # Health score
    score, details = compute_health_score(entry)
    entry["health_score"] = score
    entry["health_details"] = details

    return entry


# ===== Output Formatters =====


def format_health_report(catalog: list) -> str:
    """Format a health report sorted by score (worst first)."""
    lines = []

    # Summary
    scores = [s["health_score"] for s in catalog]
    avg = sum(scores) / len(scores) if scores else 0
    critical = [s for s in catalog if s["health_score"] < 40]
    healthy = [s for s in catalog if s["health_score"] >= 70]

    lines.append(f"# Skill Health Report ({len(catalog)} skills)")
    lines.append("")
    lines.append(
        f"Average: {avg:.0f}/100 | Healthy (≥70): {len(healthy)} | Critical (<40): {len(critical)}"
    )
    lines.append("")

    # Distribution
    buckets = {"90-100": 0, "70-89": 0, "50-69": 0, "30-49": 0, "0-29": 0}
    for s in scores:
        if s >= 90:
            buckets["90-100"] += 1
        elif s >= 70:
            buckets["70-89"] += 1
        elif s >= 50:
            buckets["50-69"] += 1
        elif s >= 30:
            buckets["30-49"] += 1
        else:
            buckets["0-29"] += 1

    lines.append("## Distribution")
    for bucket, count in buckets.items():
        bar = "█" * count
        lines.append(f"  {bucket}: {bar} ({count})")
    lines.append("")

    # Critical skills detail
    if critical:
        lines.append("## Critical Skills (score < 40)")
        lines.append("")
        lines.append("| Skill | Score | Missing |")
        lines.append("|-------|-------|---------|")
        for s in critical:
            missing = [
                k.replace("has_", "").replace("_", " ")
                for k, v in s["health_details"].items()
                if not v["pass"]
            ]
            lines.append(f"| {s['name']} | {s['health_score']}/100 | {', '.join(missing)} |")
        lines.append("")

    # Top improvement opportunities (biggest gaps)
    lines.append("## Top Improvement Opportunities")
    lines.append("")
    gap_counts = {}
    for s in catalog:
        for k, v in s["health_details"].items():
            if not v["pass"]:
                gap_counts[k] = gap_counts.get(k, 0) + 1

    for gap, count in sorted(gap_counts.items(), key=lambda x: -x[1]):
        pct = count / len(catalog) * 100
        label = gap.replace("has_", "").replace("_", " ")
        lines.append(f"  - **{label}**: {count}/{len(catalog)} skills ({pct:.0f}%) missing")

    return "\n".join(lines)


def format_pipeline_report(catalog: list) -> str:
    """Format pipeline compatibility report."""
    connections = generate_pipeline_matrix(catalog)
    io_skills = [s for s in catalog if s.get("io_schema")]

    lines = []
    lines.append(f"# Pipeline Compatibility ({len(io_skills)} skills with io: schema)")
    lines.append("")

    if not connections:
        lines.append("No pipeline connections found. Add io: schema to more skills.")
        lines.append("")
        lines.append("## Skills without io: schema")
        no_io = [s["name"] for s in catalog if not s.get("io_schema")]
        for name in sorted(no_io):
            lines.append(f"  - {name}")
        return "\n".join(lines)

    # Group by source
    by_source = {}
    for c in connections:
        by_source.setdefault(c["from"], []).append(c)

    lines.append("## Connections")
    lines.append("")
    lines.append("| From | To | Via MIME | Description |")
    lines.append("|------|----|---------|-------------|")
    for c in sorted(connections, key=lambda x: (x["from"], x["to"])):
        lines.append(
            f"| {c['from']} | {c['to']} | `{c['via_mime']}` | {c['from_desc']} → {c['to_desc']} |"
        )
    lines.append("")

    # Hub analysis (most connected)
    hub_out = {}
    hub_in = {}
    for c in connections:
        hub_out[c["from"]] = hub_out.get(c["from"], 0) + 1
        hub_in[c["to"]] = hub_in.get(c["to"], 0) + 1

    lines.append("## Hub Skills (most connections)")
    lines.append("")
    lines.append("| Skill | Outgoing | Incoming | Total |")
    lines.append("|-------|----------|----------|-------|")
    all_hubs = set(hub_out.keys()) | set(hub_in.keys())
    for name in sorted(
        all_hubs,
        key=lambda n: hub_out.get(n, 0) + hub_in.get(n, 0),
        reverse=True,
    )[:10]:
        out = hub_out.get(name, 0)
        inp = hub_in.get(name, 0)
        lines.append(f"| {name} | {out} | {inp} | {out + inp} |")

    # Coverage gap
    lines.append("")
    lines.append(
        f"## Coverage: {len(io_skills)}/{len(catalog)} skills have io: schema ({len(io_skills) / len(catalog) * 100:.0f}%)"
    )

    return "\n".join(lines)


# ===== Main =====


def main():
    parser = argparse.ArgumentParser(description="Extract skill catalog v0.6.0")
    parser.add_argument("--skills-dir", default=DEFAULT_SKILLS_DIR)
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_argument("--skill", help="Single skill name to extract")
    parser.add_argument("--health", action="store_true", help="Show health report")
    parser.add_argument("--pipeline", action="store_true", help="Show pipeline compatibility")
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

    # Special output modes
    if args.health:
        report = format_health_report(catalog)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"Health report written to {args.output}", file=sys.stderr)
        else:
            print(report)
        return

    if args.pipeline:
        report = format_pipeline_report(catalog)
        if args.output:
            Path(args.output).write_text(report, encoding="utf-8")
            print(f"Pipeline report written to {args.output}", file=sys.stderr)
        else:
            print(report)
        return

    # Standard output
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
                "health_score",
                "io_input_mimes",
                "io_output_mimes",
            ]
        )
        for e in catalog:
            io_in = "; ".join(x["mime"] for x in e.get("io_schema", {}).get("input", []))
            io_out = "; ".join(x["mime"] for x in e.get("io_schema", {}).get("output", []))
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
                    e.get("health_score", 0),
                    io_in,
                    io_out,
                ]
            )
        result = output.getvalue()
    else:
        result = json.dumps(catalog, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(
            f"Catalog written to {args.output} ({len(catalog)} skills)",
            file=sys.stderr,
        )
    else:
        print(result)


if __name__ == "__main__":
    main()
