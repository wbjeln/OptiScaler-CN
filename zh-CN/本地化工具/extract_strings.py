#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OptiScaler 界面字符串抽取器 v2

相比 v1 的三处关键改进：
  1. 合并相邻字面量：源码里长提示语常写成 "第一段\\n" "第二段"，必须当成一个整体翻译，
     否则会出现中英混杂的句子。
  2. 补全包装函数：ShowHelpMarker / ScopedCollapsingHeader / SeparatorText / PopulateCombo /
     AddResourceBarrier / CalcTextSize 等自定义封装里的文字同样是玩家可见的。
  3. 增加 Tier C：初始化列表里的标签（如 std::vector<MenuOption<T>> = { {值, "标签", "说明"} }）
     这些是下拉框选项文字，v1 完全漏掉了。

输出 JSON 结构：
  { file, line, start, end, parts: [[s,e],...], call, tier, has_id, text }
  回写时把译文写进 parts[0]，其余 parts 置空，保证 C++ 字符串拼接结果正确。
"""
import json
import pathlib
import re
import sys
from collections import Counter

UI_CALLS = {
    # 标准 ImGui
    "Text", "TextWrapped", "TextDisabled", "TextColored", "TextUnformatted",
    "LabelText", "BulletText", "TextLink", "TextLinkOpenURL", "SeparatorText",
    "Button", "SmallButton", "ArrowButton",
    "Checkbox", "RadioButton", "Selectable", "MenuItem",
    "BeginCombo", "Combo", "BeginListBox", "ListBox",
    "BeginMenu", "BeginTabItem", "TabItem",
    "CollapsingHeader", "TreeNode", "TreeNodeEx",
    "SetTooltip", "SetItemTooltip", "BeginPopupModal", "Begin",
    "BeginChild", "InputText", "InputTextMultiline", "InputInt", "InputFloat",
    "SliderFloat", "SliderInt", "SliderFloat2", "SliderFloat3",
    "DragFloat", "DragInt", "ProgressBar", "BeginTable", "TableSetupColumn",
    "TableHeader", "TableNextColumn", "CalcTextSize",
    # 通知弹窗
    "setTitle", "setContent",
    # 本项目自定义封装
    "ShowHelpMarker", "ScopedCollapsingHeader", "PopulateCombo",
    "AddResourceBarrier", "PopulateTab", "ShowHelpMarkerWithIcon",
}

SKIP_CALLS = {
    "PushID", "PopID", "GetID", "ImHashStr", "LOG_DEBUG", "LOG_INFO",
    "LOG_WARN", "LOG_ERROR", "LOG_TRACE", "LOG_IMPORTANT", "AddLogView",
}

SCOPE_INCLUDE = ("OptiScaler/menu/", "OptiScaler/dllmain.cpp")
SCOPE_EXCLUDE = ("OptiScaler/menu/font/", "/imgui/", "/external/")

TOKEN_TAIL = re.compile(r"([A-Za-z_][A-Za-z0-9_:<>]*)\s*$")
MERGE_GAP = re.compile(r'"\s*"', re.S)


def in_scope(rel):
    if any(x in rel for x in SCOPE_EXCLUDE):
        return False
    return any(rel.startswith(x) for x in SCOPE_INCLUDE)


def scan_literals(text):
    """返回 [(content_start, content_end, raw)]，跳过注释、字符字面量与原始字符串。"""
    out = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            j = text.find("\n", i)
            i = n if j < 0 else j + 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if c == "R" and i + 1 < n and text[i + 1] == '"':
            j = text.find("(", i + 2)
            if 0 < j - i < 20:
                close = ")" + text[i + 2:j] + '"'
                k = text.find(close, j)
                if k >= 0:
                    i = k + len(close)
                    continue
        if c == '"':
            j = i + 1
            buf = []
            while j < n:
                ch = text[j]
                if ch == "\\":
                    buf.append(text[j:j + 2])
                    j += 2
                    continue
                if ch == '"':
                    break
                buf.append(ch)
                j += 1
            out.append((i + 1, j, "".join(buf)))
            i = j + 1
            continue
        if c == "'":
            j = text.find("'", i + 1)
            if 0 < j - i <= 6:
                i = j + 1
                continue
        i += 1
    return out


def merge_adjacent(text, parts):
    """把只被引号+空白分隔的相邻字面量合并为一个逻辑字符串"""
    if not parts:
        return []
    groups = [[parts[0]]]
    for prev, cur in zip(parts, parts[1:]):
        gap = text[prev[1]:cur[0]]
        if MERGE_GAP.fullmatch(gap):
            groups[-1].append(cur)
        else:
            groups.append([cur])
    merged = []
    for g in groups:
        raw = "".join(p[2] for p in g)
        merged.append({"parts": [[p[0], p[1]] for p in g], "raw": raw,
                       "start": g[0][0], "end": g[-1][1]})
    return merged


def init_ranges(text):
    """返回 [ (start,end) ] —— 花括号初始化列表的区间，用于识别标签数组"""
    ranges = []
    stack = []  # (brace_pos, is_init)
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            j = text.find("\n", i)
            i = n if j < 0 else j + 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        if c in '"\'':
            # 跳过字面量内容
            q = c
            j = i + 1
            while j < n and text[j] != q:
                j += 2 if text[j] == "\\" else 1
            i = j + 1
            continue
        if c == "{":
            k = i - 1
            while k >= 0 and text[k] in " \t\r\n":
                k -= 1
            prev = text[k] if k >= 0 else ""
            parent_init = stack[-1][1] if stack else False
            is_init = prev == "=" or (parent_init and prev in "{,")
            stack.append((i, is_init))
        elif c == "}":
            if stack:
                pos, is_init = stack.pop()
                if is_init:
                    ranges.append((pos, i))
        i += 1
    return ranges


def call_context(text, lit_start, window=400):
    seg = text[max(0, lit_start - window):lit_start]
    depth = 0
    commas = 0
    for k in range(len(seg) - 1, -1, -1):
        ch = seg[k]
        if ch in ")]}":
            depth += 1
        elif ch in "([{":
            if depth == 0:
                if ch == "(":
                    m = TOKEN_TAIL.search(seg[:k])
                    return (m.group(1) if m else None), commas
                return None, None
            depth -= 1
        elif ch == "," and depth == 0:
            commas += 1
        elif ch == ";" and depth == 0:
            return None, None
    return None, None


def short_name(fn):
    return fn.split("::")[-1].split("<")[0] if fn else ""


def looks_like_sentence(s):
    if len(s) < 6 or len(s) > 400:
        return False
    if not re.search(r"[A-Za-z]{2}", s):
        return False
    return len(re.findall(r"[A-Za-z]{2,}", s)) >= 3


def main():
    root = pathlib.Path(sys.argv[1])
    out_path = pathlib.Path(sys.argv[2])
    files = []
    for pat in ("**/*.cpp", "**/*.h", "**/*.hpp"):
        for f in root.glob(pat):
            if in_scope(str(f.relative_to(root)).replace("\\", "/")):
                files.append(f)

    entries = []
    for f in sorted(set(files)):
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = str(f.relative_to(root)).replace("\\", "/")
        parts = scan_literals(text)
        merged = merge_adjacent(text, parts)
        inits = init_ranges(text)

        def in_init(pos):
            return any(a <= pos <= b for a, b in inits)

        for m in merged:
            fn, argi = call_context(text, m["start"])
            sn = short_name(fn)
            if sn in SKIP_CALLS:
                continue
            tier = None
            if sn in UI_CALLS:
                tier = "A"
            elif in_init(m["start"]):
                tier = "C"
            elif not sn and looks_like_sentence(m["raw"]):
                tier = "B"
            if tier is None or not m["raw"].strip():
                continue
            entries.append({
                "file": rel,
                "line": text.count("\n", 0, m["start"]) + 1,
                "start": m["start"], "end": m["end"], "parts": m["parts"],
                "call": fn or "", "arg": argi, "tier": tier,
                "has_id": "##" in m["raw"],
                "text": m["raw"],
            })

    by_file = Counter(x["file"] for x in entries)
    payload = {
        "root": str(root), "total": len(entries),
        "unique": len(set(x["text"] for x in entries)),
        "tier_count": dict(Counter(x["tier"] for x in entries)),
        "by_file": dict(by_file.most_common()),
        "entries": entries,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"files: {len(set(files))}  entries: {len(entries)}  unique: {payload['unique']}")
    print("tier:", payload["tier_count"])
    print("多段拼接条目:", sum(1 for x in entries if len(x["parts"]) > 1))
    for k, v in by_file.most_common(6):
        print(f"  {v:5d}  {k}")


if __name__ == "__main__":
    main()
