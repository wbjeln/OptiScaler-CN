#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OptiScaler 汉化回写器

策略：
  1. 载入 tools/translations_*.py 词条（键=源码原始字面量，值=中文逻辑文本）
  2. 读取 build/strings.json 获取每个字面量的精确偏移与分段信息
  3. 解析译文：
       - 整串命中词条表 → 直接用
       - 未命中但由多个相邻段拼成，且每一段都能命中 → 自动拼接（中文无需保留源码里的换行缩进）
       - 其他情况保持英文
  4. 按偏移从后往前写入：译文放到第一段，其余段置空，保证 C++ 拼接结果正确
  5. 写入前校验占位符 / ##ID / 转义引号 / %% 一致性
"""
import argparse
import glob
import importlib.util
import json
import pathlib
import re
from collections import defaultdict

TOOLS = pathlib.Path(__file__).resolve().parent
PROJ = TOOLS.parent

SPEC_RE = re.compile(r"%(?:%|[-+ #0]*\d*(?:\.\d+)?(?:ll|l|h)?[diufxXeEgGscp])|\{[^}]*\}")
ID_RE = re.compile(r"###?[^\s#]+")


def load_translations():
    table, override = {}, defaultdict(dict)
    for f in sorted(glob.glob(str(TOOLS / "translations_*.py"))):
        spec = importlib.util.spec_from_file_location(pathlib.Path(f).stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        table.update(getattr(mod, "T", {}))
        for k, v in getattr(mod, "OVERRIDE", {}).items():
            override[k].update(v)
    return table, override


def c_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")


def validate(orig, zh):
    errs = []
    if not zh.strip():
        return ["译文为空"]
    if sorted(SPEC_RE.findall(orig)) != sorted(SPEC_RE.findall(zh)):
        errs.append(f"占位符不一致 {SPEC_RE.findall(orig)} -> {SPEC_RE.findall(zh)}")
    if ID_RE.findall(orig) != ID_RE.findall(zh):
        errs.append(f"##ID 不一致 {ID_RE.findall(orig)} -> {ID_RE.findall(zh)}")
    if orig.count('\\"') != c_escape(zh).count('\\"'):
        errs.append("转义引号数量不一致")
    if orig.count("%%") != zh.count("%%"):
        errs.append("%% 数量不一致")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(PROJ / "src"))
    ap.add_argument("--strings", default=str(PROJ / "build" / "strings.json"))
    ap.add_argument("--report", default=str(PROJ / "build" / "apply_report.txt"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    data = json.loads(pathlib.Path(args.strings).read_text(encoding="utf-8"))
    table, override = load_translations()
    print(f"词条表：{len(table)} 条，词条实例：{data['total']} 处")

    # 先读入所有涉及的文件（保持原始内容，用于分段取文本）
    files = sorted(set(e["file"] for e in data["entries"]))
    texts = {}
    for rel in files:
        fp = root / rel
        if fp.exists():
            texts[rel] = fp.read_text(encoding="utf-8")

    plan = defaultdict(list)
    used, partial, failed, untranslated = set(), [], [], defaultdict(int)
    direct_n = merged_n = 0

    for e in data["entries"]:
        orig = e["text"]
        t = texts.get(e["file"])
        if t is None:
            continue
        zh = override.get((e["file"], e["line"]), {}).get(orig, table.get(orig))
        how = "direct" if zh else None
        if not zh and len(e["parts"]) > 1:
            segs = [t[a:b] for a, b in e["parts"]]
            hits = [table.get(s) for s in segs]
            if all(hits):
                zh = "".join(hits)
                how = "merged"
            elif any(hits):
                partial.append((e, segs))
        if not zh:
            untranslated[e["file"]] += 1
            continue
        # 自动补回 ##ID
        ids = ID_RE.findall(orig)
        if ids and not ID_RE.findall(zh):
            zh = zh + "".join(ids)
        errs = validate(orig, zh)
        if errs:
            failed.append((e, errs))
            continue
        parts = e["parts"]
        edits = [(parts[0][0], parts[0][1], c_escape(zh))]
        edits += [(p[0], p[1], "") for p in parts[1:]]
        plan[e["file"]].append((edits, orig, zh))
        used.add(orig)
        if how == "direct":
            direct_n += 1
        else:
            merged_n += 1

    total = 0
    for rel, items in plan.items():
        text = texts[rel]
        flat = [ed for it in items for ed in it[0]]
        for (s, en, esc) in sorted(flat, key=lambda x: -x[0]):
            text = text[:s] + esc + text[en:]
        total += len(flat)
        if not args.dry_run:
            (root / rel).write_text(text, encoding="utf-8")

    lines = [f"写入替换：{total} 处（直接命中 {direct_n}，分段合并 {merged_n}）",
             f"涉及文件：{', '.join(f'{k}({len(v)})' for k, v in plan.items())}",
             "", f"未收录（保持英文）：{sum(untranslated.values())} 处"]
    for k, v in sorted(untranslated.items(), key=lambda kv: -kv[1]):
        lines.append(f"  {v:5d}  {k}")
    lines += ["", f"分段部分命中（需人工补译）：{len(partial)}"]
    for e, segs in partial[:40]:
        done = [s for s in segs if s in table]
        miss = [s for s in segs if s not in table]
        lines.append(f"  {e['file']}:{e['line']} 已译{len(done)}/共{len(segs)}  待译={miss}")
    lines += ["", f"校验失败（保持英文）：{len(failed)}"]
    for e, errs in failed:
        lines.append(f"  {e['file']}:{e['line']} {e['text'][:60]!r} -> {'; '.join(errs)}")
    lines += ["", f"词条表中未被使用：{len(set(table) - used)}"]
    for u in sorted(set(table) - used):
        lines.append(f"  {u!r}")

    report = "\n".join(lines)
    pathlib.Path(args.report).write_text(report, encoding="utf-8")
    print(report[:2500])


if __name__ == "__main__":
    main()
