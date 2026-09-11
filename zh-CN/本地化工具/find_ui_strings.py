#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确找出「界面控件标签」里还没汉化的英文文案。

三个关键点，缺一不可：
  1) 按括号配平取出控件调用内部的字面量——只取第 1 个（即标签），
     这样不会把同文件里的 LOG_* 日志文案算进来。
  2) 用词法扫描生成「注释位置掩码」，排除被注释掉的代码
     （例如 `// ImGui::Checkbox("Only Generated##2", ...)` 不是界面文案）。
  3) 控件名单要全，否则会漏：Slider / Combo / TreeNode / TabItem / SeparatorText
     等同样带标签。

注意：ImGui 用 "显示文本##ID" 把显示文本与控件 ID 分开，
     所以 "Active##2" 里会被玩家看到的是 Active，翻译时要保留 ##ID。
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent / "src"

WIDGETS = (
    # 文本类
    "ImGui::TextUnformatted", "ImGui::TextWrapped", "ImGui::TextDisabled",
    "ImGui::BulletText", "ImGui::Text", "ImGui::LabelText",
    # 按钮/选择类
    "ImGui::Checkbox", "ImGui::Button", "ImGui::SmallButton", "ImGui::InvisibleButton",
    "ImGui::Selectable", "ImGui::MenuItem", "ImGui::BeginMenu", "ImGui::RadioButton",
    "ImGui::CollapsingHeader", "ImGui::TreeNode", "ImGui::TreeNodeEx",
    # 输入类
    "ImGui::Combo", "ImGui::BeginCombo", "ImGui::InputText", "ImGui::InputTextWithHint",
    "ImGui::InputFloat", "ImGui::InputInt", "ImGui::SliderFloat", "ImGui::SliderInt",
    "ImGui::DragFloat", "ImGui::DragInt", "ImGui::ColorEdit3", "ImGui::ColorEdit4",
    # 结构与提示
    "ImGui::BeginTabItem", "ImGui::SeparatorText", "ImGui::ProgressBar",
    "ImGui::SetTooltip", "ImGui::ListBox", "ImGui::SetNextItemWidth",
)

LIT = re.compile(r'"((?:[^"\\]|\\.)*)"')
CJK = re.compile(r"[\u4e00-\u9fff]")


def comment_mask(text: str) -> bytearray:
    """标记每个字符是否处于注释中（行注释或块注释）。"""
    n = len(text)
    mask = bytearray(n)
    i = 0
    while i < n:
        c = text[i]
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            while i < n and text[i] != "\n":
                mask[i] = 1
                i += 1
            continue
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            mask[i] = mask[i + 1] = 1
            i += 2
            while i < n and not (text[i] == "*" and i + 1 < n and text[i + 1] == "/"):
                mask[i] = 1
                i += 1
            if i < n:
                mask[i] = mask[i + 1] = 1
                i += 2
            continue
        if c == '"':
            m = LIT.match(text, i)
            if m:
                i = m.end()
                continue
        if c == "'":
            j = i + 1
            while j < n and text[j] != "'":
                j += 2 if text[j] == "\\" else 1
            i = j + 1
            continue
        i += 1
    return mask


def first_literal(text: str, open_paren: int):
    depth = 0
    i = open_paren
    while i < len(text):
        c = text[i]
        if c == '"':
            m = LIT.match(text, i)
            return (m.group(1), i) if m else None
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return None
        i += 1
    return None


def main():
    out, seen = [], set()
    for pat in ("**/*.cpp", "**/*.h"):
        for f in ROOT.glob(pat):
            p = str(f).replace("\\", "/")
            if "/external/" in p or "/include/" in p or "/menu/font/" in p:
                continue
            try:
                t = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            mask = comment_mask(t)
            for w in WIDGETS:
                start = 0
                while True:
                    k = t.find(w, start)
                    if k < 0:
                        break
                    start = k + len(w)
                    if mask[k]:
                        continue                      # 被注释掉的代码，跳过
                    op = t.find("(", k)
                    if op < 0 or op - k > 30:
                        continue
                    got = first_literal(t, op)
                    if not got:
                        continue
                    s, pos = got
                    if not s or CJK.search(s) or not re.search(r"[A-Za-z]{2,}", s):
                        continue
                    line = t[:k].count("\n") + 1
                    rel = str(f.relative_to(ROOT)).replace("\\", "/")
                    key = (rel, line, s)
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append((rel, line, w.split("::")[-1], s))

    for rel, line, widget, s in sorted(out):
        print(f'{rel}:{line}  {widget}  "{s}"')
    print(f"\n合计 {len(out)} 条英文控件标签（已排除注释中的代码）")
    return 0 if not out else 1


if __name__ == "__main__":
    sys.exit(main())
