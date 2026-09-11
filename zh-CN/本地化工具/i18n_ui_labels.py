#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补齐「界面控件标签」的汉化（菜单里仍显示英文的那几个）。

背景：界面文案汉化漏掉了几类容易被忽略的写法——
    · ImGui 的 "显示文本##ID" 形式：只看到 ##ID 会觉得是内部标识，
      其实 ## 前面那截（如 "Active"）是会被玩家看到的；
    · std::format / StrFmt 拼出来的短标签，如 "ON {}x"；
    · 颜色选择器的标签 "Custom Accent Color"；
    · 半角冒号与全角冒号混用（"libxess: %s" vs "nvngx_dll ：%s"）。

先用 tools/find_ui_strings.py 列出全部英文控件标签，再用本脚本按表修正。
表里只放「字面量内部文本」，替换时补回双引号。

用法：
    python tools/i18n_ui_labels.py            # 干跑
    python tools/i18n_ui_labels.py --apply    # 写入
"""
import pathlib
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
SRC = TOOLS.parent / "src"

TABLE = {
    # ImGui 的 "显示文本##ID"：## 之后是控件 ID，必须原样保留
    "Active##2": "已启用##2",
    "Active##3": "已启用##3",
    "Active##4": "已启用##4",

    # std::format 拼出来的短标签
    "ON {}x": "开启 {}x",

    # 颜色选择器
    "Custom Accent Color": "自定义强调色",
    "Custom BG Colour": "自定义背景色",

    # 统计行里的可见英文词
    "%08x, %s->%s, Count: %llu, %s": "%08x, %s->%s, 计数：%llu, %s",
    "FGId: %llu, RfxId: %llu": "帧生成Id：%llu, ReflexId：%llu",

    # 统一成全角冒号，并与其它条目的写法保持一致（产品名保留英文）
    "libxess: %s": "libxess：%s",
    "FSR 3.1: %s": "FSR 3.1：%s",
    "FSR 3.1 SR: %s": "FSR 3.1 超分：%s",
    "FSR 3.1 FG: %s": "FSR 3.1 帧生成：%s",
}


def main():
    apply = "--apply" in sys.argv
    f = SRC / "OptiScaler" / "menu" / "menu_common.cpp"
    text = f.read_text(encoding="utf-8", newline="")
    orig = text
    total = 0
    done, pending = set(), set()

    for old, new in TABLE.items():
        q_old, q_new = f'"{old}"', f'"{new}"'
        n = text.count(q_old)
        if n:
            text = text.replace(q_old, q_new)
            pending.add(old)
            total += n
            print(f"  x{n}  {old}  ->  {new}")
        elif q_new in text:
            done.add(old)

    print(f"\n本次新替换 {total} 处")
    unknown = [o for o in TABLE if o not in pending and o not in done]
    if unknown:
        print("[X] 既无原文也无译文：")
        for u in unknown:
            print("    " + u)
        return 1
    if done - pending:
        print(f"其中 {len(done - pending)} 条此前已处理")

    if total and apply:
        if text.count("\n") != orig.count("\n"):
            print("[X] 行数发生变化，已中止")
            return 1
        f.write_text(text, encoding="utf-8", newline="")
        print(f"已写入：{f.relative_to(SRC)}")
    elif total:
        print("（干跑模式，未写入。加 --apply 才真正修改。）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
