#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下载上游 OptiScaler 在指定提交的源码包（本机 git 走不通时的替代方案）。

为什么不用 git clone：本机代理拦 github.com:443（git push/fetch 都失败），
但 api.github.com 是通的，而 API 的 tarball 端点会把跳转落到 codeload.github.com
（同样放行），所以能稳定拿到任意提交的完整源码。

用法：
    python tools/fetch_upstream.py <完整或短SHA>        # 下载并解压到 build/upstream-<SHA>/
    python tools/fetch_upstream.py                      # 用 .github/upstream-commit.txt 里的版本
"""
import io
import json
import pathlib
import sys
import tarfile
import urllib.error
import urllib.request

TOOLS = pathlib.Path(__file__).resolve().parent
ROOT = TOOLS.parent
PIN = (ROOT / "src" / ".github" / "upstream-commit.txt").read_text(encoding="utf-8").strip()
OUT = ROOT / "build"
UPSTREAM = "OptiScaler/OptiScaler"


class NoAuth(urllib.request.HTTPRedirectHandler):
    """跳到 codeload.githubusercontent.com 时必须摘掉 Authorization"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        r = super().redirect_request(req, fp, code, msg, headers, newurl)
        if r is not None and urllib.parse.urlsplit(newurl).hostname != urllib.parse.urlsplit(req.full_url).hostname:
            r.headers.pop("Authorization", None)
        return r


import urllib.parse  # noqa: E402

TOKEN = (ROOT / "build" / "cred.txt").read_text(encoding="utf-8").split("password=")[1].strip().splitlines()[0]
OPENER = urllib.request.build_opener(NoAuth())


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}", "User-Agent": "fetch-upstream",
        "Accept": "application/vnd.github+json"})
    return OPENER.open(req, timeout=600).read()


def main():
    sha = (sys.argv[1] if len(sys.argv) > 1 else PIN).strip()
    if len(sha) < 7:
        sys.exit("SHA 至少 7 位")

    # 1) 把短 SHA 补全，并确认它真的存在于上游
    print(f"确认上游提交 {sha} ……")
    try:
        meta = json.loads(fetch(f"https://api.github.com/repos/{UPSTREAM}/commits/{sha}"))
    except urllib.error.HTTPError as e:
        sys.exit(f"上游不存在该提交（HTTP {e.code}）：{e.read().decode('utf-8', 'replace')[:200]}")
    full = meta["sha"]
    short = full[:7]
    when = meta["commit"]["committer"]["date"]
    msg = meta["commit"]["message"].splitlines()[0]
    print(f"  {short}  {when}  {msg}")

    dest = OUT / f"upstream-{short}"
    marker = dest / ".done"
    if marker.exists():
        print(f"\n已存在 {dest}（跳过下载）。")
        return 0

    # 2) 下载源码包（跟随跳转到 codeload）
    print("下载源码包（约 20~30MB，走代理可能要一两分钟）……")
    blob = fetch(f"https://api.github.com/repos/{UPSTREAM}/tarball/{full}")
    print(f"  收到 {len(blob)/1048576:.1f} MB")

    # 3) 解压（tarball 里最外层是 <repo>-<sha>/ 目录，去掉这一层）
    dest.mkdir(parents=True, exist_ok=True)
    count = 0
    with tarfile.open(fileobj=io.BytesIO(blob)) as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            rel = m.name.split("/", 1)[1] if "/" in m.name else m.name
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(tf.extractfile(m).read())
            count += 1
    marker.write_text(f"{full}\n{when}\n{msg}\n", encoding="utf-8")
    print(f"  解压 {count} 个文件 -> {dest}")

    # 4) 提示下一步
    print(
        "\n下一步（详见《更新上游.md》）：\n"
        "  1. 把当前 Release 里的 localization.patch 应用到上面目录：\n"
        f"     cd {dest} && git apply --reject --whitespace=nowarn ../../zh-CN/构建工具/localization.patch\n"
        "  2. 处理 *.rej，重跑字符串替换工具，再重新生成字体子集\n"
        "  3. 把改动文件覆盖回 src/ 并用 publish_overlay.py 上传"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
