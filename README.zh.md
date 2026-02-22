[English](README.md) | [繁體中文](README.zh.md)

# skill-catalog

Extract and export structured metadata from all installed skills as JSON/CSV.

## 說明

Skill Catalog scans `~/.claude/skills/` to produce a complete inventory of installed skills with their metadata, tool requirements, and trigger patterns — exportable as JSON, CSV, or terminal table.

## 功能特色

- Scans all SKILL.md files and extracts structured metadata
- Outputs JSON, CSV, or formatted terminal table
- Reports version, tools, argument hints, and descriptions
- Identifies skills missing required fields
- Feeds into `skill-graph` for relationship mapping
- Delegates scanning to `explorer` agent for efficiency

## 使用方式

透過以下觸發語句呼叫 Claude Code 來使用此技能：

- "list all skills"
- "skill catalog"
- "skill inventory"
- "show skill overview"
- "skill 清單"
- "列出所有 skill"

## 相關技能

- [`skill-graph`](https://github.com/joneshong-skills/skill-graph)
- [`skill-curator`](https://github.com/joneshong-skills/skill-curator)
- [`skill-lifecycle`](https://github.com/joneshong-skills/skill-lifecycle)

## 安裝

將技能目錄複製到 Claude Code 技能資料夾：

```
cp -r skill-catalog ~/.claude/skills/
```

放置在 `~/.claude/skills/` 的技能會被 Claude Code 自動發現，無需額外註冊。
