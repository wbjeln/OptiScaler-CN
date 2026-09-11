#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确找出「用户可见弹窗」里还没汉化的英文文案。

为什么要精确到括号范围：
    ImGui::InsertNotification({ ImGuiToastType::Error, 20000, "英文" }) 里的是玩家
    会在游戏里看到的弹窗；而紧邻的 LOG_DEBUG("英文") 只是写日志，不该算进「界面
    汉化」范围。只按行扫描会把两者混在一起。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent / "src"
CALLS = ("ImGui::InsertNotification", "InsertNotification", ".setTitle", ".setContent",
         "setButtonLabel")
LIT = re.compile(r'"((?:[^"\\]|\\.)*)"')
CJK = re.compile(r"[\u4e00-\u9fff]")


def literals_in_call(text: str, open_paren: int):
    """从 open_paren 处的 '(' 开始，按括号配平取出本次调用里的所有字符串字面量"""
    depth = 0
    i = open_paren
    n = len(text)
    out = []
    while i < n:
        c = text[i]
        if c == '"':
            m = LIT.match(text, i)
            if not m:
                break
            out.append(m.group(1))
            i = m.end()
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                break
        i += 1
    return out


def main():
    hits = {}
    for pat in ("**/*.cpp", "**/*.h", "**/*.hpp"):
        for f in ROOT.glob(pat):
            p = str(f).replace("\\", "/")
            if "/external/" in p or "/include/" in p or "/menu/font/" in p:
                continue
            try:
                t = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                # 上游有个别非 UTF-8 文件，跳过（本次汉化也不涉及它们）
                continue
            for call in CALLS:
                start = 0
                while True:
                    k = t.find(call, start)
                    if k < 0:
                        break
                    start = k + len(call)
                    # 避免 "InsertNotification" 在 "ImGui::InsertNotification" 里被重复统计
                    if call == "InsertNotification" and t[max(0, k - 7):k] == "ImGui::":
                        continue
                    op = t.find("(", k)
                    if op < 0 or op - k > 40:
                        continue
                    line = t[:k].count("\n") + 1
                    for s in literals_in_call(t, op):
                        if not s or CJK.search(s):
                            continue
                        if len(re.findall(r"[A-Za-z]{2,}", s)) < 2 and len(s) < 8:
                            continue
                        rel = str(f.relative_to(ROOT)).replace("\\", "/")
                        hits.setdefault(rel, []).append((line, s))

    total = 0
    for rel in sorted(hits):
        print(f"\n### {rel}")
        for line, s in hits[rel]:
            print(f"  行{line:>5}: {s!r}")
            total += 1
    if total == 0:
        print("未发现未汉化的弹窗文案。")
    else:
        print(f"\n合计未汉化弹窗文案：{total} 条，涉及 {len(hits)} 个文件")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
