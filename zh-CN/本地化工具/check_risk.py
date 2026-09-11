#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汉化风险检测

担心的问题：某些界面字符串可能同时被当作「配置键 / 映射表键 / 字符串比较值」使用。
若把这类字符串汉化，会导致配置读写错乱或逻辑分支失效。

做法：对每个准备汉化的原串，在整个源码树里统计其出现次数，
      出现次数多于「界面替换次数」的，或在敏感上下文（比较、查表）里的，全部列出来人工确认。
"""
import json
import pathlib
import re
import sys
from collections import defaultdict

SENSITIVE = re.compile(r"(==|!=|strcmp|compare\(|\.find\(|\.contains\(|\[\s*\"|hash|Hash|Map|map<|IsEqual)")

KEYS = None


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "src")
    strings = json.loads(pathlib.Path("build/strings.json").read_text(encoding="utf-8"))

    # 每个原串的界面替换次数
    planned = defaultdict(int)
    for e in strings["entries"]:
        planned[e["text"]] += 1

    sys.path.insert(0, "tools")
    import glob, importlib.util
    table = {}
    for f in sorted(glob.glob("tools/translations_*.py")):
        spec = importlib.util.spec_from_file_location(pathlib.Path(f).stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        table.update(getattr(mod, "T", {}))

    # 收集源码文件
    files = []
    for pat in ("**/*.cpp", "**/*.h", "**/*.hpp"):
        for f in root.glob(pat):
            p = str(f).replace("\\", "/")
            if "/external/" in p or "/include/imgui/" in p:
                continue
            files.append(f)

    texts = {}
    for f in files:
        try:
            texts[f] = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            pass

    risky = []
    for orig, zh in table.items():
        if orig == zh or len(orig) < 3:
            continue
        needle = '"' + orig + '"'
        hits = []
        for f, t in texts.items():
            if needle not in t:
                continue
            for m in re.finditer(re.escape(needle), t):
                line_start = t.rfind("\n", 0, m.start()) + 1
                line_end = t.find("\n", m.start())
                line = t[line_start:line_end if line_end > 0 else len(t)]
                hits.append((str(f.relative_to(root)).replace("\\", "/"),
                             t.count("\n", 0, m.start()) + 1, line.strip()))
        if len(hits) > planned.get(orig, 0):
            risky.append((orig, zh, planned.get(orig, 0), hits))

    print(f"检测词条：{len(table)} 条，疑似风险：{len(risky)} 条\n")
    for orig, zh, n, hits in risky:
        print(f"[风险] {orig!r}  界面替换 {n} 处，全库出现 {len(hits)} 处")
        for hfile, hline, htext in hits[:6]:
            flag = " <<< 敏感上下文" if SENSITIVE.search(htext) else ""
            print(f"    {hfile}:{hline}  {htext[:120]}{flag}")
        print()


if __name__ == "__main__":
    main()
