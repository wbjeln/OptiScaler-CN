# 一键卸载 OptiScaler（简体中文版）—— 实际逻辑都在这里。
#
# 「卸载 OptiScaler.bat」只是个入口，负责调用本脚本；
# 逻辑放在 PowerShell 里是因为它原生支持 Unicode 路径，
# 而 cmd 处理中文路径／中文注释时有一堆代码页与解析上的坑。
#
# 安全原则：
#   · 只删「确认属于 OptiScaler」的文件
#   · 游戏／ReShade 自带的同名 DLL 会被保留——按文件内容识别，不是按文件名
#     （识别依据：版本信息里的 ProductName／FileDescription，或文件内容含 OptiScaler 字样）
#   · 每个文件夹都会先验证内容，确认是我们的才整份删除
#   · 不碰注册表、不碰系统目录，只操作当前文件夹
#
# 用法：双击「卸载 OptiScaler.bat」；或命令行加 -Yes 跳过确认。

param([switch]$Yes)

$ErrorActionPreference = 'SilentlyContinue'
Set-Location -LiteralPath (Split-Path -Parent $MyInvocation.MyCommand.Path)

# ---------------------------------------------------------------------------
# 判断一个 DLL 是不是 OptiScaler
# ---------------------------------------------------------------------------
function Test-OursDll([string]$name) {
    try {
        $item = Get-Item -LiteralPath $name -ErrorAction Stop
        $v = $item.VersionInfo
        if ($v.ProductName -like '*OptiScaler*' -or $v.FileDescription -like '*OptiScaler*') { return $true }
        $bytes = [IO.File]::ReadAllBytes($name)
        return ([Text.Encoding]::ASCII.GetString($bytes).Contains('OptiScaler'))
    } catch { return $false }
}

# ---------------------------------------------------------------------------
# 扫描
# ---------------------------------------------------------------------------
Write-Host '── 正在扫描当前文件夹……'
Write-Host ''

$files = @()
$dirs  = @()

# 1) 名字就能确定是我们的
foreach ($n in 'OptiScaler.dll','OptiScaler.ini','OptiScaler.asi',
                'Remove_OptiScaler.bat','Remove OptiScaler.bat') {
    if (Test-Path -LiteralPath $n -PathType Leaf) { $files += $n }
}

# 日志文件（含轮转出来的 .log.1 之类）
Get-ChildItem -LiteralPath . -Filter 'OptiScaler.log*' -File -ErrorAction SilentlyContinue |
    ForEach-Object { $files += $_.Name }

# 解压提示文件
$marker = '!! 请将所有文件解压到游戏目录 !!'
if (Test-Path -LiteralPath $marker) { $files += $marker }

# 2) 这些名字游戏可能也在用，必须先验证文件内容
$sharedNames = 'dxgi.dll','winmm.dll','version.dll','winhttp.dll','wininet.dll',
               'd3d12.dll','dbghelp.dll','nvapi64.dll','nvngx.dll'
foreach ($n in $sharedNames) {
    if (-not (Test-Path -LiteralPath $n -PathType Leaf)) { continue }
    if (Test-OursDll $n) {
        Write-Host ("  ［发现］ {0}   —— 已确认是 OptiScaler" -f $n)
        $files += $n
    } else {
        Write-Host ("  ［保留］ {0}   —— 不是 OptiScaler，不删" -f $n)
    }
}

# 3) 文件夹：先验证内容，确认是我们的才整份删除
if (Test-Path -LiteralPath 'OptiScaler' -PathType Container) {
    $m = 'OptiScaler\libxess.dll','OptiScaler\amd_fidelityfx_loader_dx12.dll',
         'OptiScaler\D3D12_OptiScaler','OptiScaler\Streamline','OptiScaler\streamline',
         'OptiScaler\plugins'
    if ($m | Where-Object { Test-Path -LiteralPath $_ }) { $dirs += 'OptiScaler' }
}
if (Test-Path -LiteralPath 'Licenses' -PathType Container) {
    $m = 'Licenses\XeSS_LICENSE.txt','Licenses\DirectX_LICENSE.txt',
         'Licenses\FidelityFX_v2_LICENSE.md'
    if ($m | Where-Object { Test-Path -LiteralPath $_ }) { $dirs += 'Licenses' }
}
if (Test-Path -LiteralPath '文档' -PathType Container) {
    $m = '文档\Config.zh.md','文档\OptiScaler中文文档.html','文档\Issues.zh.md'
    if ($m | Where-Object { Test-Path -LiteralPath $_ }) { $dirs += '文档' }
}

foreach ($f in $files)  { Write-Host ("  ［发现］ {0}" -f $f) }
foreach ($d in $dirs)   { Write-Host ("  ［发现］ {0}\" -f $d) }

# ---------------------------------------------------------------------------
# 确认
# ---------------------------------------------------------------------------
$total = $files.Count + $dirs.Count
if ($total -eq 0) {
    Write-Host ''
    Write-Host '没有发现任何 OptiScaler 的文件，无需卸载。'
    Write-Host '如果游戏装在别的文件夹，请把本脚本复制到那个文件夹里再运行一次。'
    if (-not $Yes) { Read-Host '按回车键退出' | Out-Null }
    exit 0
}

Write-Host ''
Write-Host ("共发现 {0} 个项目（见上表）。" -f $total)
if (-not $Yes) {
    Write-Host ''
    $answer = Read-Host '确认删除以上全部内容吗？【Y＝删除 ／ N＝取消】'
    if ($answer -notmatch '^[Yy]$') {
        Write-Host ''
        Write-Host '已取消，未删除任何文件。'
        exit 1
    }
}

# ---------------------------------------------------------------------------
# 删除
# ---------------------------------------------------------------------------
Write-Host ''
Write-Host '── 正在删除……'
Write-Host ''

$left = @()
foreach ($f in $files) {
    Remove-Item -LiteralPath $f -Force -ErrorAction SilentlyContinue
    if (Test-Path -LiteralPath $f) {
        Write-Host ("  [失败] {0}   —— 文件可能正被游戏占用" -f $f)
        $left += $f
    } else {
        Write-Host ("  [已删] {0}" -f $f)
    }
}
foreach ($d in $dirs) {
    Remove-Item -LiteralPath $d -Recurse -Force -ErrorAction SilentlyContinue
    if (Test-Path -LiteralPath $d) {
        Write-Host ("  [失败] {0}\   —— 里面有文件被占用" -f $d)
        $left += $d
    } else {
        Write-Host ("  [已删] {0}\" -f $d)
    }
}

# ---------------------------------------------------------------------------
# 复查残留
# ---------------------------------------------------------------------------
Write-Host ''
Write-Host '── 复查是否还有残留……'

foreach ($f in $files)  { if (Test-Path -LiteralPath $f)  { Write-Host ("  [残留] {0}   —— 请关闭游戏后重试" -f $f) } }
foreach ($d in $dirs)   { if (Test-Path -LiteralPath $d)  { Write-Host ("  [残留] {0}\   —— 请关闭游戏后重试" -f $d) } }
if ($left.Count -eq 0) { Write-Host '   没有残留，已全部清除。' }

# ---------------------------------------------------------------------------
# 删除卸载器本体（本脚本；入口 .bat 由调用方在自己退出后删除）
# ---------------------------------------------------------------------------
Remove-Item -LiteralPath $MyInvocation.MyCommand.Path -Force -ErrorAction SilentlyContinue

Write-Host ''
Write-Host '卸载完成！'
if (-not $Yes) { Read-Host '按回车键退出' | Out-Null }
exit 0
