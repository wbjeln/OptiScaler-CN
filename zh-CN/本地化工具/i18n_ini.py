#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OptiScaler.ini 注释汉化

只改注释（; 开头），键名与取值一律不动，保证和官方配置完全兼容。

处理顺序：
  1. 词典层  ini_dict_*.tsv   （高优先级，逐条人工翻译）
  2. 保留层  ini_dict_*.tsv 中"只有英文、没有 Tab"的行 —— 有意保持原样（URL、dll 文件名等）
  3. 规则层  RULES            （批量模板句，作为兜底）
  4. 仍未命中的原样保留，并写入 build/ini_report.txt

匹配采用"空白归一化"：把连续空白压成一个空格再去首尾，
因此源文件里的对齐空格/制表符差异不会造成漏配。
"""
import argparse
import glob
import pathlib
import re
import sys

# ---------------------------------------------------------------- 归一化

_WS = re.compile(r"\s+")


def norm(s: str) -> str:
    return _WS.sub(" ", s).strip()


# ---------------------------------------------------------------- 规则层
# 全部作用于 norm() 之后的小写敏感原文
RULES = [
    # true or false ...
    (re.compile(r"^true or false\s*-\s*Default \(auto\) is\s+(.*)$"),
     r"true 或 false - 默认（auto）为 \1"),
    (re.compile(r"^true or false\s*-\s*Default \(auto\)\s+(.*)$"),
     r"true 或 false - 默认（auto）\1"),
    # 纯默认值
    (re.compile(r"^Default \(auto\) is\s+(.*)$"), r"默认（auto）为 \1"),
    (re.compile(r"^Default \(auto\) is disabled$"), r"默认（auto）为禁用"),
    (re.compile(r"^Default \(auto\) values:$"), r"默认（auto）值："),
    # 区间 + 默认值（带 is）
    (re.compile(r"^([-\d.]+)\s*(?:to|~)\s*([-\d.]+|max float value|infinite)\s*-\s*Default \(auto\) is\s+(.*)$"),
     r"\1 至 \2 - 默认（auto）为 \3"),
    (re.compile(r"^([-\d.]+)\s*-\s*([-\d.]+|max float value|infinite)\s*-\s*Default \(auto\) is\s+(.*)$"),
     r"\1 - \2 - 默认（auto）为 \3"),
    # 区间 + 默认值（无 is）
    (re.compile(r"^([-\d.]+)\s*(?:to|~)\s*([-\d.]+)\s*-\s*Default \(auto\)\s+(.*)$"),
     r"\1 至 \2 - 默认（auto）\3"),
    # 单个数值 + 默认值
    (re.compile(r"^([-\d.]+|max)\s*[-=]\s*Default \(auto\) is\s+(.*)$"),
     r"\1 - 默认（auto）为 \2"),
    (re.compile(r"^([-\d.]+|max)\s*[-=]\s*Default \(auto\)\s+(.*)$"),
     r"\1 - 默认（auto）\2"),
]

# 类型前缀（float/integer/uint/string 等）+ 默认值
_TYPE_PREFIX = re.compile(
    r"^(float|integer|uint|int|string|bool)\s+value(\s+above\s*>\s*0)?\s*-\s*Default \(auto\) is\s+(.*)$",
    re.I,
)

_TYPE_ZH = {
    "float": "float", "integer": "整数", "uint": "uint", "int": "整数",
    "string": "字符串", "bool": "布尔",
}

# 枚举行：含 " - Default (auto) is " 且左侧是 option 列表
ENUM_DEFAULT = re.compile(r"^(.*?)\s*-\s*Default \(auto\) is\s+(.*)$")

# 枚举行里可安全替换的通用词（按长度倒序，避免子串冲突）
WORDS = [
    ("Default", "默认"), ("disabled", "禁用"), ("unselected", "未选择"),
    ("Unlimited", "无限制"), ("infinite", "无限"),
    ("none selected", "未选择"), ("none", "无"), ("off", "关闭"),
]


def _word_pass(text: str) -> str:
    out = text
    for en, zh in WORDS:
        out = re.sub(rf"(?<![A-Za-z]){re.escape(en)}(?![A-Za-z])", zh, out)
    return out


def apply_rules(text: str):
    """text 必须已 norm()"""
    m = _TYPE_PREFIX.match(text)
    if m:
        kind = m.group(1).lower()
        mid = m.group(2) or ""
        mid_zh = "，取值需大于 0" if mid else ""
        return f"{_TYPE_ZH.get(kind, kind)}{mid_zh} - 默认（auto）为 {m.group(3)}"

    for pat, rep in RULES:
        m = pat.match(text)
        if m:
            return m.expand(rep)

    m = ENUM_DEFAULT.match(text)
    if m:
        left, right = m.group(1), m.group(2)
        # 左侧看起来像枚举选项（含逗号或全是短标识符）才处理
        if "," in left or re.fullmatch(r"[A-Za-z0-9_\- ]{1,40}", left.strip()):
            return f"{_word_pass(left)} - 默认（auto）为 {_word_pass(right)}"
    return None


# ---------------------------------------------------------------- 词典层

def load_dict():
    """返回 (dict_en2zh, keep_set, stats)"""
    d, keep, stats = {}, set(), {}
    base = pathlib.Path(__file__).resolve().parent
    for f in sorted(glob.glob(str(base / "ini_dict_*.tsv"))):
        n_t, n_k = 0, 0
        for raw in pathlib.Path(f).read_text(encoding="utf-8").splitlines():
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            if "\t" in raw:
                en, zh = raw.split("\t", 1)
                en, zh = norm(en), zh.strip()
                if en and zh:
                    d[en] = zh
                    n_t += 1
            else:
                k = norm(raw)
                if k:
                    keep.add(k)
                    n_k += 1
        stats[pathlib.Path(f).name] = (n_t, n_k)
    return d, keep, stats


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ini", default="src/OptiScaler.ini")
    ap.add_argument("--out", default="src/OptiScaler.ini")
    ap.add_argument("--report", default="build/ini_report.txt")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    d, keep, stats = load_dict()
    print(f"[词典] {len(d)} 条翻译，{len(keep)} 条有意保持原样")
    for k, v in stats.items():
        print(f"        {k}: 翻译 {v[0]} / 保留 {v[1]}")

    p = pathlib.Path(args.ini)
    lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
    out, unmatched = [], []
    n_dict = n_keep = n_rule = 0

    for ln in lines:
        if not ln.strip().startswith(";"):
            out.append(ln)
            continue
        m = re.match(r"^(\s*;\s?)(.*)$", ln.rstrip("\r\n"))
        if not m:
            out.append(ln)
            continue
        prefix, body = m.group(1), m.group(2)
        lead = body[: len(body) - len(body.lstrip())]
        key = norm(body)
        if not key or set(key) <= {"-", "=", "*", "_"}:
            out.append(ln)
            continue

        zh = d.get(key)
        if zh is not None:
            n_dict += 1
        elif key in keep:
            n_keep += 1
            out.append(ln)
            continue
        else:
            zh = apply_rules(key)
            if zh:
                n_rule += 1
        if not zh:
            unmatched.append(key)
            out.append(ln)
            continue
        out.append(prefix + lead + zh + ("\n" if ln.endswith("\n") else ""))

    if not args.dry_run:
        p.write_text("".join(out), encoding="utf-8")

    print(f"[结果] 词典命中 {n_dict} 行，有意保留 {n_keep} 行，规则命中 {n_rule} 行，未处理 {len(unmatched)} 行")
    pathlib.Path(args.report).write_text("\n".join(sorted(set(unmatched))), encoding="utf-8")
    if unmatched:
        print(f"[提示] 未处理清单已写入 {args.report}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
