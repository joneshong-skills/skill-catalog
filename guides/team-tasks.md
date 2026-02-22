# Team Tasks 說明書

## 一句話介紹

多 Agent 任務協調中心 — 支援 Claude Code 內建 Agent Teams、自訂 Pipeline、和辯論模式三種引擎。

## 什麼時候該用？

- 需要多個 Agent **即時討論、互相挑戰、自主協調**（Native Agent Teams）
- 需要**持久化任務紀錄**、跨 session 追蹤進度（Custom Pipeline）
- 需要**多方辯論 → 交叉審查 → 綜合結論**（Debate 模式）
- 想**手動精確控制**每一步的派發和依賴關係
- 大型專案需要 DAG 依賴圖管理平行任務

## 什麼時候不該用？（用其他 Skill 更好）

| 需求 | 更適合的 Skill | 原因 |
|------|---------------|------|
| 想丟一句話全自動搞定 | maestro | Maestro 自動分析 + 路由 + 執行 |
| 簡單任務不需要多 Agent | 直接用對應 CLI skill | 殺雞不用牛刀 |
| 只需要跨 CLI 比較輸出 | maestro（Race 模式） | Maestro 自動化比較流程 |

## 三種引擎

### Engine A — Native Agent Teams（即時協作）

Claude Code 內建的實驗性功能，啟用後可以：

- 建立多個 **Teammate**（獨立 Claude Code 實例）
- Teammates 透過**信箱**互相直接通訊
- 共享**任務清單**，支援依賴追蹤
- **自動認領**任務，完成後自動拿下一個

| 特點 | 說明 |
|------|------|
| 溝通方式 | Teammates 互相直接通訊 |
| 持久化 | Session 結束即消失 |
| CLI 限制 | 僅 Claude Code |
| Token 成本 | 較高（每 teammate 獨立實例） |
| 適合 | 研究、辯論、並行開發 |

**啟用方式**：`settings.json` 中設定 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

### Engine B — Custom Pipeline（持久化管理）

透過 `task_manager.py` 管理任務，支援三種模式：

#### Linear（依序執行）
適用：Bug 修復、逐步驗證、固定流程
```
code-agent → test-agent → docs-agent
```

#### DAG（依賴圖平行執行）
適用：大型功能、多模組並行、複雜依賴鏈
```
         ┌→ backend ─┐
design ──┤            ├→ e2e-test
         └→ frontend ─┘
```

#### Debate（多方辯論）
適用：架構決策、Code Review、技術選型
```
多方提出觀點 → 交叉審查 → 綜合結論
```

| 特點 | 說明 |
|------|------|
| 溝通方式 | 透過 JSON 檔間接傳遞 |
| 持久化 | JSON 檔永久保存 |
| CLI 支援 | Claude + Gemini + Codex（headless 或 interactive） |
| Token 成本 | 較低（headless）或中等（interactive） |
| 適合 | CI/CD pipeline、跨 session 追蹤 |

### Engine C — Hybrid（結合兩者）

用 Custom Pipeline 規劃任務結構 + 用 Agent Teams 實際執行，兼具持久化和即時協作。

## 快速範例

```bash
TM="python3 ~/.claude/skills/team-tasks/scripts/task_manager.py"

# DAG 模式
"$TM" init my-feature --mode dag -g "建立使用者系統"
"$TM" add my-feature design -a planner --desc "設計 API 規格"
"$TM" add my-feature backend -a coder --deps "design" --desc "實作後端"
"$TM" add my-feature frontend -a ui --deps "design" --desc "實作前端"
"$TM" ready my-feature  # 查看可派發任務

# Debate 模式
"$TM" init arch-review --mode debate -g "微服務 vs 單體架構？"
"$TM" add-debater arch-review security -p "資安角度"
"$TM" add-debater arch-review perf -p "效能角度"
"$TM" round arch-review start
```

## 與 maestro 的關係

| | team-tasks | maestro |
|---|---|---|
| **角色** | 工具箱（提供各種協調工具） | 建築師（自動決定用什麼工具） |
| **智能程度** | 手動 / 半自動 | 全自動 |
| **獨有功能** | Agent Teams、Debate、DAG | 自動 CLI 路由、Race、Escalation |
| **底層關係** | 獨立運作 | Maestro 內部使用 team-tasks |

**結論**：日常任務用 `/maestro`；需要 Agent Teams 即時協作、Debate 辯論、或手動精確控制時用 `/team-tasks`。

## 常見搭配

- **maestro** → Maestro 內部自動使用 team-tasks 管理任務
- **claude-code-headless / codex-cli-headless / gemini-cli-headless** → Pipeline 中派發任務給不同 CLI
- **claude-code-interactive / codex-cli-interactive / gemini-cli-interactive** → 多輪對話任務
