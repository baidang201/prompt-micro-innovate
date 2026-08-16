"""
prompt-micro-innovate skill v0.2 · 参考实现

新增：
- luwei check（戏根/困境突围/只能他说）
- InnovateResult 现在带 6 项自检（3 问铁律 + 3 芦苇检）
"""
from __future__ import annotations
import re
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict


# ---------- 6 类核心钩子识别 ----------
HOOK_PATTERNS = {
    "未完成承诺+反向诉求": ["鼓励", "点赞", "祝福", "加油", "给我", "能不能", "能否", "请"],
    "共情反差": ["但是", "其实", "却", "偏偏", "然而"],
    "见证时刻": ["最后一次", "终于", "终于圆", "终于完", "最后一", "退休", "毕业"],
    "底层逆袭": ["逆袭", "反击", "证明", "坚持", "不放弃"],
    "失去恐惧": ["害怕", "担心", "不要", "别", "即将", "再也"],
    "未解悬念": ["如果", "会不会", "还能", "还能"],
}

def identify_hooks(text: str) -> List[str]:
    hits = []
    for hook_name, keywords in HOOK_PATTERNS.items():
        if any(kw in text for kw in keywords):
            hits.append(hook_name)
    return hits[:2]


# ---------- 相似度（Jaccard 2-gram） ----------
def tokenize(text: str) -> set:
    text = re.sub(r"[，。！？、；：\s\n\d:]+", "", text)
    return set(text[i:i+2] for i in range(len(text)-1))

def jaccard(a: str, b: str) -> float:
    sa, sb = tokenize(a), tokenize(b)
    if not sa or not sb: return 0.0
    return round(len(sa & sb) / len(sa | sb) * 100, 2)


# ---------- 护城河细节密度（v0.2 扩展） ----------
SENSORY_PATTERNS = [
    # 视觉-痕迹
    "泥巴", "磨痕", "磨得", "掉漆", "泛黄", "发白", "起毛", "破损", "裂", "缝补", "补丁", "针脚",
    "油渍", "油墨", "猫毛", "煤渣", "落叶", "灰尘", "烟灰", "灰烬", "汗", "血迹", "泪", "眼红",
    # 视觉-色彩
    "昏黄", "暮色", "暖金色", "夕阳", "破晓", "暗红",
    # 触觉
    "粗糙", "光滑", "磨软", "磨硬", "硬邦邦", "软乎乎", "温温",
    # 听觉
    "嘶", "咔嚓", "鸣笛", "呼啸", "呢喃", "哽咽", "沙哑",
    # 嗅觉
    "煤球", "烟味", "汗味", "机油",
    # 微小物件
    "工牌", "纽扣", "拉链", "胶带", "手帕", "铁丝",
    "皴裂", "脱皮", "结痂", "皱裂", "粗糙", "凸起",
]
RHYTHM_PATTERNS = ["长镜头", "推近", "缓缓", "远景", "中近景", "特写", "慢放", "节奏", "节拍", "口型", "时长", "秒"]
# 文化细节：地域 / 年代 / 职业 / 民俗的具体符号
CULTURAL_PATTERNS = [
    # 地域
    "弄堂", "草原", "山区", "山村", "豫北", "陕北", "东北", "上海", "广州", "深圳", "成都", "新疆", "西藏",
    "黄浦江", "外滩", "天际线", "万国旗", "梧桐", "石库门",
    # 场所 / 场景
    "停机坪", "手术室", "茅草房", "窑洞", "毡帽", "羊毛毡", "大槐树", "狗窝", "鸡窝", "祠堂",
    "作坊", "教室", "操场", "站台", "车站", "早餐店", "面馆", "包子铺",
    "南极", "极地", "边疆", "孤岛", "海岛", "山区", "山村",
    # 职业 / 身份
    "讲台", "退役", "退伍", "工牌", "军人", "护士", "教师", "机长", "司机",
    "木雕", "文物", "传承", "手艺", "瓷器", "早餐", "列车", "科考", "辅导员", "支教",
    # 民俗 / 节令
    "大雪", "冰碴", "积雪", "霜降", "立冬", "薄雾", "破晓", "暮色",
]

def detail_density(text: str) -> Dict[str, int]:
    return {
        "sensory": sum(1 for p in SENSORY_PATTERNS if p in text),
        "rhythm": sum(1 for p in RHYTHM_PATTERNS if p in text),
        "cultural": sum(1 for p in CULTURAL_PATTERNS if p in text),
    }


# ---------- 三问铁律（v0.1） ----------
def three_questions(reference: str, new: str, core_hooks: List[str]) -> Dict[str, bool]:
    q1_pass = any(any(kw in new for kw in HOOK_PATTERNS.get(h, [])) for h in core_hooks) if core_hooks else True
    q2_pass = len(new) >= len(reference) * 0.9
    q3_pass = jaccard(reference, new) < 70
    return {
        "q1_hook_preserved": q1_pass,
        "q2_more_decisions": q2_pass,
        "q3_past_half_life": q3_pass,
    }


# ---------- 芦苇三检（v0.2 新增） ----------

# 戏根识别：原 prompt 中的核心人物关系 / 关键事件
# 用"动词+对象"模式识别（"领回来""收养""等待""退休"）
# 戏根动作模式（含单字版，覆盖"等""回""来"等口语动词）
XI_GEN_PATTERNS = [
    # 双向动作
    "领回来", "收养", "收留", "等待", "退休", "退役",
    "回来", "团圆", "送别", "重逢", "抢救", "送祝福", "加油", "鼓励", "点个赞",
    # 单字基础动词（覆盖口语化表达）
    "等", "回", "来", "守", "盼", "送", "找", "救", "帮", "守",
    "团聚", "归来", "相见", "送行", "告别", "回家",
]

def luwei_q4_gen_retained(reference: str, new: str) -> Dict[str, bool]:
    """戏根保留：原 prompt 中的"奠基性动作"在新 prompt 中至少出现 1 个等价动作"""
    found_in_ref = [p for p in XI_GEN_PATTERNS if p in reference]
    if not found_in_ref:
        return {"q4_xi_gen_retained": True, "detail": "原 prompt 无明显戏根，跳过"}
    retained = [p for p in found_in_ref if p in new or any(alt in new for alt in _get_alts(p))]
    return {
        "q4_xi_gen_retained": len(retained) > 0,
        "detail": f"原戏根动作 {found_in_ref}，新 prompt 保留 {retained or '无'}",
    }

def _get_alts(pattern: str) -> List[str]:
    """戏根动作的等价替换词（微创新时常被替换的词）"""
    return {
        "领回来": ["捡回来", "领养", "带回家"],
        "收养": ["领养", "带回家", "照顾"],
        "等待": ["等", "守候", "盼望"],
        "退休": ["最后一趟", "最后一次", "收官"],
        "回来": ["归来", "回家", "团聚"],
        "团圆": ["重逢", "团聚", "相见"],
        "送别": ["告别", "送行", "最后"],
        "重逢": ["相见", "团聚", "再见"],
        "抢救": ["救援", "救人", "救"],
        "送祝福": ["祝福", "鼓励", "加油"],
        "鼓励": ["祝福", "加油", "关注", "陪伴"],
        "点个赞": ["鼓励", "关注", "支持"],
    }.get(pattern, [])


# 困境—突围识别：必须既有"困境信号"也有"突围/动作信号"
DILEMMA_PATTERNS = ["求", "孤独", "无助", "可怜", "残", "病", "贫困", "失", "难", "苦", "痛", "唯一", "最后", "冷", "饿", "留守", "流浪"]
BREAKTHROUGH_PATTERNS = ["去", "做", "走", "找", "回来", "领", "收养", "送", "帮", "鼓励", "支持", "守", "等", "撑", "坚持"]

def luwei_q5_dilemma_breakthrough(new: str) -> Dict[str, bool]:
    """困境—突围保留：新 prompt 中必须既有困境信号也有突围/动作信号"""
    dilemmas = [p for p in DILEMMA_PATTERNS if p in new]
    breakthroughs = [p for p in BREAKTHROUGH_PATTERNS if p in new]
    has_both = len(dilemmas) > 0 and len(breakthroughs) > 0
    return {
        "q5_dilemma_breakthrough_retained": has_both,
        "detail": f"困境信号 {dilemmas[:3]}，突围动作 {breakthroughs[:3]}",
    }


# "只能他说"测试：抽取关键口播句，检查是否包含"这个人物独有"的细节
SPEECH_CUE_PATTERNS = [r"「[^」]*」", r"「[^」]*」", r'"[^"]*"', r"：[^。]+。"]

def luwei_q6_only_he_can_say(reference: str, new: str) -> Dict[str, bool]:
    """关键台词过"只能他说"测试：包含原 prompt 中没有的人物独有细节"""
    # 抽取 new 中的口播句
    speeches = []
    for pat in SPEECH_CUE_PATTERNS:
        speeches.extend(re.findall(pat, new))
    
    if not speeches:
        return {"q6_only_he_can_say": False, "detail": "未找到明确口播句"}
    
    # 看口播里是否包含具体人物细节（数字、年代、关系、具体物品）
    specific_markers = ["年", "岁", "次", "个", "天", "月", "次", "趟", "每天", "第一次", "第一次", "第一次"]
    has_specific = any(any(m in s for m in specific_markers) for s in speeches)
    
    return {
        "q6_only_he_can_say": has_specific,
        "detail": f"口播句数 {len(speeches)}，含人物独有细节: {has_specific}",
    }


def luwei_checks(reference: str, new: str) -> Dict[str, bool]:
    """合并 3 项芦苇自检"""
    q4 = luwei_q4_gen_retained(reference, new)
    q5 = luwei_q5_dilemma_breakthrough(new)
    q6 = luwei_q6_only_he_can_say(reference, new)
    return {
        "q4_xi_gen_retained": q4["q4_xi_gen_retained"],
        "q5_dilemma_breakthrough_retained": q5["q5_dilemma_breakthrough_retained"],
        "q6_only_he_can_say": q6["q6_only_he_can_say"],
    }


@dataclass
class InnovateResult:
    core_hooks: List[str]
    new_prompt: str
    detail_score: Dict[str, int]
    three_questions: Dict[str, bool]
    luwei_checks: Dict[str, bool]  # v0.2 新增
    similarity_to_reference: float
    similarity_to_history: float
    iterations: int
    passed: bool
    notes: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)


def micro_innovate(
    reference_prompt: str,
    history_prompts: Optional[List[str]] = None,
    avoid_patterns: Optional[List[str]] = None,
    new_prompt: Optional[str] = None,
    max_iterations: int = 3,
    sim_threshold: float = 70.0,
) -> InnovateResult:
    if new_prompt is None:
        raise ValueError("new_prompt 必须由调用方按 SCAMPER-LP + 芦苇维度流程生成")
    
    history_prompts = history_prompts or []
    avoid_patterns = avoid_patterns or []
    
    core_hooks = identify_hooks(reference_prompt)
    sim_to_ref = jaccard(reference_prompt, new_prompt)
    sim_to_hist = max([jaccard(new_prompt, h) for h in history_prompts], default=0.0)
    avoid_hits = [p for p in avoid_patterns if p in new_prompt]
    
    detail = detail_density(new_prompt)
    q = three_questions(reference_prompt, new_prompt, core_hooks)
    lq = luwei_checks(reference_prompt, new_prompt)
    
    passed = (
        sim_to_ref < sim_threshold
        and sim_to_hist < sim_threshold
        and not avoid_hits
        and all(q.values())
        and all(lq.values())
        and detail["sensory"] >= 1 and detail["cultural"] >= 1
    )
    
    notes = []
    if sim_to_ref >= sim_threshold: notes.append(f"与原始相似度 {sim_to_ref}% ≥ {sim_threshold}%")
    if sim_to_hist >= sim_threshold: notes.append(f"与历史相似度 {sim_to_hist}% ≥ {sim_threshold}%")
    if avoid_hits: notes.append(f"撞避坑清单：{avoid_hits}")
    if not all(q.values()): notes.append(f"三问未通过：{[k for k, v in q.items() if not v]}")
    if not all(lq.values()): notes.append(f"芦苇三检未通过：{[k for k, v in lq.items() if not v]}")
    if detail["sensory"] < 1: notes.append("缺少感官细节")
    if detail["cultural"] < 1: notes.append("缺少文化细节")
    
    return InnovateResult(
        core_hooks=core_hooks,
        new_prompt=new_prompt,
        detail_score=detail,
        three_questions=q,
        luwei_checks=lq,
        similarity_to_reference=sim_to_ref,
        similarity_to_history=sim_to_hist,
        iterations=1,
        passed=passed,
        notes=notes,
    )


if __name__ == "__main__":
    ref = "北方乡村返乡与土狗重逢：男孩当兵三年回来，狗在村口等"
    new = """帮我生成一个视频：深冬，北方山村大雪封山清晨。一只浅棕色土狗从破旧狗窝爬起来，踩着没过小腿积雪，颠颠跑到村口大树下，望着进村唯一的泥巴路。一年又一年它都在这里等——村里人念叨：当年那个穿军装的小子去当兵了，3 年没回来。镜头切回土狗正脸，鼻头冻得通红，胡须挂着冰碴。广播响起那天，土狗听到军靴声，跑出来看：是他，是他回来了！小男孩蹲下搂住土狗，眼眶泛红：老伙计，你等了我 3 年？土狗尾巴摇得欢实。镜头从狗的视角推向男孩（POV）：他带着北方乡音，声音哽咽：每次回家它都守在村口等我... 能不能给我们一点鼓励，谢谢大家？"""
    result = micro_innovate(ref, new_prompt=new)
    print("=== v0.2 Innovate Result ===")
    print(f"core_hooks: {result.core_hooks}")
    print(f"detail: {result.detail_score}")
    print(f"three_questions: {result.three_questions}")
    print(f"luwei_checks: {result.luwei_checks}")
    print(f"passed: {result.passed}")
    print(f"notes: {result.notes}")


# ============================================================
# v0.4 增量自检（验收问题驱动，2026-08-16）
# ============================================================

# 5 种结构骨架模板（用于 R15）
SKELETON_TEMPLATES = {
    "坚守": ["年", "每天", "一直", "坚持", "守", "凌晨"],
    "传承": ["交给", "接班", "离开", "最后一", "师父", "传承"],
    "反悔": ["本想", "差点", "最后", "决定", "没想到", "但是"],
    "对照": ["当年", "过去", "如今", "曾经", "那时候", "对比"],
    "被发现": ["路人", "发现", "第一次", "原来", "真相", "镜头后"],
}

# 前 3 秒钩子关键词（R16）
HOOK_3SEC_PATTERNS = {
    "数字": re.compile(r'\d+(?:年|岁|天|个|月|代|次|分|秒|小时)?'),
    "反差": re.compile(r'(?:本应|原本|没想到|可是|但是|却|然而)'),
    "悬念": re.compile(r'(?:…|\.{3}|？|!|为什么|谁|怎样|怎么)'),
}

# 受众分层钩子词（R19）
HOOK_WORDS_BY_AUDIENCE = {
    "women_18_40": ["心疼", "求求", "帮忙", "忍不住", "看哭了", "谁懂", "麻烦帮我"],
    "men_general": ["致敬", "支持", "顶一个", "干得漂亮", "硬核"],
    "neutral": ["请点赞", "麻烦帮我", "谢谢", "求赞"],
}

# 避雷镜头词（R20）
CAMERA_VAPOR_PATTERNS = re.compile(
    r'镜头从(?:外|门|远|全景)?(?:推|拉|摇|移)?(?:入|到|向|至)?'
    r'|慢慢(?:拉|推|摇|移)'
    r'|朦胧(?:了|了灯|灯光)'
    r'|蒸汽(?:缭绕|弥漫|升腾)'
    r'[\u4e00-\u9fa5，,。]{15,}'
)

# 奠基动作词（R22）—— 短视频常见奠基动作
FOUNDING_ACTIONS = [
    # 人物动作类
    "领", "收养", "等待", "退休", "团圆", "送别", "重逢",
    "传承", "守护", "归来", "承诺", "托付", "怀念",
    # 职业/经营类
    "开了", "开店", "开了一家", "经营", "做了", "做这行", "教书", "从医",
    "务农", "种", "养", "守岛", "守塔", "守边",
    # 物品/手艺类
    "绣", "编织", "缝", "烧窑", "打磨", "雕刻",
    # 时间类
    "30年", "10年", "20年", "一辈子", "一辈子", "一辈子",
    "一辈子",  # 加重
    "半辈子", "一代人", "祖辈",
]


def check_r2_revised(reference: str, new: str) -> Dict[str, Any]:
    """R2 修订：保留关键词非完整句。识别 reference 中的标志性完整句。"""
    # 找出 reference 中所有 "X，X。" / "X是X" / 含"的" 的完整短句
    full_sentences = re.findall(r'[^。！？\.!\?]{8,40}[。！？\.!\?]', reference)
    if not full_sentences:
        return {"pass": True, "detail": "reference 无完整短句，跳过"}
    
    # 找出 new 中完整复用的句子
    reused = [s for s in full_sentences if s in new]
    return {
        "pass": len(reused) <= 1,  # 完整句至多复用 1 次
        "detail": f"reference 有 {len(full_sentences)} 个完整句 / new 复用 {len(reused)} 个（上限 1）",
        "reused_sentences": reused,
    }


def check_r15_skeleton(new: str) -> Dict[str, Any]:
    """R15 结构骨架识别：返回这个候选所属骨架类型。"""
    matched = []
    for skeleton_name, keywords in SKELETON_TEMPLATES.items():
        if any(kw in new for kw in keywords):
            matched.append(skeleton_name)
    return {
        "pass": len(matched) >= 1,
        "detail": f"匹配骨架：{matched}",
        "skeletons": matched,
    }


def check_r16_3sec_hook(new: str) -> Dict[str, Any]:
    """R16 前 3 秒钩子：前 30 字含数字/反差/悬念。"""
    first_30 = new[:30]
    hits = {}
    for hook_type, pattern in HOOK_3SEC_PATTERNS.items():
        if pattern.search(first_30):
            hits[hook_type] = True
    
    has_hook = len(hits) > 0
    return {
        "pass": has_hook,
        "detail": f"前 30 字含钩子：{list(hits.keys()) or '无'}",
        "first_30": first_30,
    }


def check_r17_length(new: str, max_length: int = 80) -> Dict[str, Any]:
    """R17 长度约束：候选 ≤ max_length 字。"""
    actual_len = len(new)
    return {
        "pass": actual_len <= max_length,
        "detail": f"长度 {actual_len} 字（上限 {max_length}）",
        "too_long": actual_len > max_length,
        "actual_length": actual_len,
    }


def check_r18_logic(reference: str, new: str) -> Dict[str, Any]:
    """R18 逻辑自洽校验：年龄差 / 人物关系矛盾检测。

    注意：中文里数字和单位之间常有空格（如 "100 岁" / "90 年前"），
    正则需要兼容两种写法。
    """
    issues = []

    # 1. 提取 reference 和 new 中的年龄数字（兼容 "100 岁" / "100岁" 两种写法）
    new_ages = [int(m) for m in re.findall(r'(\d+)\s*岁', new)]

    # 2. 检测年龄差矛盾
    for age in new_ages:
        for n_years in re.findall(r'(\d+)\s*年', new):
            n = int(n_years)
            if age - n < 8:  # 倒推年龄 < 8 岁（学龄前）才算不合常理
                # 例外：童子功（10-12 岁学艺）也合理 → 阈值放宽到 8
                issues.append(f"{age}岁 - {n}年 = {age-n}岁，不合常理（学龄前）")

    # 3. 检测凭空添加的人物关系（如 reference 没提"女儿已故"）
    death_keywords = ["已故", "去世", "走了", "不在了", "阴阳两隔"]
    if any(kw in new for kw in death_keywords):
        ref_has_death = any(kw in reference for kw in death_keywords)
        if not ref_has_death:
            issues.append("凭空添加'已故'等人物关系")

    return {
        "pass": len(issues) == 0,
        "detail": f"逻辑问题：{issues or '无'}",
        "issues": issues,
    }


def check_r19_audience_hook(new: str, audience: str = "women_18_40") -> Dict[str, Any]:
    """R19 受众感知钩子词：按受众画像检查钩子词。"""
    audience_keywords = HOOK_WORDS_BY_AUDIENCE.get(audience, [])
    matched = [kw for kw in audience_keywords if kw in new]
    return {
        "pass": len(matched) >= 1,
        "detail": f"受众 '{audience}' 钩子词匹配：{matched or '无'}",
        "matched": matched,
    }


def check_r20_no_vapor_camera(new: str) -> Dict[str, Any]:
    """R20 避雷清单硬规则：镜头 > 30 字且无强事件 → 失败。"""
    # 检测长镜头描写
    camera_match = CAMERA_VAPOR_PATTERNS.search(new)
    if not camera_match:
        return {"pass": True, "detail": "无空镜堆砌"}
    
    vapor_text = camera_match.group()
    if len(vapor_text) <= 30:
        return {"pass": True, "detail": f"镜头描写 {len(vapor_text)} 字，未超阈值"}
    
    # 长度 > 30 时，检查是否有强事件/动作动词
    action_verbs = ["举", "放", "递", "开", "关", "切", "喊", "抱", "摔",
                     "递", "拍", "摸", "抬", "低", "笑", "哭", "看"]
    has_action = any(v in new for v in action_verbs)
    
    return {
        "pass": has_action,
        "detail": f"镜头 {len(vapor_text)} 字 + 强动作 {'有' if has_action else '无'}",
        "vapor_length": len(vapor_text),
    }


def check_r22_founding_action(reference: str) -> Dict[str, Any]:
    """R22 空 prompt 兜底：奠基动作 = 0 → 触发兜底。"""
    ref_actions = [a for a in FOUNDING_ACTIONS if a in reference]
    return {
        "pass": len(ref_actions) >= 1,
        "detail": f"reference 奠基动作：{ref_actions or '无'}（应 ≥1）",
        "founding_actions": ref_actions,
    }


# ============================================================
# v0.4 跨候选检查（cross-candidate）
# ============================================================

def check_r21_hook_diversity(candidates: List[str]) -> Dict[str, Any]:
    """R21 5 候选钩子词差异化：≥3 种。
    
    抓取末尾的钩子动词（如"致敬 / 鼓励 / 求求 / 帮忙 / 加油"等），
    而不是抓"师徒 / 父子"这种被点赞对象名词。
    """
    # 匹配模式：(点赞|鼓励|致敬|支持|帮忙|求求|心疼|看哭了|麻烦帮我|干得漂亮|顶一个) 后面 1-6 字
    hook_verbs = ["点赞致敬", "点赞鼓励", "求求", "麻烦帮我", "看哭了",
                  "忍不住", "心疼", "干得漂亮", "顶一个", "请支持", "求赞"]
    # 候选尾部常见参数尾巴（不属于钩子动词，必须排除）
    tail_noise_patterns = [
        r"9\s*[:：]\s*16\s*竖屏.*?$",
        r"4K\s*高清.*?$",
        r"60\s*秒以[内外].*?$",
        r"竖屏.*?$",
        r"高清.*?$",
        r"\d+K\s*高清.*?$",
    ]
    hooks = []
    for c in candidates:
        # 优先匹配多字钩子词（命中整段文本，包括尾巴之前的位置）
        matched = None
        for verb in hook_verbs:
            if verb in c:
                matched = verb
                break
        if matched:
            hooks.append(matched)
            continue
        # 退化：抓最后非参数尾巴的钩子部分
        tail_src = c
        for pat in tail_noise_patterns:
            tail_src = re.sub(pat, "", tail_src)
        tail = tail_src.strip()[-12:]
        if tail:
            hooks.append(f"(尾:{tail})")
        else:
            hooks.append("(尾:空)")
    
    unique_hooks = set(hooks)
    return {
        "pass": len(unique_hooks) >= 3,
        "detail": f"5 候选钩子动词：{hooks} / 唯一数 {len(unique_hooks)}（应 ≥3）",
        "hooks": hooks,
        "unique_count": len(unique_hooks),
    }


def check_r15_skeleton_diversity(candidates: List[str]) -> Dict[str, Any]:
    """R15 5 候选结构骨架 ≥3 种。"""
    all_skeletons = []
    for c in candidates:
        result = check_r15_skeleton(c)
        all_skeletons.extend(result["skeletons"])
    
    unique_skeletons = set(all_skeletons)
    return {
        "pass": len(unique_skeletons) >= 3,
        "detail": f"5 候选覆盖骨架：{list(unique_skeletons)}（应 ≥3）",
        "unique_count": len(unique_skeletons),
    }


def v04_checks(reference: str, new: str, audience: str = "women_18_40") -> Dict[str, Any]:
    """v0.4 全部 9 项自检（单候选）。"""
    return {
        "r2_revised": check_r2_revised(reference, new),
        "r16_3sec_hook": check_r16_3sec_hook(new),
        "r17_length": check_r17_length(new),
        "r18_logic": check_r18_logic(reference, new),
        "r19_audience_hook": check_r19_audience_hook(new, audience),
        "r20_no_vapor_camera": check_r20_no_vapor_camera(new),
        "r22_founding_action": check_r22_founding_action(reference),
    }


def v04_cross_candidate_checks(candidates: List[str]) -> Dict[str, Any]:
    """v0.4 跨候选自检。"""
    return {
        "r15_skeleton_diversity": check_r15_skeleton_diversity(candidates),
        "r21_hook_diversity": check_r21_hook_diversity(candidates),
    }


# ============================================================
# v0.4 整合版 micro_innovate
# ============================================================

def micro_innovate_v04(
    reference_prompt: str,
    new_prompts: List[str],
    audience: str = "women_18_40",
    max_length: int = 80,
    sim_threshold: float = 70.0,
) -> Dict[str, Any]:
    """
    v0.4 整合版微创新自检：
    - 输入：reference + 5 个 new_prompts（由调用方按 SCAMPER-LP 生成）
    - 输出：每个候选的 v0.3 自检 + v0.4 自检 + 跨候选自检
    
    返回：{
        "per_candidate": [{ v0.3 + v0.4 自检结果 }, ...],
        "cross_candidate": { R15 + R21 跨候选检查 },
        "all_pass": bool,
        "fallback_triggered": bool,  # R22 空 prompt
    }
    """
    if not new_prompts:
        # R22 fallback: 调用方未提供候选，主动告知进入 Profile §6.1 兜底 review
        return {
            "per_candidate": [],
            "cross_candidate": {},
            "all_pass": False,
            "fallback_triggered": True,
            "fallback_reason": "new_prompts 为空，v0.4 自检无法跨候选对比；进入 Profile §6.1 兜底 review，要求调用方先按 SCAMPER-LP 生成 ≥3 个候选。",
            "guidance": [
                "1. 用 SCAMPER-LP 五维（Substitute / Modify / Adapt / Combine / Put）启发式或 LLM 生成候选",
                "2. 每个候选 MUST 走不同骨架（坚守 / 传承 / 反悔 / 对照 / 被发现）",
                "3. 每个候选 MUST 含受众钩子词（women_18_40：心疼 / 看哭了 / 忍不住 / 致敬 等）",
                "4. 每个候选长度 MUST ≤ 80 字",
            ],
        }
    
    # R22: 先检查 reference 是否有奠基动作（空 prompt 兜底）
    r22 = check_r22_founding_action(reference_prompt)
    if not r22["pass"]:
        return {
            "per_candidate": [],
            "cross_candidate": {},
            "all_pass": False,
            "fallback_triggered": True,
            "fallback_reason": f"reference 无奠基动作（R22），触发 Profile §6.1 兜底 review",
            "r22_detail": r22,
        }
    
    # 逐候选自检
    per_candidate = []
    for new_prompt in new_prompts:
        # 原有 v0.3 自检
        core_hooks = identify_hooks(reference_prompt)
        sim_to_ref = jaccard(reference_prompt, new_prompt)
        detail = detail_density(new_prompt)
        q = three_questions(reference_prompt, new_prompt, core_hooks)
        lq = luwei_checks(reference_prompt, new_prompt)
        
        # 新增 v0.4 自检
        v04 = v04_checks(reference_prompt, new_prompt, audience=audience)
        
        # 综合通过判定
        v03_pass = (
            sim_to_ref < sim_threshold
            and all(q.values())
            and all(lq.values())
            and detail["sensory"] >= 1 and detail["cultural"] >= 1
        )
        v04_pass = all(c["pass"] for c in v04.values())
        
        per_candidate.append({
            "new_prompt": new_prompt,
            "v03": {
                "similarity_to_reference": sim_to_ref,
                "detail_score": detail,
                "three_questions": q,
                "luwei_checks": lq,
                "passed": v03_pass,
            },
            "v04": v04,
            "all_pass": v03_pass and v04_pass,
        })
    
    # 跨候选自检
    cross = v04_cross_candidate_checks([c["new_prompt"] for c in per_candidate])
    cross_pass = all(c["pass"] for c in cross.values())
    
    return {
        "per_candidate": per_candidate,
        "cross_candidate": cross,
        "all_pass": cross_pass and all(c["all_pass"] for c in per_candidate),
        "fallback_triggered": False,
    }
