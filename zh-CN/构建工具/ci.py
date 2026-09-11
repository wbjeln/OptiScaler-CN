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
    python tools/ci.py release <run_id>    # 把产物发布成 Release（固定下载地址）

令牌来源优先级：环境变量 GITHUB_TOKEN / GH_TOKEN > --token-file 指定的文件 >
本机 git 凭据管理器。之所以要有「令牌文件」这条路：在部分沙箱环境里
`git credential fill` 打印完凭据后不会退出，进程会一直挂住。
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

def read_token_file(path: str):
    """从凭据导出文件里读取令牌（文件内需有 `password=` 行）"""
    try:
        text = pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for line in text.splitlines():
        if line.startswith("password="):
            tok = line[len("password="):].strip()
            if tok:
                return tok
    return None


def get_token(token_file: str = None) -> str:
    env_tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if env_tok and env_tok.strip():
        return env_tok.strip()
    if token_file:
        tok = read_token_file(token_file)
        if tok:
            return tok
        sys.exit(f"错误：{token_file} 中没有 password= 行")

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


class ApiError(Exception):
    """GitHub API 返回了非 2xx。带状态码，便于调用方区分「资源不存在」等情况。"""

    def __init__(self, code: int, message: str):
        self.code = code
        super().__init__(f"HTTP {code}: {message}")


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
        raise ApiError(e.code, f"{e.reason} {e.read().decode('utf-8', 'replace')[:500]}") from None
    if raw:
        return payload
    return json.loads(payload.decode("utf-8", "replace")) if payload else None


def api_soft(path: str, allow=(404,)):
    """出错时返回 None 而不是抛异常，用于「不存在就创建」这类分支"""
    try:
        return api(path)
    except ApiError as e:
        if e.code in allow:
            return None
        raise


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


def safe_target(out: pathlib.Path, name: str) -> pathlib.Path:
    """拼出落盘路径，并挡住 zip 里的绝对路径与 ../ 越界（zip-slip）"""
    rel = pathlib.PurePosixPath(name.replace("\\", "/"))
    parts = [p for p in rel.parts if p not in ("", ".", "..", "/")]
    return out.joinpath(*parts)


def cmd_fetch(args):
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    arts = api(f"/repos/{REPO}/actions/runs/{args.run_id}/artifacts")["artifacts"]
    if not arts:
        print("该次运行没有产物")
        return 1
    for a in arts:
        name = a["name"]
        print(f"下载产物：{name}（{a['size_in_bytes']/1048576:.1f} MB）")
        blob = api(a["archive_download_url"], raw=True)

        try:
            zf = zipfile.ZipFile(io.BytesIO(blob))
            names = [n for n in zf.namelist() if not n.endswith("/")]
        except zipfile.BadZipFile:
            target = out / name
            target.write_bytes(blob)
            print(f"   -> {target}  ({target.stat().st_size/1048576:.1f} MB)")
            continue

        # 情况 1：GitHub 的「产物包装 zip」——里面只有我们要的那一个压缩包
        if len(names) == 1 and names[0].lower().endswith((".zip", ".7z")):
            target = out / pathlib.PurePosixPath(names[0]).name
            target.write_bytes(zf.read(names[0]))
            print(f"   -> {target}  ({target.stat().st_size/1048576:.1f} MB)")
            continue

        # 情况 2：工作流用了 upload-artifact 的 archive:false，GitHub 直接把原文件作为
        # 产物提供（产物名就是文件名）。此时下载到的字节本身就是那个压缩包，
        # 必须原样另存，绝不能当包装包去解包——否则整棵目录树会被压平成一堆文件。
        if pathlib.PurePosixPath(name).suffix.lower() in (".zip", ".7z"):
            target = out / name
            target.write_bytes(blob)
            print(f"   -> {target}  ({target.stat().st_size/1048576:.1f} MB)")
            continue

        # 情况 3：普通产物 zip，按原目录结构解包
        for info in zf.infolist():
            if info.is_dir():
                continue
            target = safe_target(out, info.filename)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(info))
            print(f"   -> {target}  ({target.stat().st_size/1048576:.1f} MB)")
    return 0


def cmd_trigger(args):
    api(f"/repos/{REPO}/actions/workflows/{args.workflow}/dispatches",
        method="POST", body={"ref": args.ref})
    print(f"已触发 {args.workflow} @ {args.ref}")
    return 0


DEFAULT_NOTES = """OptiScaler 简体中文版（汉化 + 预编译）

解压 `OptiScaler-CN.zip` 到**游戏主程序 exe 所在目录**，双击 `setup_windows.bat`
按中文提示操作即可。虚幻引擎游戏请解压到 `<游戏目录>\\<项目名>\\Binaries\\Win64`。

- 设置菜单、提示弹窗、配置注释、安装脚本提示均为简体中文
- 中文字体已内嵌进 DLL，无需另外安装字体
- 功能逻辑与官方版本完全一致

`OptiScaler-CN-source.zip` 是汉化后的完整源码（GPLv3 要求随二进制一并提供）。

授权：GNU GPLv3。本汉化版由第三方制作，与 OptiScaler 原作者无关，仅供学习交流。
"""


def cmd_release(args):
    """把构建产物发布成 GitHub Release，得到一个固定、永不过期的下载地址"""
    dist = pathlib.Path(args.out)
    want = ["OptiScaler-CN.zip", "OptiScaler-CN-source.zip"]

    if args.run_id and args.run_id != "-":
        if cmd_fetch(argparse.Namespace(run_id=args.run_id, out=str(dist))) != 0:
            return 1

    files = [dist / f for f in want if (dist / f).is_file()]
    if not files:
        print(f"没有找到可发布的产物（{dist} 下没有 {' / '.join(want)}）")
        print("请先用 `python tools/ci.py fetch <运行ID>` 下载，或改用 --run-id <运行ID>。")
        return 1
    for f in want:
        if not (dist / f).is_file():
            print(f"[提示] 缺少 {f}，本次只发布已存在的文件")

    notes = DEFAULT_NOTES
    if args.notes_file:
        notes = pathlib.Path(args.notes_file).read_text(encoding="utf-8")

    rel = api_soft(f"/repos/{REPO}/releases/tags/{args.tag}")
    if rel is None:
        rel = api(f"/repos/{REPO}/releases", method="POST", body={
            "tag_name": args.tag,
            "name": args.name or f"OptiScaler 简体中文版 {args.tag}",
            "body": notes,
            "draft": False,
            "prerelease": False,
            "target_commitish": args.ref,
        })
        print(f"已创建 Release：{args.tag}")
    else:
        rel = api(f"/repos/{REPO}/releases/{rel['id']}", method="PATCH",
                  body={"name": args.name or f"OptiScaler 简体中文版 {args.tag}", "body": notes})
        print(f"Release {args.tag} 已存在，已更新说明")

    # GitHub 不允许同名附件重复上传，先删掉旧的
    old = {a["name"]: a["id"] for a in api(f"/repos/{REPO}/releases/{rel['id']}/assets")}
    for f in files:
        if f.name in old:
            api(f"/repos/{REPO}/releases/assets/{old[f.name]}", method="DELETE")
            print(f"  已删除同名旧附件 {f.name}")

    base = f"https://uploads.github.com/repos/{REPO}/releases/{rel['id']}"
    for f in files:
        data = f.read_bytes()
        req = urllib.request.Request(
            f"{base}/assets?name={urllib.parse.quote(f.name)}", data=data, method="POST",
            headers={"Authorization": f"Bearer {TOKEN}",
                     "Accept": "application/vnd.github+json",
                     "Content-Type": "application/zip",
                     "User-Agent": "optiscaler-cn-ci"})
        with OPENER.open(req, timeout=900) as r:
            info = json.loads(r.read().decode("utf-8", "replace"))
        print(f"  已上传 {f.name}  ({len(data)/1048576:.1f} MB)")

    print(f"\n下载页面：https://github.com/{REPO}/releases/tag/{args.tag}")
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

    p = sub.add_parser("release", help="把产物发布成 Release（固定下载地址）")
    p.add_argument("run_id", nargs="?", default="-", help="运行 ID；填 - 表示用 --out 里已有的文件")
    p.add_argument("--tag", default="v10.0.0-cn")
    p.add_argument("--name", default=None)
    p.add_argument("--out", default=str(ROOT / "dist"))
    p.add_argument("--notes-file", default=None)
    p.add_argument("--ref", default="main")
    p.set_defaults(func=cmd_release)

    ap.add_argument("--token-file", default=None,
                    help="从文件读取令牌（文件内需有 password= 行）")
    args = ap.parse_args()

    global TOKEN
    TOKEN = get_token(args.token_file)
    try:
        return args.func(args)
    except ApiError as e:
        print(f"GitHub API 调用失败：{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
