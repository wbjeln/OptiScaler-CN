#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OptiScaler-CN 云编译助手

用法：
    python tools/ci.py runs                # 列出最近的工作流运行
    python tools/ci.py runs --watch        # 轮询直到最新一次运行结束
    python tools/ci.py status <run_id>     # 查看某次运行的每个步骤
    python tools/ci.py logs   <run_id>     # 下载失败步骤的日志
    python tools/ci.py fetch  <run_id>     # 下载产物到 dist/
    python tools/ci.py trigger             # 手动触发一次构建

令牌来源：本机 git 凭据管理器（不落盘、不打印）。
"""
import argparse
import io
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

REPO = "wbjeln/OptiScaler-CN"
API = "https://api.github.com"
ROOT = pathlib.Path(__file__).resolve().parent.parent


# ------------------------------------------------------------------ 凭据

def get_token() -> str:
    env = dict(os.environ)
    env.update(GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="never", GCM_PROVIDER="generic")
    out = ""
    try:
        p = subprocess.run(["git", "credential", "fill"],
                           input="protocol=https\nhost=github.com\n\n",
                           capture_output=True, text=True, env=env, timeout=8)
        out = p.stdout
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or "")
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
    for line in out.splitlines():
        if line.startswith("password="):
            return line[len("password="):].strip()
    sys.exit("错误：未能从凭据管理器取得 GitHub 令牌")


# ------------------------------------------------------------------ HTTP

class _NoAuthOnRedirect(urllib.request.HTTPRedirectHandler):
    """跨域重定向（下载产物会跳到对象存储）时必须去掉 Authorization 头"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new is not None and urllib.parse.urlsplit(newurl).hostname != urllib.parse.urlsplit(req.full_url).hostname:
            new.headers.pop("Authorization", None)
        return new


OPENER = urllib.request.build_opener(_NoAuthOnRedirect)
TOKEN = None


def api(path: str, method: str = "GET", body=None, raw: bool = False):
    url = path if path.startswith("http") else f"{API}{path}"
    data = None
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "optiscaler-cn-ci",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with OPENER.open(req, timeout=60) as r:
            payload = r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} {e.reason}: {e.read().decode('utf-8', 'replace')[:500]}")
    if raw:
        return payload
    return json.loads(payload.decode("utf-8", "replace")) if payload else None


# ------------------------------------------------------------------ 命令

def latest_run():
    d = api(f"/repos/{REPO}/actions/runs?per_page=1")
    runs = d.get("workflow_runs") or []
    return runs[0] if runs else None


def fmt_run(r):
    return (f"#{r['run_number']}  id={r['id']}  状态={r['status']:<12} 结论={r['conclusion'] or '-':<10} "
            f"分支={r['head_branch']}  提交={r['head_sha'][:8]}  创建={r['created_at']}")


def cmd_runs(args):
    if args.watch:
        while True:
            r = latest_run()
            if r is None:
                print("尚未有任何运行……等待工作流被触发")
            else:
                print(fmt_run(r))
                if r["status"] == "completed":
                    print(f"\n运行已结束，结论：{r['conclusion']}")
                    print(f"详情：https://github.com/{REPO}/actions/runs/{r['id']}")
                    return 0 if r["conclusion"] == "success" else 1
            sys.stdout.flush()
            time.sleep(args.interval)
    d = api(f"/repos/{REPO}/actions/runs?per_page={args.limit}")
    runs = d.get("workflow_runs") or []
    if not runs:
        print("没有运行记录")
        return 1
    for r in runs:
        print(fmt_run(r))
    return 0


def cmd_status(args):
    run = api(f"/repos/{REPO}/actions/runs/{args.run_id}")
    print(f"运行 #{run['run_number']}  {run['status']} / {run['conclusion']}")
    print(f"提交 {run['head_sha'][:8]}  分支 {run['head_branch']}")
    jobs = api(f"/repos/{REPO}/actions/runs/{args.run_id}/jobs")["jobs"]
    bad = []
    for j in jobs:
        print(f"\n■ {j['name']}  [{j['status']}/{j['conclusion']}]")
        for s in j.get("steps", []):
            mark = {"success": "✓", "failure": "✗", "skipped": "-", "cancelled": "x"}.get(s["conclusion"], "·")
            print(f"   {mark} {s['name']}  ({s['conclusion']})")
            if s["conclusion"] == "failure":
                bad.append(s["name"])
    if bad:
        print("\n失败的步骤：" + "、".join(bad))
        if args.auto_logs:
            for name in bad:
                cmd_logs(argparse.Namespace(run_id=args.run_id, step=name, tail=80))
        return 1
    return 0


def cmd_logs(args):
    """拉取整份运行日志，按作业分组打印（失败作业优先）"""
    data = api(f"/repos/{REPO}/actions/runs/{args.run_id}/logs", raw=True)
    zf = zipfile.ZipFile(io.BytesIO(data))
    names = zf.namelist()
    # 优先显示名字里带 failed 的作业
    names.sort(key=lambda n: (0 if "fail" in n.lower() else 1, n))
    for n in names:
        if args.step and args.step not in n:
            continue
        print(f"\n{'='*80}\n### {n}\n{'='*80}")
        text = zf.read(n).decode("utf-8", "replace")
        lines = text.splitlines()
        if args.step:
            # 只保留失败步骤附近的上下文
            keep, hit = [], False
            for i, ln in enumerate(lines):
                if "##[error]" in ln or "##[group]" in ln:
                    keep.extend(lines[max(0, i - 3): i + 3])
            lines = keep or lines
        for ln in lines[-args.tail:]:
            print(ln)


def cmd_fetch(args):
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    arts = api(f"/repos/{REPO}/actions/runs/{args.run_id}/artifacts")["artifacts"]
    if not arts:
        print("该次运行没有产物")
        return 1
    for a in arts:
        print(f"下载产物：{a['name']}（{a['size_in_bytes']/1048576:.1f} MB）")
        blob = api(a["archive_download_url"], raw=True)
        zf = zipfile.ZipFile(io.BytesIO(blob))
        for n in zf.namelist():
            target = out / pathlib.Path(n).name
            target.write_bytes(zf.read(n))
            print(f"   -> {target}  ({target.stat().st_size/1048576:.1f} MB)")
    return 0


def cmd_trigger(args):
    api(f"/repos/{REPO}/actions/workflows/{args.workflow}/dispatches",
        method="POST", body={"ref": args.ref})
    print(f"已触发 {args.workflow} @ {args.ref}")
    return 0


def main():
    global TOKEN
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("runs"); p.add_argument("--limit", type=int, default=5)
    p.add_argument("--watch", action="store_true"); p.add_argument("--interval", type=int, default=20)
    p.set_defaults(func=cmd_runs)

    p = sub.add_parser("status"); p.add_argument("run_id")
    p.add_argument("--auto-logs", action="store_true"); p.set_defaults(func=cmd_status)

    p = sub.add_parser("logs"); p.add_argument("run_id")
    p.add_argument("--step", default=None); p.add_argument("--tail", type=int, default=120)
    p.set_defaults(func=cmd_logs)

    p = sub.add_parser("fetch"); p.add_argument("run_id")
    p.add_argument("--out", default=str(ROOT / "dist")); p.set_defaults(func=cmd_fetch)

    p = sub.add_parser("trigger")
    p.add_argument("--workflow", default="build-cn.yml")
    p.add_argument("--ref", default="main"); p.set_defaults(func=cmd_trigger)

    args = ap.parse_args()
    TOKEN = get_token()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
