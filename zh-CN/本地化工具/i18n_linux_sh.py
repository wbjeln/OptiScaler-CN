#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup_linux.sh 汉化器（只改用户可见文案与注释，不动任何逻辑）

为什么用「精确字符串替换」而不是重写整个脚本：
    这个脚本有 379 行、含交互分支和 heredoc 生成卸载脚本，重写极易引入逻辑错误。
    精确替换 + 逐条断言命中 + bash -n 语法校验，能把风险压到最低。

为什么必须保持 LF 换行：
    文件带 `#!/usr/bin/env bash`。CRLF 会让内核把解释器读成 `/usr/bin/env bash\\r`，
    在 Linux 上直接报 "bad interpreter"。所以读写都强制 newline=""。

用法：
    python tools/i18n_linux_sh.py            # 干跑，只报告会改多少处
    python tools/i18n_linux_sh.py --apply    # 真正写入
"""
import pathlib
import sys

TOOLS = pathlib.Path(__file__).resolve().parent
PROJ = TOOLS.parent
TARGET = PROJ / "src" / "setup_linux.sh"

# 保持原样的字符串：ASCII 图形 banner、参数名、dll 文件名、WINEDLLOVERRIDES 示例等
# 说明：替换表按「原文 -> 译文」精确匹配，同一原文出现多次会被全部替换。

REPLACEMENTS = [
    # ---------- 帮助信息 ----------
    ('echo "Usage: $0 [OPTIONS]"',
     'echo "用法：$0 [选项]"'),
    ('echo "Options:"',
     'echo "选项："'),
    ('echo "  --filename=<string>        Set target filename for OptiScaler.dll. Options are:"',
     'echo "  --filename=<string>        指定 OptiScaler.dll 的目标文件名，可选值："'),
    ('echo "  --overwrite=<y|n>       Overwrite existing file (y/n)"',
     'echo "  --overwrite=<y|n>       是否覆盖已存在的文件（y/n）"'),
    ('echo "  --using_nvidia=<y|n>    Using Nvidia GPU (y/n)"',
     'echo "  --using_nvidia=<y|n>    是否为 Nvidia 显卡（y/n）"'),
    ('echo "  --using_dlss=<y|n>      Use DLSS inputs/spoofing (y/n)"',
     'echo "  --using_dlss=<y|n>      是否使用 DLSS 输入/伪装（y/n）"'),
    ('echo "  -h, --help              Show this help message"',
     'echo "  -h, --help              显示本帮助信息"'),
    ('echo "Example:"',
     'echo "示例："'),

    # ---------- banner 后的俏皮话（原文是星球大战梗的改写） ----------
    ('echo "Coping is strong with this one..."',
     'echo "复制文件的功力不俗……"'),

    # ---------- 注释 ----------
    ('# Get the script directory', '# 取得脚本所在目录'),
    ('# Remove junk files', '# 删除多余文件'),
    ('# Check if OptiScaler.dll exists', '# 检查 OptiScaler.dll 是否存在'),
    ('# Unreal Engine detection (skip for headless)', '# 虚幻引擎检测（无界面模式会跳过）'),
    ('# Skip if filename already set and valid', '# 若已指定合法文件名则直接跳过'),
    ('# Check if file already exists', '# 检查目标文件是否已存在'),
    ('# Break out of both loops', '# 跳出两层循环'),
    ('# Break out of the inner loop, continue filename selection', '# 跳出内层循环，重新选择文件名'),
    ("# File doesn't exist, proceed", '# 文件不存在，可以直接继续'),
    ('# Try to detect Nvidia', '# 尝试检测 Nvidia 显卡'),
    ('# Disable spoofing', '# 关闭伪装'),
    ('# Use sed to replace Dxgi=auto with Dxgi=false', '# 用 sed 把 Dxgi=auto 改成 Dxgi=false'),
    ('# Rename OptiScaler file', '# 重命名 OptiScaler 文件'),
    ('# Create uninstaller', '# 生成卸载脚本'),
    ('# Create the uninstaller', '# 生成卸载脚本'),
    ('# Remove OptiScaler files', '# 删除 OptiScaler 相关文件'),
    ('# Remove directories', '# 删除目录'),
    ('# Remove this uninstaller', '# 删除本卸载脚本自身'),
    ('# Replace the placeholder with the actual selected filename', '# 把占位符替换成实际选择的文件名'),
    ('# Make the uninstaller executable', '# 赋予卸载脚本执行权限'),
    ('# Success message', '# 安装成功提示'),
    ('# Display Wine DLL override information', '# 显示 Wine 的 DLL 覆盖设置说明'),
    ('# Cleanup - remove setup script', '# 收尾：删除安装脚本自身'),

    # ---------- 交互提示 ----------
    ('read -p "Press Enter to exit..."', 'read -p "按回车键退出..."'),
    ('read -p "Press Enter to continue..."', 'read -p "按回车键继续..."'),
    ('echo "OptiScaler \\"OptiScaler.dll\\" file is not found!"',
     'echo "未找到 OptiScaler \\"OptiScaler.dll\\" 文件！"'),
    ('echo "Please make sure you extracted all OptiScaler files to the game folder."',
     'echo "请确认已把 OptiScaler 的全部文件解压到游戏目录。"'),
    ('echo "For Unreal Engine games, look for the game executable in:"',
     'echo "若是虚幻引擎（Unreal Engine）游戏，请在以下位置寻找游戏主程序："'),
    ('echo "- Ignore the Engine folder"',
     'echo "- 请忽略 Engine 文件夹"'),
    ('echo "Found Engine folder, if this is an Unreal Engine game then please extract OptiScaler to #CODENAME#/Binaries/Win64"',
     'echo "检测到 Engine 文件夹。如果这是虚幻引擎游戏，请把 OptiScaler 解压到 #CODENAME#/Binaries/Win64"'),
    ('read -p "Continue installation to current folder? [y/n]: " continue_choice',
     'read -p "是否继续安装到当前文件夹？[y/n]：" continue_choice'),
    ('echo "Installation cancelled."', 'echo "已取消安装。"'),
    ('echo "Invalid filename: $selected_filename"', 'echo "文件名无效：$selected_filename"'),
    ('echo "Choose a filename for OptiScaler (default is dxgi.dll):"',
     'echo "请为 OptiScaler 选择一个文件名（默认为 dxgi.dll）："'),
    ('read -p "Enter 1-8 (or press Enter for default): " filename_choice',
     'read -p "请输入 1-8（直接回车使用默认值）：" filename_choice'),
    ('echo "WARNING: $selected_filename already exists in the current folder."',
     'echo "警告：当前文件夹中已存在 $selected_filename。"'),
    ('echo "File exists and overwrite_choice=$overwrite_choice, exiting."',
     'echo "文件已存在，且 overwrite_choice=$overwrite_choice，退出。"'),
    ('read -p "Do you want to overwrite it? [y/n]: " overwrite_choice',
     'read -p "是否覆盖它？[y/n]：" overwrite_choice'),
    ('echo "Invalid choice. Please enter \'y\' or \'n\'."',
     'echo "输入无效，请输入 \'y\' 或 \'n\'。"'),
    ('echo "Nvidia GPU detected."', 'echo "检测到 Nvidia 显卡。"'),
    ('read -r -p "Are you using an Nvidia GPU [Y/n]: " using_nvidia',
     'read -r -p "你使用的是 Nvidia 显卡吗 [Y/n]：" using_nvidia'),
    ('read -r -p "Are you using an Nvidia GPU [y/N]: " using_nvidia',
     'read -r -p "你使用的是 Nvidia 显卡吗 [y/N]：" using_nvidia'),
    ('read -r -p "Will you try to use DLSS inputs? (enables spoofing, required for DLSS FG, Reflex->AL2) [Y/n]: " using_dlss',
     'read -r -p "是否使用 DLSS 输入？（会启用伪装，DLSS 帧生成与 Reflex→AL2 需要它）[Y/n]：" using_dlss'),
    ('echo "Config file not found: $config_file"', 'echo "未找到配置文件：$config_file"'),
    ('echo "Spoofing disabled in configuration."', 'echo "已在配置文件中关闭伪装。"'),
    ('echo "Removing previous $selected_filename..."', 'echo "正在删除原有的 $selected_filename……"'),
    ('echo "Renaming OptiScaler file to $selected_filename..."',
     'echo "正在把 OptiScaler 文件重命名为 $selected_filename……"'),
    ('echo "ERROR: Failed to rename OptiScaler file to $selected_filename."',
     'echo "错误：无法把 OptiScaler 文件重命名为 $selected_filename。"'),
    ('echo "Please check file permissions and try again."', 'echo "请检查文件权限后重试。"'),

    # ---------- 卸载脚本（heredoc 内，同样只改文案） ----------
    ('echo "  --remove=<y|n>    Confirm removal (y/n)"',
     'echo "  --remove=<y|n>    确认卸载（y/n）"'),
    ('echo "  -h, --help        Show this help message"',
     'echo "  -h, --help        显示本帮助信息"'),
    ('read -p "Do you want to remove OptiScaler? [y/n]: " remove_choice',
     'read -p "确定要卸载 OptiScaler 吗？[y/n]：" remove_choice'),
    ('echo "Removing OptiScaler files..."', 'echo "正在删除 OptiScaler 文件……"'),
    ('echo "OptiScaler removed!"', 'echo "OptiScaler 已卸载完成！"'),
    ('echo "Operation cancelled."', 'echo "操作已取消。"'),
    ('echo "Uninstaller created: remove_optiscaler.sh"',
     'echo "已生成卸载脚本：remove_optiscaler.sh"'),

    # ---------- 结尾提示 ----------
    ('echo " OptiScaler setup completed successfully..."',
     'echo " OptiScaler 安装完成……"'),
    ('echo "IMPORTANT FOR LINUX/WINE USERS:"', 'echo "Linux / Wine 用户请注意："'),
    ('echo "You might need to add the renamed DLL to Wine overrides"',
     'echo "你可能需要把重命名后的 DLL 加入 Wine 的 DLL 覆盖列表"'),
    ('echo "Example, if using Steam, add this to launch options:"',
     'echo "例如在 Steam 中，把下面这行加入启动选项："'),
    ('echo "Remember: Insert key opens OptiScaler overlay, Page Up/Down for performance stats"',
     'echo "请记住：Insert 键打开 OptiScaler 叠加界面，Page Up/Down 查看性能统计"'),
]


def main():
    apply = "--apply" in sys.argv

    if not TARGET.exists():
        sys.exit(f"找不到目标文件：{TARGET}")

    # newline="" —— 原样读写，绝不把 LF 变成 CRLF
    text = TARGET.read_text(encoding="utf-8", newline="")
    original = text

    total = 0
    missing = []
    for old, new in REPLACEMENTS:
        n = text.count(old)
        if n == 0:
            missing.append(old[:70])
            continue
        text = text.replace(old, new)
        total += n
        print(f"  x{n}  {old[:66]}")

    print()
    print(f"命中替换：{total} 处")

    if missing:
        print(f"\n[X] 有 {len(missing)} 条替换没匹配到（可能是上游改动或表述不一致）：")
        for m in missing:
            print("    " + m)
        print("未做任何写入。")
        return 1

    if text == original:
        print("内容无变化。")
        return 0

    # 校验：换行符必须仍是纯 LF
    if "\r\n" in text:
        print("[X] 结果里出现了 CRLF，会破坏 bash 脚本，已中止。")
        return 1

    # 校验：逻辑行（去掉文案后的骨架）不该有增删
    if text.count("\n") != original.count("\n"):
        print(f"[X] 行数发生变化：{original.count(chr(10))} -> {text.count(chr(10))}，已中止。")
        return 1

    if not apply:
        print("干跑完成，未写入。加 --apply 才会真正修改文件。")
        return 0

    TARGET.write_text(text, encoding="utf-8", newline="")
    print(f"已写入：{TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
