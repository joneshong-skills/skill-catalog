# Maestro 說明書

## 一句話介紹

智能指揮官 — 自動分析任務、選擇最佳 CLI 工具、選擇執行模式，一句話搞定多 Agent 協作。

## 什麼時候該用？

- 想丟一句話讓系統**全自動**分析 → 路由 → 執行
- 需要**跨 CLI 協作**（Claude Code + Codex CLI + Antigravity CLI）
- 大型任務需要拆分成多個子任務平行處理
- 想比較不同 CLI 對同一任務的輸出品質（Race 模式）
- 想用最省 token 的方式完成任務（Escalation 模式）

## 什麼時候不該用？（用其他 Skill 更好）

| 需求 | 更適合的 Skill | 原因 |
|------|---------------|------|
| 需要多個 Agent 即時討論、互相挑戰 | team-tasks（Native Agent Teams） | Maestro 走 headless/interactive 派發，不啟動 Agent Teams |
| 需要多方辯論 → 交叉審查 → 綜合結論 | team-tasks（Debate 模式） | Maestro 的 5 種 pattern 沒有 debate |
| 想手動精確控制每一步的派發和依賴 | team-tasks（Custom Pipeline） | Maestro 是全自動的，插手空間有限 |
| 單一 CLI 就能完成的簡單任務 | 直接用對應的 headless/interactive skill | 不需要 Maestro 的自動路由層 |

## 五種執行模式（Pattern）

| Pattern | Agent 數量 | 適用場景 |
|---------|-----------|---------|
| **Solo** | 1 | 簡單、明確、單一範圍的任務（預設，涵蓋 70% 場景） |
| **Pipeline** | 2-5 依序 | 多階段工作（規劃 → 實作 → 審查） |
| **Race** | 2-3 平行 | 品質至上，比較多個 CLI 的輸出 |
| **Swarm** | 3+ 平行 | 大型可拆分任務，獨立子任務同時執行 |
| **Escalation** | 1→升級 | 預算優先，從便宜開始，品質不夠再升級 |

## CLI 路由表

Maestro 根據任務類型自動選擇最適合的 CLI：

| 任務類型 | 主要 CLI | 省錢 CLI | 最強 CLI |
|---------|---------|---------|---------|
| 程式碼生成 | Claude Code | Antigravity CLI | Claude Code |
| Code Review | Claude Code | Codex CLI | Claude Code |
| 除錯 | Claude Code | Antigravity CLI | Claude Code |
| 重構 | Codex CLI | Codex CLI | Claude Code |
| 架構設計 | Claude Code | Claude Code | Claude Code |
| 測試 | Codex CLI | Codex CLI | Claude Code |
| 長文分析 | Antigravity CLI | Antigravity CLI | Antigravity CLI |
| 前端 | Claude Code | Antigravity CLI | Claude Code |
| 後端 | Codex CLI | Codex CLI | Claude Code |
| 研究 | Antigravity CLI | Antigravity CLI | Antigravity CLI |

## 快速範例

```bash
MAESTRO="python3 ~/.claude/skills/maestro/scripts/maestro.py"

# 最常用：自動分析並派發
$MAESTRO run "Fix the login bug in auth.ts" --cwd /path/to/project

# 指定模式
$MAESTRO run --pattern pipeline "Build user registration" --cwd /path/to/project

# 只看計畫不執行
$MAESTRO plan "Refactor the entire payments module"

# 查看狀態和報告
$MAESTRO status maestro-20260211-143022
$MAESTRO report maestro-20260211-143022
```

## 與 team-tasks 的關係

| | Maestro | team-tasks |
|---|---|---|
| **角色** | 建築師（決定用什麼工具、怎麼蓋） | 工具箱（鐵鎚、鋸子） |
| **智能程度** | 全自動（分析 → 路由 → 執行） | 手動 / 半自動 |
| **CLI 選擇** | 自動根據任務類型 + 預算選擇 | 你自己決定 |
| **底層依賴** | 內部使用 team-tasks 做任務管理 | 獨立運作 |

**結論**：日常任務只叫 `/maestro`；需要 Agent Teams 即時協作或 Debate 時才叫 `/team-tasks`。

## 常見搭配

- **spec-kit** → 先寫規格，再用 Maestro 派發實作
- **team-tasks** → Maestro 內部已自動使用，通常不需手動搭配
- **model-mentor** → Maestro 內建路由表已整合 model-mentor 的 CLI 比較數據
