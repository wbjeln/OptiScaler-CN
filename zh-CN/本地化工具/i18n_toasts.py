#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汉化「游戏内提示弹窗」（ImGuiToast / InsertNotification / setTitle / setContent）。

为什么需要单独做这件事：
    界面文案汉化只覆盖了 menu_common.cpp / dllmain.cpp，但 OptiScaler 还会在运行时用
    ImGui::InsertNotification(...) 弹提示（帧生成初始化失败、回退到某个超分方案、
    缺少 DLL 等）。这些玩家同样能看到，却分散在 hooks/ inputs/ upscalers/ proxies/
    等十来个文件里，很容易漏掉。

做法：精确字符串替换 + 逐条断言命中，不做正则批量替换，
      以免误伤同一文件里的 LOG_* 日志文案（那些不属于界面汉化范围）。

写法说明：表里只存「字面量内部文本」，替换时再补回两侧双引号。
    这样就不必在 Python 源码里同时处理 C++ 的双引号和英文里的撇号
    （写成 r'"Can't ..."' 会因为撇号提前终止字符串）。

用法：
    python tools/i18n_toasts.py            # 干跑
    python tools/i18n_toasts.py --apply    # 写入
"""
import pathlib
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
PROJ = TOOLS.parent
SRC = PROJ / "src"

# 键 = 原文（不含两侧双引号），值 = 译文（不含两侧双引号）。
# 源码里的 \n 是「反斜杠 + n」两个字面字符，所以用 r"" 原始字符串书写；
# {} / {0} 等占位符必须原样保留。
TABLE = {
    # ---- 帧生成初始化失败（hooks/FG_Hooks.cpp）----
    r"Can't init FSR FG\nAre you missing the required DLLs?":
        r"无法初始化 FSR 帧生成\n是不是缺少所需的 DLL？",
    r"Can't init XeFG\nAre you missing the required DLLs?":
        r"无法初始化 XeFG\n是不是缺少所需的 DLL？",
    r"Can't init DLSSG Output\nAre you missing the streamline folder?":
        r"无法初始化 DLSSG 输出\n是不是缺少 streamline 文件夹？",

    # ---- RTSS 冲突提醒（hooks/Reflex_Hooks.cpp）----
    r"RTSS + XeFG detected":
        r"检测到 RTSS + XeFG",
    r"RTSS Reflex Injection is known to cause issues.\nEspecially when using XeFG.\nPlease disable it.":
        r"RTSS 的 Reflex 注入已知会引发问题，\n使用 XeFG 时尤其明显，\n请把它关掉。",

    # ---- 超分运行失败 / 回退提示 ----
    r"Upscaler failed to run!":
        r"超分运行失败！",
    r"Falling back to FSR 2.1.2":
        r"回退到 FSR 2.1.2",
    r"Falling back to FSR 2.2":
        r"回退到 FSR 2.2",
    r"Falling back to XeSS":
        r"回退到 XeSS",

    # ---- 缺少第三方 DLL ----
    r"Can't load amd_fidelityfx_dx12\nDid you forget to extract that dll?":
        r"无法加载 amd_fidelityfx_dx12\n是不是忘了解压这个 dll？",
    r"Couldn't load libxess.dll\nCheck if the dll is present":
        r"无法加载 libxess.dll\n请确认该 dll 是否存在",
    r"Couldn't load libxess_dx11.dll\nCheck if the dll is present":
        r"无法加载 libxess_dx11.dll\n请确认该 dll 是否存在",
    r"Couldn't create XeSS context\n{}":
        r"无法创建 XeSS 上下文\n{}",

    # ---- 其它 ----
    r"Error while compiling a shader!":
        r"着色器编译失败！",
    r"Failed to create a shared texture\nMake sure you are using at least Wine/Proton 11":
        r"创建共享纹理失败\n请确认至少使用 Wine/Proton 11",
    r"{} is not available.\nFalling back to {}.":
        r"{} 不可用。\n回退到 {}。",
    r"{} is not available and can't fallback":
        r"{} 不可用，且无法回退",
}

SKIP_DIRS = ("/external/", "/include/")


def main():
    apply = "--apply" in sys.argv
    total = 0
    touched = []
    skipped = []
    done, pending = set(), set()

    for f in sorted(SRC.rglob("*.cpp")) + sorted(SRC.rglob("*.h")):
        p = str(f).replace("\\", "/")
        if any(d in p for d in SKIP_DIRS):
            continue
        try:
            text = f.read_text(encoding="utf-8", newline="")
        except UnicodeDecodeError:
            # 上游有个别文件不是 UTF-8。既然解不出文本，就不可能含目标文案。
            skipped.append(str(f.relative_to(SRC)))
            continue

        orig = text
        for old, new in TABLE.items():
            quoted_old, quoted_new = f'"{old}"', f'"{new}"'
            n = text.count(quoted_old)
            if n:
                text = text.replace(quoted_old, quoted_new)
                total += n
                pending.add(old)
                print(f"  x{n}  {f.relative_to(SRC)}  {old[:56]}")
            elif quoted_new in text:
                # 已经是译文了：这一条之前处理过，不算失败
                done.add(old)

        if text != orig:
            touched.append(f)
            if apply:
                f.write_text(text, encoding="utf-8", newline="")

    print(f"\n本次新替换 {total} 处，涉及 {len(touched)} 个文件")
    if skipped:
        print(f"（跳过 {len(skipped)} 个非 UTF-8 文件：{'、'.join(skipped)}）")

    unknown = [o for o in TABLE if o not in pending and o not in done]
    if unknown:
        print(f"\n[X] 有 {len(unknown)} 条既找不到原文、也找不到译文（可能被拆成多段字面量）：")
        for m in unknown:
            print("    " + m)
        return 1

    already = len(done - pending)
    if already:
        print(f"其中 {already} 条此前已汉化，无需重复处理")
    print("全部弹窗文案均已汉化。")
    if not apply and total:
        print("（干跑模式，未写入。加 --apply 才真正修改。）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
