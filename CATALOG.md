# Skill Catalog

少爺自家 skill 集中目錄，由 `~/.claude/data/skill-registry/registry.json` 自動渲染。

## 更新方式

```bash
# 重建 registry（掃 ~/.claude/skills/ → 寫 registry.json）
~/.local/bin/python3 ~/.claude/skills/skill-publisher/scripts/bootstrap_registry.py

# 重渲染 catalog 表格（讀 registry.json → 替換 marker 之間區塊）
~/.local/bin/python3 ~/.claude/skills/skill-publisher/scripts/render_catalog.py
```

## Sync Status 語意

| Badge | 含義 |
|-------|------|
| ✅ published | 有 GitHub remote、無 unpushed commit |
| ⚠️ needs-update | 有 GitHub remote 但本地 commit 未 push |
| 📝 draft | 有 .git 但未設 upstream（本地分支） |
| 🔒 local-only | 無 .git，僅本機 |

---

<!-- catalog:start -->

_Auto-generated from registry.json — total 47 skills._

| Skill | Lifecycle | Sync | Tags | GitHub |
| --- | --- | --- | --- | --- |
| `_ref-review-criteria` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/_ref-review-criteria) |
| `_ref-workshop-patterns` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/_ref-workshop-patterns) |
| `_ref-writing-structure` | `active` | 🔒 local-only | — | — |
| `agent-hatchery` | `active` | 🔒 local-only | — | — |
| `anvil` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/anvil) |
| `blink-builder` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/blink-builder) |
| `blueprint` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/blueprint) |
| `brainstorming` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/brainstorming) |
| `cannibalize` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/cannibalize) |
| `cli-headless` | `active` | 🔒 local-only | — | — |
| `content-writer` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/content-writer) |
| `create-skill` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/create-skill) |
| `diagram-gen` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/diagram-gen) |
| `divergent-thinking` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/divergent-thinking) |
| `docvault` | `active` | 📝 draft | — | [link](https://github.com/joneshong-skills/docvault) |
| `forge` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/forge) |
| `frontend-design` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/frontend-design) |
| `git-worktrees` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/git-worktrees) |
| `image-prompt` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/image-prompt) |
| `intelflow` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/intelflow) |
| `macos-ui-automation` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/macos-ui-automation) |
| `maestro` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/maestro) |
| `memvault` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/memvault) |
| `message-polish` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/message-polish) |
| `model-mentor` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/model-mentor) |
| `ocr` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/ocr) |
| `pencil-design` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/pencil-design) |
| `playground` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/playground) |
| `prompt-router` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/prompt-router) |
| `sandbox-patterns` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/sandbox-patterns) |
| `session-channel` | `active` | 🔒 local-only | — | — |
| `skill-catalog` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-catalog) |
| `skill-curator` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/skill-curator) |
| `skill-graph` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/skill-graph) |
| `skill-lifecycle` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/skill-lifecycle) |
| `skill-optimizer` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/skill-optimizer) |
| `skill-publisher` | `active` | 📝 draft | — | [link](https://github.com/joneshong-skills/skill-publisher) |
| `skill-tester` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-tester) |
| `smart-search` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/smart-search) |
| `sync-config` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/sync-config) |
| `systematic-debugging` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/systematic-debugging) |
| `team-tasks` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/team-tasks) |
| `tmux-expert` | `active` | 📝 draft | — | [link](https://github.com/joneshong-skills/tmux-expert) |
| `tmux-relay` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/tmux-relay) |
| `verification-before-completion` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/verification-before-completion) |
| `web-video-tutorial` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/web-video-tutorial) |
| `webcrawl` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/webcrawl) |

<!-- catalog:end -->
