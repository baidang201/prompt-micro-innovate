# -*- coding: utf-8 -*-
"""
prompt-micro-innovate v0.4.1 · 3 样本端到端实测 runner

跑 3 个真实样本 × 5 个启发式 SCAMPER-LP 候选 × 21 项自检，
输出结构化结果到 stdout。

用法：
    python3 tests/e2e_runner.py
"""
import sys
from pathlib import Path

# 把 scripts/ 加入 sys.path
SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

from innovate import micro_innovate_v04


SAMPLE_1 = """帮我生成一个视频：南方小镇上，一家开在巷口的早餐店。每天凌晨3点，老板娘揉面，老板烧火，灶台蒸汽朦胧了灯光。30年了，他们每天只睡4个小时。镜头从门外推进屋内，从第一笼包子出炉到天亮；老板说："我不为赚钱，就是想让早起赶路的人有口热的。"9:16 竖屏，4K 高清，60 秒以内。请给这对夫妻点赞鼓励。"""

SAMPLE_2 = """帮我生成一个视频：周末，几个朋友约好去爬山。他们爬到山顶，坐下来聊天看风景吃零食。天气很好，山下景色很美。大家很开心，拍了几张照片就下山了。9:16 竖屏。"""

SAMPLE_3 = """帮我生成一个视频：云南山村的彝族老奶奶，今年 70 岁，还在绣她 50 年前没绣完的嫁衣。镜头从她布满老茧的手指特写起，慢慢拉到整件嫁衣。她说："我要在闭眼之前把它绣完，留给孙女。" 9:16 竖屏，4K 高清，60 秒以内。请给这位老奶奶点赞祝福。"""


def gen_for_breakfast():
    """sample-1 早餐店 · 5 个 SCAMPER-LP 启发式候选"""
    return [
        "帮我生成一个视频：北方山村里，一家开在村口的豆腐坊。每天凌晨2点，老汉磨豆，老伴烧火，蒸汽朦胧了灶台的灯。40年了，他们每天只睡5个小时。镜头从雪地里推进屋内，从第一锅豆浆翻滚到天亮；老汉说：「不为赚钱，就是想让上山砍柴的人有口热的。」9:16 竖屏，4K 高清，60 秒以内。请给这对夫妻点赞鼓励。",
        "帮我生成一个视频：南方小镇巷口，一家30年的早餐店。每天凌晨3点，老板娘揉面，老板烧火，灶台蒸汽朦胧了灯光。墙上老座钟停在3:17，他们每天只睡4个小时。镜头从门缝钻进屋内，从第一笼包子出炉到天亮；老板说：「不为赚钱，就是想让早起赶路的人有口热的。」9:16 竖屏，4K 高清，60 秒以内。",
        "帮我生成一个视频：80年代的南方小镇，一家开在巷口的早餐店。每天凌晨3点，老板娘围着蓝布围裙揉面，老板往灶膛里添柴，蒸汽朦胧了昏黄的灯泡。30年了，他们每天只睡4个小时。镜头从贴满奖状的木门推进屋内，从第一笼包子出炉到天亮；老板说：「不为赚钱，就是想让早起赶路的人有口热的。」9:16 竖屏。",
        "帮我生成一个视频：南方小镇巷口的早餐店，开了30年。每天凌晨3点，老板娘揉面，老板烧火，灶台蒸汽朦胧了灯光。儿子去年辞了城里的工作回乡接班。他们每天只睡4个小时。镜头从门外推进屋内，从第一笼包子出炉到天亮；儿子说：「爸妈不为赚钱，就是想让早起赶路的人有口热的，我得替他们把这口锅守住。」9:16 竖屏，4K 高清，60 秒以内。",
        "帮我生成一个视频：以老板娘的第一人称视角。南方小镇巷口开了30年的早餐店。每天凌晨3点，我揉面，老板烧火，灶台蒸汽朦胧了灯光。我们每天只睡4个小时。镜头从我的眼睛看出去，从第一笼包子出炉到天亮；我对自己说：「不为赚钱，就是想让早起赶路的人有口热的。」9:16 竖屏，4K 高清，60 秒以内。请给这对夫妻点赞。",
    ]


def gen_for_embroidery():
    """sample-3 嫁衣 · 5 个 SCAMPER-LP 启发式候选"""
    return [
        "帮我生成一个视频：贵州苗寨的阿妈，今年72岁，还在绣她30年前没绣完的百鸟衣。镜头从她膝盖上褪色的绣绷起，慢慢拉到整件衣裳。她说：「闭眼之前要把它绣完，传给儿媳妇。」9:16 竖屏，4K 高清，60 秒以内。请给这位阿妈点赞祝福。",
        "帮我生成一个视频：云南山村的彝族老奶奶，今年70岁，还在绣她50年前没绣完的嫁衣。煤油灯下，老花镜压在鼻梁上。镜头从她布满老茧的手指特写起，慢慢拉到整件嫁衣。她说：「我要在闭眼之前把它绣完，留给孙女。」9:16 竖屏，4K 高清，60 秒以内。",
        "帮我生成一个视频：1958年开始绣嫁衣的彝族老奶奶。今年70岁。镜头从1958年她绣的第一针起，到今天满屋的绣线。她说：「50年了，从黑发绣到白发。闭眼之前要把它绣完，留给孙女。」9:16 竖屏，4K 高清，60 秒以内。",
        "帮我生成一个视频：云南山村的彝族老奶奶，今年70岁，带着女儿一起绣她50年前没绣完的嫁衣。镜头从母女俩对坐的手指特写起，切换50年前同款绣绷的旧照片。她说：「闭眼之前要把它绣完，留给孙女，也留给女儿一段我们一起走过的日子。」9:16 竖屏，4K 高清，60 秒以内。请点赞祝福。",
        "帮我生成一个视频：以孙女的第一人称视角。云南山村，奶奶今年70岁，还在绣她50年前没绣完的嫁衣。我从小看奶奶绣，现在我帮她穿针。镜头从我手里针线起，拉到整件嫁衣。奶奶说：「闭眼之前要把它绣完，留给你。」9:16 竖屏，4K 高清，60 秒以内。请给奶奶点赞。",
    ]


def walk_fails(node, prefix="", out=None):
    """递归收集所有 false 项。"""
    if out is None:
        out = []
    if isinstance(node, dict):
        for k_leaf in ("pass", "passed"):
            if k_leaf in node and isinstance(node[k_leaf], bool):
                if not node[k_leaf]:
                    reason = node.get("reason") or node.get("detail") or ""
                    out.append((prefix or "<root>", reason))
                return out
        for k, v in node.items():
            if k.startswith("_"):
                continue
            new_prefix = f"{prefix}.{k}" if prefix else k
            walk_fails(v, new_prefix, out)
    elif isinstance(node, bool) and not node and prefix:
        out.append((prefix, ""))
    return out


def fmt_sample(name, ref, candidates, result):
    line = "=" * 78
    print(line)
    print(f"【{name}】")
    print(f"原始长度 {len(ref)} 字 · 候选数 {len(candidates)}")
    print(line)

    fb = result.get("fallback_triggered")
    pc_list = result.get("per_candidate", [])
    cross = result.get("cross_candidate", {})
    fb_signal = fb is True or (not candidates and not pc_list and not cross)
    print(f"all_pass = {result.get('all_pass')} · fallback_field = {fb}")
    print()

    print("【跨候选检查】")
    if not cross:
        print("  (空 — fallback 路径不跑 cross)")
    for k, v in cross.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict):
            print(f"  {k}: {v.get('pass', '?')} · {v.get('detail', '')}")
        else:
            print(f"  {k}: {v}")
    print()

    if fb_signal:
        print("🛡️  R22 fallback 已触发 ✓")
        print(f"   reason: {result.get('fallback_reason', '')}")
        if result.get("guidance"):
            print("   guidance:")
            for g in result["guidance"]:
                print(f"     - {g}")
        return

    if not pc_list:
        print("  (无单候选检查结果)")
        return

    print("【单候选检查】")
    for i, pc in enumerate(pc_list, 1):
        text = candidates[i - 1] if i - 1 < len(candidates) else ""
        passed = pc.get("all_pass", False)
        mark = "✅" if passed else "❌"
        snippet = text[:55] + "..." if len(text) > 55 else text
        print(f"\n候选 {i} ({len(text)} 字) {mark}")
        print(f"  {snippet}")
        fails = walk_fails({"v03": pc.get("v03", {}), "v04": pc.get("v04", {})})
        if fails:
            print(f"  失败项 ({len(fails)}):")
            for k, rs in fails:
                line = f"    - {k}"
                if rs:
                    line += f" :: {rs}"
                print(line)
        else:
            print("  全部通过")


def main():
    print("\n" + "#" * 78)
    print("# prompt-micro-innovate v0.4.1 · 3 样本实测")
    print("#" * 78 + "\n")

    c1 = gen_for_breakfast()
    r1 = micro_innovate_v04(SAMPLE_1, c1, audience="women_18_40")
    fmt_sample("sample-1 早餐店夫妻（152 字）", SAMPLE_1, c1, r1)
    print("\n")

    r2 = micro_innovate_v04(SAMPLE_2, [], audience="women_18_40")
    fmt_sample("sample-2 周末爬山（79 字，故意残缺）", SAMPLE_2, [], r2)
    print("\n")

    c3 = gen_for_embroidery()
    r3 = micro_innovate_v04(SAMPLE_3, c3, audience="women_18_40")
    fmt_sample("sample-3 彝族老奶奶 + 嫁衣（126 字）", SAMPLE_3, c3, r3)

    print("\n" + "#" * 78)
    print("# 汇总")
    print("#" * 78)
    print(f"  sample-1  all_pass={r1.get('all_pass')}  cross_keys={list(r1.get('cross_candidate',{}).keys())}")
    print(f"  sample-2  all_pass={r2.get('all_pass')}  fallback_field={r2.get('fallback_triggered')}")
    print(f"  sample-3  all_pass={r3.get('all_pass')}  cross_keys={list(r3.get('cross_candidate',{}).keys())}")


if __name__ == "__main__":
    main()
