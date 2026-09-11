#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把汉化覆盖层（相对上游的改动文件）上传到私有仓库 wbjeln/OptiScaler-CN。

两个关键设计：

1) 为什么不用 git push：
   本机网络只放行了 api.github.com / codeload.github.com，github.com:443 被代理
   拦截（CONNECT 502），git push 走不通，所以改用 GitHub REST API。

2) 为什么用 Git Data API 做「单次提交」而不是 Contents API 逐文件上传：
   Contents API 每上传一个文件就产生一个 commit，而 workflow 在 push 到 main 时
   触发，结果是「39 个文件 -> 38 个并发构建」，既浪费额度，又因为每次提交只有
   部分文件而必然失败。Git Data API 可以一次构造 tree + commit + 更新 ref，
   整批文件只产生一个提交、只触发一次构建。

用法：
    python tools/publish_overlay.py --token-file build/cred.txt            # 干跑
    python tools/publish_overlay.py --token-file build/cred.txt --apply    # 真正上传
"""
import argparse
import base64
import json
import pathlib
import subprocess
import sys
import urllib.error
import urllib.request

REPO = "wbjeln/OptiScaler-CN"
BRANCH = "main"
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# 这些路径属于「覆盖层仓库自己的东西」，不该被覆盖到上游源码里
EXCLUDE_PREFIXES = (".git/", "x64/", "build/")
EXCLUDE_EXACT = {".git"}


def read_token_file(path: str) -> str:
    text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    for line in text.splitlines():
        if line.startswith("password="):
            tok = line[len("password="):].strip()
            if tok:
                return tok
    sys.exit(f"错误：{path} 中没有 password= 行")


TOKEN = None


def call(path: str, method="GET", body=None):
    url = f"https://api.github.com{path}"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "optiscaler-cn-publish",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
        return r.status, (json.loads(raw.decode()) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw}


def changed_files():
    """相对上游提交的改动清单（含未提交的工作区改动与新增文件）"""
    def git(*args):
        return subprocess.run(["git", "-c", "core.quotePath=false", *args],
                              cwd=SRC, capture_output=True, text=True,
                              encoding="utf-8", errors="replace").stdout

    # HEAD~1 = 上游基线；对比工作区，能同时覆盖「已提交 + 未提交」的改动
    files = set(l.strip() for l in git("diff", "--name-only", "HEAD~1").splitlines() if l.strip())
    # 新增但还没提交的文件（--exclude-standard 会尊重 .gitignore）
    files |= set(l.strip() for l in git("ls-files", "--others", "--exclude-standard").splitlines() if l.strip())

    keep = []
    for f in sorted(files):
        norm = f.replace("\\", "/")
        if norm in EXCLUDE_EXACT or norm.startswith(EXCLUDE_PREFIXES):
            continue
        if (SRC / norm).is_file():
            keep.append(norm)
    return keep


def file_mode(rel: str) -> str:
    """沿用索引里的文件权限位；未跟踪文件按扩展名给默认值"""
    out = subprocess.run(["git", "ls-files", "-s", "--", rel], cwd=SRC,
                         capture_output=True, text=True, encoding="utf-8").stdout.strip()
    if out:
        return out.split()[0]
    return "100755" if rel.endswith((".py", ".sh")) else "100644"


def upload_single_commit(files, message: str) -> bool:
    st, ref = call(f"/repos/{REPO}/git/ref/heads/{BRANCH}")
    if st != 200:
        print(f"[X] 取分支失败 HTTP {st}: {str(ref)[:200]}")
        return False
    base_commit = ref["object"]["sha"]

    st, commit = call(f"/repos/{REPO}/git/commits/{base_commit}")
    if st != 200:
        print(f"[X] 取基线提交失败 HTTP {st}")
        return False
    base_tree = commit["tree"]["sha"]
    print(f"基线提交：{base_commit[:8]}  tree：{base_tree[:8]}")

    entries = []
    for i, rel in enumerate(files, 1):
        data = (SRC / rel).read_bytes()
        st, blob = call(f"/repos/{REPO}/git/blobs", "POST",
                        {"content": base64.b64encode(data).decode(), "encoding": "base64"})
        if st not in (200, 201):
            print(f"  [X] {rel} 建 blob 失败 HTTP {st}: {str(blob)[:160]}")
            return False
        entries.append({"path": rel, "mode": file_mode(rel), "type": "blob", "sha": blob["sha"]})
        print(f"  {i:>3}/{len(files)}  {rel}  ({len(data)} 字节)  blob {blob['sha'][:8]}")

    st, tree = call(f"/repos/{REPO}/git/trees", "POST", {"base_tree": base_tree, "tree": entries})
    if st not in (200, 201):
        print(f"[X] 建 tree 失败 HTTP {st}: {str(tree)[:200]}")
        return False

    st, newc = call(f"/repos/{REPO}/git/commits", "POST",
                    {"message": message, "tree": tree["sha"], "parents": [base_commit]})
    if st not in (200, 201):
        print(f"[X] 建提交失败 HTTP {st}: {str(newc)[:200]}")
        return False

    st, res = call(f"/repos/{REPO}/git/refs/heads/{BRANCH}", "PATCH",
                   {"sha": newc["sha"], "force": False})
    if st not in (200, 201):
        print(f"[X] 更新分支失败 HTTP {st}: {str(res)[:200]}")
        return False

    print(f"\n完成：单个提交 {newc['sha'][:8]}，共 {len(files)} 个文件，只触发一次构建。")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正上传（默认只干跑）")
    ap.add_argument("--token-file", default=None, help="令牌文件（内含 password= 行）")
    ap.add_argument("--message", default="汉化：修复编译错误并补全安装脚本汉化",
                    help="提交信息")
    args = ap.parse_args()

    global TOKEN
    if not args.token_file:
        sys.exit("请用 --token-file 指定令牌文件（由 shell 从凭据管理器导出）")
    TOKEN = read_token_file(args.token_file)

    files = changed_files()
    print(f"改动文件数：{len(files)}")
    for f in files:
        print(f"    {f}  ({file_mode(f)})")

    if not args.apply:
        print("\n干跑结束，未上传。加 --apply 才真正提交。")
        return 0

    print()
    return 0 if upload_single_commit(files, args.message) else 1


if __name__ == "__main__":
    sys.exit(main())
