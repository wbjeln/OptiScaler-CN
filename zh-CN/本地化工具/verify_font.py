#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字形覆盖校验：确认 NotoSansSC_Subset.h 覆盖了源码里出现的全部非 ASCII 字符。

为什么需要这个检查：
    字体子集是按「当时源码用到的汉字」裁出来的。之后只要再改文案（哪怕只多一个
    汉字），子集就可能缺字形，界面上会出现方块（tofu）。这个脚本把「收集字符」
    和「解析码表」对齐比较，缺字直接列出来。

用法：
    python tools/verify_font.py [源码目录] [头文件路径]
"""
import pathlib
import re
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from make_font_subset import collect_chars  # noqa: E402  （复用同一套收集逻辑）


def find_root(start: pathlib.Path) -> pathlib.Path:
    """
    向上查找仓库根目录。

    这个脚本随源码包一起分发在 zh-CN/本地化工具/ 下，此时 `父目录的父目录`
    并不是源码根目录；靠「是否存在 OptiScaler/menu」来判断才可靠。
    两种布局都要支持：
      · 本地开发：<项目>/tools/ 与 <项目>/src/OptiScaler/...（需往下找一层 src）
      · 源码包内：<源码根>/zh-CN/本地化工具/ 与 <源码根>/OptiScaler/...
    """
    for p in [start, *start.parents]:
        if (p / "OptiScaler" / "menu").is_dir():
            return p
        if (p / "src" / "OptiScaler" / "menu").is_dir():
            return p / "src"
    return start


PROJ = find_root(TOOLS)
HDR = PROJ / "OptiScaler" / "menu" / "font" / "NotoSansSC_Subset.h"


def parse_ranges(path: pathlib.Path) -> set:
    """从生成的 C++ 头文件里解析码表，展开成码点集合。"""
    txt = path.read_text(encoding="utf-8")
    m = re.search(r"noto_sc_glyph_ranges\[\]\s*=\s*\{(.*?)\};", txt, re.S)
    if not m:
        raise SystemExit(f"在 {path} 里找不到 noto_sc_glyph_ranges 数组")
    nums = [int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]+)", m.group(1))]
    if nums and nums[-1] == 0:
        nums = nums[:-1]
    if len(nums) % 2 != 0:
        raise SystemExit("码表不是成对的 [起, 止]，文件可能损坏")

    covered = set()
    for i in range(0, len(nums), 2):
        covered.update(range(nums[i], nums[i + 1] + 1))
    return covered


def main():
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else PROJ
    hdr = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else HDR

    needed = collect_chars(src)
    covered = parse_ranges(hdr)

    missing = sorted(c for c in needed if ord(c) not in covered)
    print(f"源码非 ASCII 字符：{len(needed)}")
    print(f"头文件覆盖码位：{len(covered)}")
    print(f"头文件大小：{hdr.stat().st_size} 字节")

    if missing:
        print(f"\n[X] 缺少 {len(missing)} 个字形，界面会显示成方块：")
        print("    " + "".join(missing))
        print("\n请重新运行 tools/make_font_subset.py 生成字体子集。")
        return 1

    print("\n[OK] 字形覆盖完整，没有缺字。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
