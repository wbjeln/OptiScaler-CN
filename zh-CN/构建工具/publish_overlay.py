#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把汉化覆盖层（相对上游的改动文件）通过 GitHub Contents API 上传到私有仓库。

为什么不用 git push：
    当前网络环境只放行了 api.github.com / codeload.github.com，github.com:443
    被代理拦截（CONNECT 502），git push 走不通，只能走 REST API。

用法：
    python tools/publish_overlay.py            # 干跑，列出将要上传的文件
    python tools/publish_overlay.py --apply    # 真正上传
令牌来源：本机 git 凭据管理器（不落盘、不打印）。
"""
import argparse
import base64
import json
import os
import pathlib
import subprocess
import tempfile
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

REPO = "wbjeln/OptiScaler-CN"
BRANCH = "main"
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


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
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()
        return r.status, (json.loads(raw.decode()) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw}


def changed_files():
    """用 git 算出相对上游改动的文件清单（这些就是覆盖层内容）"""
    out = subprocess.run(["git", "-c", "core.quotePath=false", "diff", "--name-only", "HEAD~1", "HEAD"],
                         cwd=SRC, capture_output=True, text=True, encoding="utf-8").stdout
    files = [l.strip() for l in out.splitlines() if l.strip()]
    # 只上传确实存在的文件（没有删除项）
    return [f for f in files if (SRC / f).is_file()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真正上传（默认只干跑）")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 个（调试用）")
    ap.add_argument("--token-file", default=None,
                    help="从文件读取令牌（文件内需有 password= 行）")
    args = ap.parse_args()

    global TOKEN
    if args.token_file:
        TOKEN = read_token_file(args.token_file)
    else:
        sys.exit("请用 --token-file 指定令牌文件（由 shell 从凭据管理器导出）")

    files = changed_files()
    if args.limit:
        files = files[: args.limit]
    print(f"覆盖层文件数：{len(files)}")

    ok = fail = 0
    for i, rel in enumerate(files, 1):
        data = (SRC / rel).read_bytes()
        print(f"  {i:>3}/{len(files)}  {rel}  ({len(data)} 字节)", end="")
        if not args.apply:
            print("   [干跑]")
            continue

        quoted = "/".join(urllib.parse.quote(seg) for seg in rel.split("/"))
        for attempt in range(2):
            status, resp = call(f"/repos/{REPO}/contents/{quoted}", "GET")
            sha = resp.get("sha") if status == 200 and isinstance(resp, dict) else None
            body = {
                "message": f"汉化覆盖层：{rel}",
                "content": base64.b64encode(data).decode(),
                "branch": BRANCH,
            }
            if sha:
                body["sha"] = sha
            status, resp = call(f"/repos/{REPO}/contents/{quoted}", "PUT", body)
            if status in (200, 201):
                print(f"   -> 上传成功 ({'更新' if sha else '新建'})")
                ok += 1
                break
            if status == 409 and attempt == 0:      # 并发/已存在，重取 sha 再试
                time.sleep(1)
                continue
            print(f"   -> 失败 HTTP {status}: {str(resp)[:200]}")
            fail += 1
            break
        time.sleep(0.2)

    print(f"\n完成：成功 {ok}，失败 {fail}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
