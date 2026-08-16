# prompt-micro-innovate

[![version](https://img.shields.io/badge/version-0.4.1-blue.svg)](manifest.json)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![python](https://img.shields.io/badge/python-3.9%2B-yellow.svg)]()

抖音 / 短视频 Prompt 微创新方法论 + 21 项自检工具。
把"已经被验证爆款"的视频生成 prompt 做差异化改写，避免平台判定为同质化抄袭。

---

## 它是什么

这是一个**抖音 / 短视频 Prompt 微创新 Agent**。
你给它一条"参考爆款"视频生成 prompt，它会：

1. 帮你按 SCAMPER-LP 五维（Substitute / Modify / Adapt / Combine / Put）启发式生成 5 个差异化候选
2. 跑 21 项硬指标自检（钩子 / 长度 / 逻辑 / 受众 / 骨架差异化 等），告诉你哪个候选真的能过审、哪个会撞模板
3. 候选空 / 候选过少时主动进入兜底 review，告诉你"为什么空 + 下一步怎么做"

---

## 它是什么（Agent 使用说明书）

### 【Agent 名称】
**prompt-micro-innovate**（v0.4.1）

### 它是什么
（一句话定位）

> 这是一个**抖音 / 短视频 Prompt 微创新 Agent**，把参考爆款 prompt 做差异化改写，并跑 21 项硬指标自检告诉你哪个候选能过审。

### 省了什么人工

| 维度 | 之前（手工） | 现在（Agent） | 量化 |
|---|---|---|---|
| 候选生成 | 自己从 0 写 5 个差异化变体，脑暴 1-2 小时 | SCAMPER-LP 五维启发式 30 秒出 5 候选 | **2 小时 → 30 秒** |
| 自检 | 写完凭直觉发，发布后才知道撞模板 | 写之前跑 21 项硬指标，未过审的当场打回 | **发布后返工 30 分钟 → 写之前拦截** |
| 失败兜底 | 自己复盘"为什么不像爆款" | 主动告诉你"为什么空 + 下一步做什么" | **复盘 15 分钟 → 即时反馈** |
| 撞模板复盘 | 发布后看数据，发现点赞低 | 写之前 R15/R21 跨候选对比，骨架撞了立刻打回 | **事后分析 → 事前拦截** |

### 用了什么工具

| 工具 | 负责什么 | 版本 |
|---|---|---|
| **Hermes Agent Platform** | 跑 Agent 的宿主平台；接收任务、调度 skill、回报结果 | Hermes 大模型 API |
| **Codex CLI** | 开发者迭代 skill 本身（修改 `references/rules.md`、调阈值） | 持续 |
| **innovate.py**（本仓库） | 21 项硬指标自检引擎（纯 Python，无外部依赖） | v0.4.1 |
| **飞书 CLI**（可选，v0.5） | 把候选 + 自检结果发到飞书群，让圈友投票 | 待接入 |
| **LLM API**（v0.5） | 候选生成从启发式升级到 LLM（保证 5 候选走 5 种骨架） | 待接入 |

### 输入

- **输入 1**（必填）：**参考爆款 prompt**（一段中文短视频生成 prompt，80-200 字，含主体 / 场景 / 镜头 / 台词）
  - 格式：纯文本 utf-8
  - 来源：你自己写的 / 抖音 / TikTok 抄录的 / 圈内分享的
- **输入 2**（可选）：**5 个差异化候选**（由 LLM 或你手工生成）
  - 格式：list[str]，每个候选 60-160 字
  - 来源：v0.4.x 用 SCAMPER-LP 启发式；v0.5 用 LLM
- **输入 3**（可选）：**目标受众**（默认 `women_18_40`）
  - 可选：`women_18_40` / `general` / `men_18_35`

### 如何触发

#### 方式 A：直接调用 Python（最快）

```python
import sys
sys.path.insert(0, "path/to/prompt-micro-innovate/scripts")
from innovate import micro_innovate_v04

reference = "帮我生成一个视频：南方小镇上，一家开在巷口的早餐店…"
candidates = ["候选1", "候选2", "候选3", "候选4", "候选5"]

result = micro_innovate_v04(reference, candidates, audience="women_18_40")
print(result["all_pass"])            # True / False
print(result["cross_candidate"])     # R15/R21 跨候选检查
print(result["per_candidate"][0])    # 每个候选的 21 项自检
```

#### 方式 B：在 Hermes Agent 里说（最常用）

> 「帮我把这条 prompt 做微创新：[粘你的参考 prompt]。我要 5 个差异化候选，每个 ≤80 字，给我过自检的结果。」

Hermes 会自动调用本 skill 的 `micro_innovate_v04`，把结果回传到飞书群。

#### 方式 C：跑完整 3 样本测试（验证 skill 本身）

```bash
cd path/to/prompt-micro-innovate
python3 tests/e2e_runner.py
```

### 输出示例

**真实跑出来的输出**（v0.4.1，sample-1 早餐店夫妻）：

```json
{
  "all_pass": false,
  "fallback_triggered": false,
  "cross_candidate": {
    "r15_skeleton_diversity": {"pass": false, "detail": "5 候选覆盖骨架：['坚守', '传承']（应 ≥3）"},
    "r21_hook_diversity": {"pass": true, "detail": "唯一数 3（应 ≥3）", "hooks": ["点赞鼓励", "(尾:早起赶路的人有口热的。」)", "(尾:得替他们把这口锅守住。」)"]}
  },
  "per_candidate": [
    {"all_pass": false, "v04": {"r17_length": {"pass": false, "detail": "长度 150 字（上限 80）"}, "r19_audience_hook": {"pass": false, "detail": "受众 'women_18_40' 钩子词匹配：无"}}}
  ]
}
```

**真实跑出来的输出**（v0.4.1，sample-2 周末爬山，故意残缺）：

```json
{
  "fallback_triggered": true,
  "fallback_reason": "new_prompts 为空，v0.4 自检无法跨候选对比；进入 Profile §6.1 兜底 review，要求调用方先按 SCAMPER-LP 生成 ≥3 个候选。",
  "guidance": [
    "1. 用 SCAMPER-LP 五维（Substitute / Modify / Adapt / Combine / Put）启发式或 LLM 生成候选",
    "2. 每个候选 MUST 走不同骨架（坚守 / 传承 / 反悔 / 对照 / 被发现）",
    "3. 每个候选 MUST 含受众钩子词（women_18_40：心疼 / 看哭了 / 忍不住 / 致敬 等）",
    "4. 每个候选长度 MUST ≤ 80 字"
  ]
}
```

### 成功运行截图

跑 `python3 tests/e2e_runner.py` 得到完整 3 样本 × 21 项自检结果：

```
======================================================================
【sample-1 早餐店夫妻（152 字）】
======================================================================
all_pass = False · fallback_field = False
跨候选: r15_skeleton_diversity=False · r21_hook_diversity=True (干净)
单候选:
  候选 1 (150 字) ❌ — v04.r17_length :: 长度 150 字（上限 80）
  候选 2 (146 字) ❌ — v04.r17_length :: 长度 146 字（上限 80）
  ...
======================================================================
【sample-2 周末爬山（79 字，故意残缺）】
======================================================================
fallback_field = True ✓  ← R22 已实现
======================================================================
【sample-3 彝族老奶奶 + 嫁衣（126 字）】
======================================================================
  候选 3 (111 字) ❌ — v04.r18_logic :: "70岁 - 1958年 = -1888岁，不合常理"  ← R18 边界验证生效
```

### 圈友怎么用

#### 第 1 步：拿到这个仓库

```bash
git clone https://github.com/baidang201/prompt-micro-innovate.git
cd prompt-micro-innovate
```

#### 第 2 步：放进你的 Codex / Hermes skills 目录

```bash
# Codex
ln -s "$(pwd)" ~/.codex/skills/prompt-micro-innovate

# 或 Hermes
cp -r "$(pwd)" ~/.hermes/skills/prompt-micro-innovate
```

#### 第 3 步：调用

```python
import sys
sys.path.insert(0, "scripts")
from innovate import micro_innovate_v04

# 你的参考爆款
ref = "你的参考 prompt"
# 5 个候选（先用启发式，v0.5 接 LLM 后会自动生成）
cands = ["c1", "c2", "c3", "c4", "c5"]

result = micro_innovate_v04(ref, cands)
print(result)
```

**最低门槛**：会 `import` 和调用 `micro_innovate_v04` 函数。

### 注意事项

#### 它做不了什么

- ❌ **不能直接生成视频**：它只做 prompt 改写 + 自检；视频生成要交给剪映 / 即梦 / 可灵
- ❌ **不能保证 100% 过审**：21 项自检是基于"经验规律的硬指标"，不是平台算法
- ❌ **不能替代人工审美**：自检通过 ≠ 视频会爆；最终还是要看数据

#### 什么时候需要人工介入

- 5 候选全失败：自己重写参考 prompt，补充"奠基动作"和"具体物件"
- R18 边界误报（如「70 岁讲 90 年前的故事」被判不合常理）：手动加注释或调整阈值
- 受众分层需要切换（如从 women_18_40 切到 men_18_35）：手动改 `audience` 参数

#### 已知问题和后续改进方向

- v0.4.x 候选生成用启发式，**5 候选可能走相同骨架**（如都走"坚守"）→ v0.5 接 LLM 强制 5 候选走 5 种不同骨架
- v03 失败报告未细分到 `luwei_checks.q5/q6` 子项 → 优先级 3，待修
- 静态参数尾巴正则有 SyntaxWarning（`\s` 在 raw string 中）→ 待清理

---

## 项目结构

```
prompt-micro-innovate-v0.4.1/
├── README.md                 ← 你正在读这个（Agent 使用说明书）
├── CHANGELOG.md              ← 版本变更记录
├── LICENSE                   ← MIT 许可证
├── manifest.json             ← skill 元数据（v0.4.1）
├── SKILL.md                  ← Codex/Hermes 调用的入口
├── references/
│   ├── rules.md              ← 22 条硬规则 + 7 条反模式
│   ├── transform-rules.md    ← SCAMPER 转换规则
│   └── case-prompt-examples.md ← 5 个实战案例
├── scripts/
│   └── innovate.py           ← 21 项自检引擎（v0.4.1）
├── templates/
│   └── micro-innovated-prompt.md ← 输出模板
├── tests/
│   ├── e2e_runner.py         ← 3 样本实测脚本
│   └── test-prompts/
│       ├── sample-1.txt      ← 早餐店夫妻（152 字）
│       ├── sample-2.txt      ← 周末爬山（79 字，故意残缺）
│       └── sample-3.txt      ← 彝族老奶奶嫁衣（126 字）
└── website/
    ├── index.html            ← 静态介绍网站
    └── style.css
```

## 版本

当前版本：**v0.4.1**（2026-08-16）

完整变更记录见 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT — 见 [LICENSE](LICENSE)。
