# Changelog

## v0.4.1 — 2026-08-16

### 修复（Fix）
- **R22 fallback 兑现**：之前传 `new_prompts=[]` 时 skill 只返回空结构，不告诉调用方"为什么空"。现在返回 `{fallback_triggered: True, fallback_reason: "...", guidance: [4 条]}`，让调用方知道进入 Profile §6.1 兜底 review。
- **R21 钩子动词假阳性**：之前 `check_r21_hook_diversity` 在抓 `c[-15:]` 尾巴时，会把候选尾部固定的参数尾巴（"9:16 竖屏"、"4K 高清"、"60 秒以内" 等）误识别为钩子动词，导致 `unique_count` 虚高。现在在抓尾巴前用 6 个正则 strip 这些参数噪音。

### 不变（No change）
- 21 项硬指标逻辑、阈值、`micro_innovate_v04` 主流程均不变
- SKILL.md / rules.md 内容不变
- 端到端 3 样本实测行为：自检仍然能抓到 R15/R17/R18/R19 等问题

### 验证
3 样本实测（`python3 tests/e2e_runner.py`）：
- sample-1 早餐店夫妻：5 候选全部触发 v03 + R17 + R19，R21 hooks 干净（"早起赶路的人有口热的」"等真实台词钩子）
- sample-2 周末爬山：`fallback_triggered=True` + reason + 4 条 guidance 完整输出
- sample-3 嫁衣：候选 3「70岁 - 1958年 = -1888岁」R18 边界验证生效

## v0.4.0 — 2026-08-16

### 新增（Add）
- **R2 修订**：核心台词 ≤1 复用（避免抄原片）
- **R16**：前 3 秒钩子必须含具体动作 / 物件 / 数字
- **R17**：候选长度 ≤80 字
- **R18**：逻辑自洽（年龄/年代倒推 ≥8 岁）
- **R19**：受众钩子词分层（women_18_40 / general）
- **R20**：避雷硬规则（不写"蒸汽朦胧镜头"等模板套话）
- **R15/R21 跨候选**：5 候选 ≥3 种骨架 / ≥3 种钩子动词
- **R22 fallback**：new_prompts=[] 时主动告知兜底
- **整合函数** `micro_innovate_v04(reference, new_prompts, audience)`

## v0.3.0 — 2026-08-07

### 新增（Add）
- `references/rules.md`：14 条硬规则 + 7 条反模式
- SKILL.md 加 v0.3 章节

## v0.2.0 — 2026-08-07

### 新增（Add）
- 芦苇编剧维度（戏根 / 困境-突围 / 小人物大历史 / 只能他说）
- 自检升级到 6 问（3 问铁律 + 3 芦苇检）
- 扩展 `SENSORY_PATTERNS` / `CULTURAL_PATTERNS` / `XI_GEN_PATTERNS` 模式库

## v0.1.0 — 2026-08-07

### 新增（Add）
- 首版：基于 `game-methodology M00` + `SCAMPER` + 三问铁律移植
