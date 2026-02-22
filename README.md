[English](README.md) | [繁體中文](README.zh.md)

# skill-catalog

Extract and export structured metadata from all installed skills as JSON/CSV.

## Description

Skill Catalog scans `~/.claude/skills/` to produce a complete inventory of installed skills with their metadata, tool requirements, and trigger patterns — exportable as JSON, CSV, or terminal table.

## Features

- Scans all SKILL.md files and extracts structured metadata
- Outputs JSON, CSV, or formatted terminal table
- Reports version, tools, argument hints, and descriptions
- Identifies skills missing required fields
- Feeds into `skill-graph` for relationship mapping
- Delegates scanning to `explorer` agent for efficiency

## Usage

Invoke by asking Claude Code with trigger phrases such as:

- "list all skills"
- "skill catalog"
- "skill inventory"
- "show skill overview"
- "skill 清單"
- "列出所有 skill"

## Related Skills

- [`skill-graph`](https://github.com/joneshong-skills/skill-graph)
- [`skill-curator`](https://github.com/joneshong-skills/skill-curator)
- [`skill-lifecycle`](https://github.com/joneshong-skills/skill-lifecycle)

## Install

Copy the skill directory into your Claude Code skills folder:

```
cp -r skill-catalog ~/.claude/skills/
```

Skills placed in `~/.claude/skills/` are auto-discovered by Claude Code. No additional registration is needed.
