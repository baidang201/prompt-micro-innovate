# 微创新 prompt 输出模板

> 把微创新后的 prompt 落到 outputs/YYYY-MM-DD/prompt.md 时用这个模板。

```markdown
---
date: {{DATE}}
seq: {{SEQ}}
original_id: {{ORIGINAL_ID}}
original_source: {{ORIGINAL_SOURCE}}
original_title: {{ORIGINAL_TITLE}}
skill: prompt-micro-innovate
skill_version: v0.1
mode: {{MODE}}  # normal | degraded
---

# 当日选中提示词（微创新版）

## 原始 prompt（已冻结，仅供参考）

```
{{ORIGINAL_PROMPT}}
```

## 微创新 prompt（最终交付）

```
{{NEW_PROMPT}}
```

## 改动记录（来自 prompt-micro-innovate skill）

### Step 1 · 识别核心钩子
{{CORE_HOOKS}}

### Step 2 · 应用变换（SCAMPER-LP）
| 维度 | 变换前 | 变换后 |
|---|---|---|
{{TRANSFORMS_TABLE}}

### Step 3 · 护城河细节
- 感官细节：{{SENSORY_DETAILS}}
- 节奏细节：{{RHYTHM_DETAILS}}
- 文化细节：{{CULTURAL_DETAILS}}

### Step 4 · 留白钩子
{{OPEN_HOOK}}

## 三问铁律自检

| # | 问题 | 结果 |
|---|---|---|
| ① | 原作核心钩子还在吗？ | {{Q1}} |
| ② | 新 prompt 给创作者/观众更多决策空间了吗？ | {{Q2}} |
| ③ | 情感共鸣能跨过原版的"半衰期"吗？ | {{Q3}} |

## 相似度自检

- 与原始 prompt：**{{SIM_TO_REF}}%**（阈值 70%）
- 与历史所有 prompt：**{{SIM_TO_HIST}}%**（阈值 70%）
- 撞避坑清单：{{AVOID_HITS}}

## skill 调用记录

- 迭代次数：{{ITERATIONS}}
- 自检结果：{{PASSED}}
- notes：{{NOTES}}
```

## 字段填写说明

| 字段 | 说明 |
|---|---|
| `CORE_HOOKS` | 从 6 类钩子中识别的 1-2 个，例如 `["未完成承诺+反向诉求", "底层反差"]` |
| `TRANSFORMS_TABLE` | Step 2 选中的变换，每行一条，例如 `\| Substitute \| 关爱流浪狗 \| 求领养流浪猫 \|` |
| `SENSORY_DETAILS` | 列出命中的感官细节词，如 `["指甲缝泥巴", "猫毛油墨"]` |
| `RHYTHM_DETAILS` | 列出节奏控制词，如 `["长镜头推近", "镜头从远景缓缓推到中近景"]` |
| `CULTURAL_DETAILS` | 列出文化符号词，如 `["上海老弄堂", "退休教师讲台"]` |
| `OPEN_HOOK` | 留白钩子的描述，如 `["未解悬念：领养人会来吗？", "可截图金句：给它一个家，也给自己一个伴"]` |
| `Q1/Q2/Q3` | `✅` 或 `❌` |
| `MODE` | `normal` = skill + 历史数据都齐全；`degraded` = 任一缺失 |
