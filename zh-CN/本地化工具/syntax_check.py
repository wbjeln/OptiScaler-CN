#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C++ 源码快速语法自检（无法本地编译时的兜底手段）

不复用简单的正则剥离，而是写一个小状态机，正确处理：
  - 行注释 //   块注释 /* */
  - 普通字符串（含 \" \\ 转义、以及 "a" "b" 相邻拼接）
  - 字符字面量（含 '\\'' 这类转义）
  - 原始字符串 R"delim(...)delim"
然后在"去掉注释与字面量"的代码上统计括号/引号配平。
用法: syntax_check.py <file.cpp> [file2.cpp ...]
"""
import pathlib
import sys


def strip_code(src: str):
    """返回 (纯代码, 问题列表)"""
    out = []
    i, n = 0, len(src)
    line = 1
    problems = []
    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            out.append(c)
            i += 1
            continue
        # 行注释
        if c == "/" and i + 1 < n and src[i + 1] == "/":
            while i < n and src[i] != "\n":
                i += 1
            continue
        # 块注释
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            start_line = line
            i += 2
            while i < n and not (src[i] == "*" and i + 1 < n and src[i + 1] == "/"):
                if src[i] == "\n":
                    line += 1
                    out.append("\n")
                i += 1
            if i >= n:
                problems.append(f"第 {start_line} 行开始的块注释没有闭合")
            i += 2
            continue
        # 原始字符串 R"delim( ... )delim"
        if c in "Rr" and i + 1 < n and src[i + 1] == '"':
            j = i + 2
            delim = ""
            while j < n and src[j] != "(":
                delim += src[j]
                j += 1
            end = ")" + delim + '"'
            k = src.find(end, j)
            if k == -1:
                problems.append(f"第 {line} 行的原始字符串没有闭合")
                break
            line += src.count("\n", i, k)
            out.append('""')
            i = k + len(end)
            continue
        # 普通字符串 / 字符字面量
        if c in "\"'":
            quote = c
            j = i + 1
            ok = False
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == "\n":
                    break
                if src[j] == quote:
                    ok = True
                    break
                j += 1
            if not ok:
                problems.append(f"第 {line} 行的 {quote} 字面量没有闭合")
                i += 1
                continue
            if quote == "'":
                out.append("''")
            else:
                out.append('""')
            i = j + 1
            continue
        out.append(c)
        i += 1
    return "".join(out), problems


def check(path: pathlib.Path):
    src = path.read_text(encoding="utf-8")
    # 处理续行：反斜杠换行
    src = src.replace("\\\r\n", " ").replace("\\\n", " ")
    code, problems = strip_code(src)
    pairs = {"{": "}", "(": ")", "[": "]"}
    stack = []
    for idx, ch in enumerate(code):
        if ch in pairs:
            stack.append((ch, code.count("\n", 0, idx) + 1))
        elif ch in pairs.values():
            if not stack:
                problems.append(f"第 {code.count(chr(10), 0, idx) + 1} 行出现多余的 {ch}")
            else:
                op, ln = stack.pop()
                if pairs[op] != ch:
                    problems.append(f"第 {ln} 行的 {op} 与第 {code.count(chr(10),0,idx)+1} 行的 {ch} 不匹配")
    for op, ln in stack:
        problems.append(f"第 {ln} 行的 {op} 没有闭合")
    return problems, len(src)


def main():
    rc = 0
    for arg in sys.argv[1:]:
        p = pathlib.Path(arg)
        problems, size = check(p)
        if problems:
            rc = 1
            print(f"[失败] {p.name} ({size} 字节)")
            for x in problems[:15]:
                print("   -", x)
        else:
            print(f"[通过] {p.name} ({size} 字节) 括号与字面量配平正常")
    return rc


if __name__ == "__main__":
    sys.exit(main())
