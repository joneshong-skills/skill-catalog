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

_Auto-generated from registry.json — total 130 skills._

| Skill | Lifecycle | Sync | Tags | GitHub |
| --- | --- | --- | --- | --- |
| `_ref-review-criteria` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/_ref-review-criteria) |
| `_ref-workshop-patterns` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/_ref-workshop-patterns) |
| `_ref-writing-structure` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-_ref-writing-structure) |
| `agent-hatchery` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-agent-hatchery) |
| `agentctl` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-agentctl) |
| `anvil` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/anvil) |
| `blink-builder` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/blink-builder) |
| `blog-writer` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/blog-writer) |
| `blueprint` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/blueprint) |
| `brainstorming` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/brainstorming) |
| `brand-guidelines` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/brand-guidelines) |
| `cannibalize` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/cannibalize) |
| `canvas-design` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/canvas-design) |
| `capture` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/capture) |
| `changelog-gen` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/changelog-gen) |
| `cli-headless` | `active` | ✅ published | — | [link](https://github.com/JonesHong/claude-skill-cli-headless) |
| `code-diet` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/code-diet) |
| `code-review-interceptor` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/code-review-interceptor) |
| `codebase-design` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-codebase-design) |
| `company-intel` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/company-intel) |
| `competitive-intel` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/competitive-intel) |
| `computer-use` | `active` | 🔒 local-only | — | — |
| `content-writer` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/content-writer) |
| `context-diet` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/context-diet) |
| `create-agent` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/create-agent) |
| `create-command` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/create-command) |
| `create-skill` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/create-skill) |
| `diagram-gen` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/diagram-gen) |
| `divergent-thinking` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/divergent-thinking) |
| `doc-coauthoring` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/doc-coauthoring) |
| `docs-butler` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/docs-butler) |
| `docvault` | `active` | 📝 draft | — | [link](https://github.com/joneshong-skills/docvault) |
| `docx` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/docx) |
| `domain-modeling` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-domain-modeling) |
| `envkit` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/envkit) |
| `executor` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/executor) |
| `explain-visual` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/explain-visual) |
| `fetch-from-air` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-fetch-from-air) |
| `finance` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/finance) |
| `fleet` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/fleet) |
| `forge` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/forge) |
| `frontend-design` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/frontend-design) |
| `git-worktrees` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/git-worktrees) |
| `github-pm` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/github-pm) |
| `goal-prompt` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-goal-prompt) |
| `grill-me` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-grill-me) |
| `grilling` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-grilling) |
| `humanizer` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/humanizer) |
| `image-edit` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/image-edit) |
| `image-gen` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/image-gen) |
| `image-prompt` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/image-prompt) |
| `incident-to-guard` | `active` | 📝 draft | — | — |
| `intelflow` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/intelflow) |
| `iterative-optimize` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/iterative-optimize) |
| `macos-ui-automation` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/macos-ui-automation) |
| `maestro` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/maestro) |
| `marketing-copy` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/marketing-copy) |
| `mcp-builder` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/mcp-builder) |
| `meeting-insights` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/meeting-insights) |
| `meetingroom` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-meetingroom) |
| `memvault` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/memvault) |
| `message-polish` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/message-polish) |
| `mjs-prompt` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-mjs-prompt) |
| `model-mentor` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/model-mentor) |
| `notebookllm` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/notebookllm) |
| `notebookllm-visual` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/notebookllm-visual) |
| `ocr` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/ocr) |
| `ocr-claude-api` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/ocr-claude-api) |
| `openclaw-mentor` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/openclaw-mentor) |
| `orca-cli` | `active` | 🔒 local-only | — | — |
| `orchestration` | `active` | 🔒 local-only | — | — |
| `over-engineering-audit` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-over-engineering-audit) |
| `paper-research` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/paper-research) |
| `pdf` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/pdf) |
| `pencil-design` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/pencil-design) |
| `person-intel` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/person-intel) |
| `photo-edit` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-photo-edit) |
| `plain-speak` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/plain-speak) |
| `playground` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/playground) |
| `pptx` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/pptx) |
| `projectagent` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-projectagent) |
| `prompt-router` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/prompt-router) |
| `quote-builder` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/quote-builder) |
| `quote-consultant` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/quote-consultant) |
| `readme-gen` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/readme-gen) |
| `repo-map` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-repo-map) |
| `sandbox-patterns` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/sandbox-patterns) |
| `sentinel` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/sentinel) |
| `seo-audit` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/seo-audit) |
| `session-channel` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-session-channel) |
| `session-intelligence` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/session-intelligence) |
| `session-redactor` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/session-redactor) |
| `skill-catalog` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-catalog) |
| `skill-curator` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-curator) |
| `skill-evolver` | `active` | 📝 draft | — | [link](https://github.com/joneshong-skills/skill-evolver) |
| `skill-graph` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-graph) |
| `skill-lifecycle` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-lifecycle) |
| `skill-optimizer` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-optimizer) |
| `skill-proxy` | `active` | ✅ published | meta, proxy, skill-discovery | [link](https://github.com/joneshong-skills/skill-proxy) |
| `skill-publisher` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-publisher) |
| `skill-security-scan` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-security-scan) |
| `skill-tester` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/skill-tester) |
| `smart-search` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/smart-search) |
| `social-content` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/social-content) |
| `social-media-dl` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/social-media-dl) |
| `spec-kit` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/spec-kit) |
| `stt` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/stt) |
| `sync-config` | `active` | ⚠️ needs-update | — | [link](https://github.com/joneshong-skills/sync-config) |
| `synergy-weaver` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/synergy-weaver) |
| `system-map` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/system-map) |
| `system-monitor` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/system-monitor) |
| `systematic-debugging` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/systematic-debugging) |
| `tdd` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/tdd) |
| `team-tasks` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/team-tasks) |
| `theme-factory` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/theme-factory) |
| `tmux-expert` | `active` | 📝 draft | — | [link](https://github.com/joneshong-skills/tmux-expert) |
| `tmux-relay` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/tmux-relay) |
| `tts` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/tts) |
| `ui-audit` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/ui-audit) |
| `verification-before-completion` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/verification-before-completion) |
| `vhs-demo-gif` | `active` | 📝 draft | — | — |
| `video-audio` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/video-audio) |
| `video-core` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/video-core) |
| `video-edit` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/video-edit) |
| `video-mix` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/video-mix) |
| `web-video-tutorial` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/web-video-tutorial) |
| `webcrawl` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/webcrawl) |
| `workflow-prompt` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-workflow-prompt) |
| `writing-great-skills` | `active` | ✅ published | — | [link](https://github.com/JonesHong/cc-skill-writing-great-skills) |
| `xlsx` | `active` | ✅ published | — | [link](https://github.com/joneshong-skills/xlsx) |

<!-- catalog:end -->

---

## Flow Map — 敘事路由（手寫區，marker 之外）

蠶食自 mattpocock `ask-matt` router 手法：關鍵字索引抓不到「兩個 skill 看起來很像、但差在 X」的語用區辨，這一區用**敘事**補上。**維護鐵律：新增 / 改名 / 改行為任何下列 skill 時,回來同步這張圖——a stale router is a router that lies。**

### Main flows（主工作流，含分支決策）

**1. 設計紀律（idea → build）**

1. `grill-me` — 動工前把「你要什麼」拷問到共識（AI 只問不決，底層引擎是 `grilling`）
2. 分支 — 術語開始定形？→ `domain-modeling`（CONTEXT.md glossary + ADR 紀律）
3. 分支 — 要決定模組介面/seam？→ `codebase-design`（deep module 詞彙）
4. 動工 — 交回下方 Main flow 6（開發實作與驗收）

Because：
- `grill-me` vs `blueprint`：grill 磨「你要什麼」（AI 只問不決）；blueprint 是已知要什麼之後展開執行計劃。先 grill 後 blueprint。
- `domain-modeling` vs `memvault`：前者管專案的 ubiquitous language 紀律；後者管跨 session 記憶。詞彙歸前者，教訓歸後者。
- `codebase-design` vs coding-discipline §1 The Ladder：Ladder 問「該不該存在」（YAGNI），codebase-design 問「存在的話介面多深」，兩軸正交。

**2. 內容產出（idea → 稿 → 潤 → 發布）**

`brainstorming` 收斂出可行方案 → `content-writer`（研究型長文帶引用）/ `marketing-copy`（廣告文案）/ `social-content`（社群貼文）→ `blog-writer`（比 content-writer 多做「發布」這一步）→ `message-polish`（單則訊息潤飾，非長文草稿）。

Because：`brainstorming` vs `divergent-thinking`：前者收斂到可行方案，後者刻意跳脫既有專案脈絡找靈感——先問「這次要收斂還是要跳脫」。

**3. 需求整形（模糊 → 可執行）**

`prompt-router`（承接一句話亂需求，判斷路由）→ `goal-prompt`（磨成明確 goal）→ `workflow-prompt`（磨成多步驟 workflow）→ `mjs-prompt`（落成可執行 agentctl workflow 檔）。四者是同一條加工鏈，差在加工深度，不是互斥選項。

**4. Skill 工廠（meta 治理：造 → 驗 → 優化 → 發布 → 進化）**

`create-skill`（造）→ `skill-tester` / `skill-security-scan` / `anvil`（驗：功能是否如預期／有無 prompt injection／遙測+結構品質評分，三線並行）→ `skill-optimizer` / `skill-curator` / `skill-lifecycle` / `skill-evolver`（優化，見下 because）→ `skill-publisher`（發布）。旁支：`skill-graph`（看協作關係）、`skill-catalog`（本文件的產出者）、`skill-proxy`（BM25 冷 skill 索引兜底）、`cannibalize`（從外部 repo 吸收新 pattern，是造的上游）、`synergy-weaver`（串接組合既有 skill）。同家不同造物：`create-agent`（造 agent）、`create-command`（造 slash command）、`mcp-builder`（造 MCP server）。

Because（優化四兄弟最易混）：
- `skill-optimizer` — 針對「這一個」skill 依回饋改
- `skill-curator` — 找「多個」skill 該不該合併/收斂
- `skill-lifecycle` — 排程週期性整體維護（active/archived/draft 狀態機）
- `skill-evolver` — 每晚自動、無人值守跑優化迭代

Vocabulary underneath：`writing-great-skills`（怎麼寫好 skill 的共用詞彙，Predictability 四軸）是本家所有 skill 的設計基準。

**5. 研究情報（找 → 讀 → 存 → 出報告）**

`smart-search`（一般搜尋）/ `webcrawl`（專門爬單一網頁轉 markdown）→ `company-intel` / `competitive-intel` / `person-intel` / `paper-research`（深挖特定對象：公司/競品/個人/論文）→ `docvault`（上傳文件庫供問答）/ `projectagent`（三源 RAG 查專案共識）/ `notebookllm`（上傳 NotebookLM）/ `notebookllm-visual`（NotebookLM 衍生視覺化簡報）→ `intelflow`（彙整成情報簡報）。旁支：`meetingroom`（即時開會記錄+問答，當下錄）vs `meeting-insights`（分析已有逐字稿，事後看）。

Because：`memvault` vs `docvault` / `projectagent`：memvault 記的是跨 session 個人/專案教訓與事實，docvault 是上傳文件庫問答，projectagent 是查專案決策共識——三者存的東西分層不同，不是同一個記憶庫的三個入口。

**6. 開發實作與驗收（blueprint → 動工 → debug → verify）**

`forge`（idea to shipped 全流程，內部串 `brainstorming` → `spec-kit` → `blueprint` → `executor` → `verification-before-completion`）；單獨叫則各自成立：`blueprint`（規劃）→ `executor`（照藍圖執行）→ `verification-before-completion`（完成前確認）。除錯支線：`systematic-debugging` / `tdd` / `code-review-interceptor`（邊寫邊審，非事後審）。瘦身支線：`over-engineering-audit`（找可刪的過度設計）vs `code-diet`（找重複/死碼，抓的目標不同）。隔離工具：`git-worktrees`。收尾優化：`iterative-optimize`（驗證通過後跑量化改善迴圈）。

### On-ramps（產生工作的起點情境）

- 動工前想先問清楚要什麼 → `grill-me`
- 一句話亂需求丟過來 → `prompt-router`
- 現有 skill 都兜不起來 → `skill-proxy`（差在：prompt-router 處理「意圖不清」，skill-proxy 處理「意圖清楚但找不到 loaded skill」）
- 沒靈感 vs 想跳脫現有框架 → `brainstorming` vs `divergent-thinking`
- 不知道用哪個模型/CLI → `model-mentor`；不確定 openclaw 怎麼用 → `openclaw-mentor`
- 想要從頭做到尾一次做完 → `forge`
- 覺得程式碼太複雜/太肥 → `over-engineering-audit` vs `code-diet`
- 要找其他 pane/agent 在幹嘛 → `session-channel`（看誰活著）vs `tmux-relay`（實際派工過去）
- 剛做完想確認有沒有真的做完 → `verification-before-completion`

### Standalone（獨立工具，無需嵌進更大工作流）

**視覺與前端設計**：`frontend-design` / `pencil-design` / `canvas-design` / `brand-guidelines` / `theme-factory` / `diagram-gen` / `explain-visual` / `playground` / `ui-audit` / `seo-audit` / `agent-hatchery`。生圖三兄弟：`image-prompt`（只寫 prompt 給其他工具用）vs `image-gen`（直接產圖）vs `image-edit`（改既有圖，如馬賽克/模糊）；另有 `photo-edit`（調色調光，非生成）、`plain-speak`（術語轉白話）。

**媒體處理**：影像 `video-core` / `video-edit` / `video-mix` / `video-audio` / `web-video-tutorial` / `social-media-dl`；語音 `stt` / `tts`；文字辨識 `ocr`（本地精確定位座標）vs `ocr-claude-api`（走 Claude API 批量辨識）。

**多 Agent 派工與環境**：`maestro`（多 CLI 競速比較）/ `team-tasks`（同一 CLI 內多 agent 協調）/ `agentctl`（goal-driven 單一 loop 跑到測試全綠）/ `fleet`（派工到遠端 win-gpu）/ `tmux-relay`（跨 pane 轉發）/ `tmux-expert`（tmux 本身的控制與 UI）/ `session-channel`（看其他 pane 活著沒）/ `cli-headless`（任一 CLI 的非互動模式）。

**系統運維與文件治理**：服務健康三兄弟 `sentinel`（事件/健康檢查）vs `system-monitor`（磁碟/服務即時狀態）vs `system-map`（拓撲/端口清單文件）；環境 `envkit` / `sync-config`；追蹤 `github-pm`；個人記錄 `capture` / `finance`；session 治理 `session-intelligence`（統計週報）/ `session-redactor`（清敏感資料）。文件產出四兄弟：`readme-gen`（專案說明）vs `changelog-gen`（release notes）vs `repo-map`（給 agent 看的導航地圖）vs `docs-butler`（稽核既有文件是否漂移，不產新文件）；另有 `context-diet`（rules/context 瘦身）。

**瀏覽器／macOS 自動化**：`macos-ui-automation`（原生對話框）/ `blink-builder`（Blink Shell 建置）/ `fetch-from-air`（跨機拉檔）。

**文件輸出**：`pdf` / `docx` / `pptx` / `xlsx`；商務文件 `quote-builder`（排版報價文件）vs `quote-consultant`（估算報價金額本身）；`doc-coauthoring`（多人協作草稿）。

### Vocabulary underneath（底層共用詞彙 skill）

- `_ref-review-criteria` — code review 標準與結構化輸出 schema
- `_ref-workshop-patterns` — workshop 後端程式慣例
- `_ref-writing-structure` — 繁中句構約束（抗 AI 味）
- `grilling` — `grill-me` 的底層引擎（model-invoked primitive，一次一題＋推薦答案）
- `writing-great-skills` — 怎麼寫好 skill 的共用詞彙，Skill 工廠家族的設計基準
- `sandbox-patterns` — sandbox_execute 使用慣例，被多個 skill（含 `skill-catalog` 自身）引用

---

涵蓋 124 個 skill（含 3 個 `_ref-*` reference）／分 13 群（6 主工作流 + 6 獨立工具家 + 1 底層詞彙區）。

