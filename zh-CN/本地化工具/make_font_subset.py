#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文字体子集生成器

思路：OptiScaler 界面里出现的汉字是有限的（约 700 个），没必要内嵌整套中文字体。
      - 扫描汉化后的源码，收集实际用到的所有非 ASCII 字符
      - 用 pyftsubset 从 Noto Sans SC 中裁出这些字形
      - 生成 C++ 头文件（原始字节数组 + 精确字符集码表），随 DLL 一起编译

为什么用原始数组而不是 base85 压缩：ImGui 的 AddFontFromMemoryCompressedTTF 用的是
stb_compress 私有格式，无法在 Python 侧可靠复现；而 ImGui 另有 AddFontFromMemoryTTF
可直接吃原始 TTF 字节，仓库里 Hack.h 也是同样做法，稳妥。
"""
import json
import pathlib
import re
import subprocess
import sys

PY = sys.executable
TOOLS = pathlib.Path(__file__).resolve().parent


def find_root(start: pathlib.Path) -> pathlib.Path:
    """
    找到源码根目录（含 OptiScaler/menu 的那一层）。

    这个脚本既会在本地开发目录 <项目>/tools/ 下运行，也会随源码包分发在
    <源码根>/zh-CN/本地化工具/ 下运行，两种布局的层级不同，所以要自动探测。
    """
    for p in [start, *start.parents]:
        if (p / "OptiScaler" / "menu").is_dir():
            return p
        if (p / "src" / "OptiScaler" / "menu").is_dir():
            return p / "src"
    return start


PROJ = find_root(TOOLS)
# 中间产物目录（变量字体、子集字体）。放在工具目录旁边，两种布局下都可写。
WORK = TOOLS.parent / "build"

# 除界面用字外，额外保底字符（中文标点与常用符号，避免以后改文案缺字）
EXTRA = "，。、：；！？（）【】《》“”‘’…—·～％＃＆＋－×÷°±§½¼¾①②③④⑤⑥⑦⑧⑨⑩㎡μΩ→←↑↓↔"


def collect_chars(root):
    chars = set()
    for pat in ("**/*.cpp", "**/*.h", "**/*.hpp"):
        for f in root.glob(pat):
            p = str(f).replace("\\", "/")
            if "/external/" in p or "/include/imgui/" in p or "/menu/font/" in p:
                continue
            try:
                txt = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for ch in txt:
                if ord(ch) > 127:
                    chars.add(ch)
    chars.update(EXTRA)
    return chars


def main():
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else PROJ
    font_in = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else WORK / "noto_var.ttf"
    out_h = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else src / "OptiScaler" / "menu" / "font" / "NotoSansSC_Subset.h"
    work = WORK

    chars = collect_chars(src)
    cjk = sorted(c for c in chars if ord(c) > 0x2000)
    print(f"收集到非 ASCII 字符 {len(chars)} 个（其中 CJK/标点 {len(cjk)} 个）")
    print("示例:", "".join(cjk[:40]))

    # 码点集合：ASCII 可见字符 + 用到的非 ASCII
    codes = [f"U+{c:04X}" for c in sorted(ord(x) for x in chars)]
    codes += ["U+0020-007E"]
    unicodes = ",".join(codes)

    # 1) 变量字体先固定到 Regular（wght=400），否则 FreeType 渲染的是默认实例，可能与预期不符
    static_ttf = work / "NotoSansSC-Regular-static.ttf"
    r = subprocess.run([PY, "-m", "fontTools.varLib.instancer", str(font_in),
                        "wght=400", "-o", str(static_ttf)], capture_output=True, text=True)
    if r.returncode != 0:
        print("instancer 失败，改用原字体：", r.stderr[-400:])
        static_ttf = font_in

    # 2) 子集化
    subset = work / "NotoSansSC-Subset.ttf"
    cmd = [PY, "-m", "fontTools.subset", str(static_ttf),
           f"--unicodes={unicodes}",
           "--layout-features=", "--glyph-names", "--symbol-cmap", "--legacy-cmap",
           "--notdef-glyph", "--notdef-outline", "--recommended-glyphs",
           "--name-IDs=*", "--name-legacy", "--name-languages=*",
           f"--output-file={subset}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("subset 失败:", r.stderr[-800:])
        sys.exit(1)
    data = subset.read_bytes()
    print(f"子集字体大小：{len(data)} 字节（原字体 {font_in.stat().st_size} 字节）")

    # 3) 生成头文件
    lines = ["#pragma once", "",
             "// Noto Sans SC 子集（仅含 OptiScaler 界面实际用到的字形）",
             "// 来源：https://github.com/notofonts/noto-cjk",
             "// 许可：SIL Open Font License 1.1（允许随软件一同分发）",
             f"// 字形数：{len(chars)}  文件大小：{len(data)} 字节",
             "",
             f"static const unsigned int noto_sc_font_size = {len(data)};",
             "",
             "static const unsigned char noto_sc_font[] = {"]
    row = []
    for i, b in enumerate(data):
        row.append(f"0x{b:02x}")
        if len(row) == 16:
            lines.append("    " + ", ".join(row) + ",")
            row = []
    if row:
        lines.append("    " + ", ".join(row) + ",")
    lines.append("};")
    lines.append("")

    # 精确码表：ImWchar 为 16 位，按 [起, 止] 成对书写，以 0 结束
    cps = sorted(set(ord(c) for c in chars) | set(range(0x20, 0x7F)))
    ranges = []
    start = prev = cps[0]
    for c in cps[1:]:
        if c == prev + 1:
            prev = c
            continue
        ranges.append((start, prev))
        start = prev = c
    ranges.append((start, prev))
    lines.append(f"// 覆盖 {len(cps)} 个码位，共 {len(ranges)} 个连续区间")
    lines.append("static const unsigned short noto_sc_glyph_ranges[] = {")
    body = []
    for a, b in ranges:
        body.append(f"0x{a:04x}, 0x{b:04x},")
    for i in range(0, len(body), 6):
        lines.append("    " + " ".join(body[i:i + 6]))
    lines.append("    0x0000")
    lines.append("};")
    lines.append("")

    out_h.write_text("\n".join(lines), encoding="utf-8")
    print("已生成:", out_h, f"({out_h.stat().st_size} 字节源码)")
    print(f"码位区间 {len(ranges)} 个，最大码位 0x{max(cps):04X}")


if __name__ == "__main__":
    main()
