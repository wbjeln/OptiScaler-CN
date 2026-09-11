<!--
  汉化版附加说明：由第三方添加，与 OptiScaler 原作者无关。
  本节之后是上游原始 README（英文），保持不变。
-->

# OptiScaler 简体中文版

> 这是开源画质增强注入工具 **[OptiScaler](https://github.com/OptiScaler/OptiScaler)** 的
> **全项目汉化版**，由 GitHub Actions **云端编译**成解压即用的 Windows 成品。
> 功能逻辑与官方完全一致，只汉化了界面、配置注释、安装脚本，并内嵌了中文字体。
> 汉化基于上游提交 `d36a078f`（版本号 10.0.0）。

- 设置菜单、提示弹窗 —— **全中文**
- `OptiScaler.ini` 配置注释 —— **全中文**（键名与取值和官方完全一致，配置文件可通用）
- `setup_windows.bat` / `setup_linux.sh` 安装脚本提示 —— **全中文**
- 中文字体（思源黑体子集）**已内嵌进 DLL**，不需要另外安装或放置字体文件

---

## 📥 下载：怎么拿到整个程序

### 方式 1：直接下载编译好的成品（推荐）

打开 **[Releases 页面](https://github.com/wbjeln/OptiScaler-CN/releases)**，
在最新版本下方下载附件：

| 附件 | 说明 |
| --- | --- |
| **`OptiScaler-CN.zip`** | **成品运行包**。解压到游戏目录即可用，不需要自己编译 |
| `OptiScaler-CN-source.zip` | 汉化后的完整源码（GPLv3 要求随二进制一并提供） |

> 本仓库是**私有**仓库，下载前需要先用有权限的 GitHub 账号登录。

### 方式 2：从 Actions 的构建记录里下载

打开 **[Actions 页面](https://github.com/wbjeln/OptiScaler-CN/actions)** →
选最新一次**成功**的运行 → 页面底部 **Artifacts** 区域 → 下载
`OptiScaler-CN-package` 与 `OptiScaler-CN-source`。

> Artifacts 默认只保留 90 天，过期后请用方式 1，或重新触发一次构建。

### 方式 3：自己编译（本机无需安装 Visual Studio）

[Actions](https://github.com/wbjeln/OptiScaler-CN/actions) →
选择左侧的 `Build OptiScaler CN (Windows x64)` → **Run workflow**。

工作流会自动：克隆上游 `d36a078f` 与全部子模块 → 覆盖汉化文件 → MSBuild 编译 `Release|x64`
→ **校验中文确实编译进了 DLL / INI / 安装脚本**（避免「编译成功但汉化没生效」的假成功）
→ 打包出运行包与 GPLv3 源码包。

本机编译请见下方第四节「编译方法」。

---

## 🧩 安装（3 步）

1. **解压位置**：把包里的**全部文件**解压到**游戏主程序 exe 所在目录**。
   - 虚幻引擎（UE）游戏通常是 `<游戏目录>\<项目名>\Binaries\Win64`
     （例如 `\Jedi Survivor\SwGame\Binaries\Win64`）
   - **千万不要**解压到 `Engine` 目录里
2. **双击 `setup_windows.bat`**，按中文提示操作。
   注入文件名默认 `dxgi.dll`（兼容性最好）；Vulkan 游戏选 `winmm.dll`。
3. **启动游戏**，默认按 `Insert` 键呼出设置菜单（可在配置文件里改快捷键）。

更完整的说明与常见问题排查见包内 **`使用说明.txt`**，配置项逐条解释见 `zh-CN/文档/`。

---

## 🀄 汉化改了什么

| # | 改动 | 涉及文件 |
| --- | --- | --- |
| 1 | 界面文案汉化（约 1000 处字符串） | `OptiScaler/menu/menu_common.cpp`、`OptiScaler/dllmain.cpp` |
| 2 | 内嵌中文字体（思源黑体子集） | 新增 `OptiScaler/menu/font/NotoSansSC_Subset.h`；改 `menu_common.cpp` |
| 3 | MSVC `/utf-8` 开关，保证中文不编译成乱码 | 新增 `Directory.Build.props`；`OptiScaler/OptiScaler.vcxproj` |
| 4 | 配置注释汉化 | `OptiScaler.ini` |
| 5 | 安装脚本提示汉化（逻辑零改动） | `setup_windows.bat`、`setup_linux.sh` |
| 6 | 版本串标注汉化版 | `OptiScaler/resource.h` |
| 7 | README 顶部追加汉化说明 | `README.md` |

几个刻意保留的设计，避免汉化影响功能：

- **数值版本号 `10.0.0` 保持不变。** 它会被传给 DLSS / XeSS / FSR 的引擎注册接口，
  版本更新检查也依赖它，改动可能影响第三方运行库。汉化标识只加在展示用的版本串上，
  叠加界面的窗口标题会显示成 `OptiScaler v10.0.0-dev (...) 简体中文版`。
- **`OptiScaler.ini` 只翻译 `;` 开头的注释行**，键名与取值一字未动，
  所以这个配置文件和官方版本可以互换使用。
- **`setup_linux.sh` 保持 LF 换行。** CRLF 会让 Linux 把 shebang 读成 `/usr/bin/env bash\r`，
  直接报 `bad interpreter`。

---

## ⚖️ 授权

- 本项目以 **GNU GPLv3** 发布（与上游一致），授权全文见 `zh-CN/LICENSE-GPLv3.txt`。
  按 GPLv3 要求，分发二进制时一并提供修改后的完整源码，即 `OptiScaler-CN-source.zip`。
- 内嵌的思源黑体（Noto Sans SC）子集以 **SIL Open Font License 1.1** 授权，允许随软件分发。
- 本汉化版由第三方制作，**与 OptiScaler 原作者无关**，仅供学习交流使用。
  因使用本软件产生的一切后果由使用者自行承担。

---

<br />

## 📄 上游原始 README（英文，保持原样）

<hr />

<div align="center">

  ![Logo](https://github.com/user-attachments/assets/c7dad5da-0b29-4710-8a57-b58e4e407abd)

</div>
<hr />
<br />
<div align="center">
  <a href="https://github.com/sponsors/cdozdil?frequency=one-time"><img src="images/gh-sponsor-red.png" /></a>
  <a href="https://buymeacoffee.com/nitec"><img src="images/bmac.png" /></a>
</div>
<br />

## Table of Contents

**1.** [**About**](#about)  
**2.** [**How it works?**](#how-it-works)  
**3.** [**Supported APIs and Upscalers**](#which-apis-and-upscalers-are-supported)  
**4.** [**Installation**](#installation)  
**5.** [**Known Issues**](#known-issues)  
**6.** [**Compilation and Credits**](#compilation)  
**7.** [**Wiki**](https://github.com/optiscaler/OptiScaler/wiki)

<br />
<div align="center">
  <a href="https://discord.gg/wEyd9w4hG5"><img src="https://img.shields.io/badge/OptiScaler-blue?style=for-the-badge&logo=discord&logoColor=white&logoSize=auto&color=5865F2" alt="Discord invite"></a>
  <a href="https://github.com/optiscaler/OptiScaler/releases/latest"><img src="https://img.shields.io/badge/Download-Stable-green?style=for-the-badge&logo=github&logoSize=auto" alt="Stable release"></a>
  <a href="https://github.com/optiscaler/OptiScaler/releases/tag/nightly"><img src="https://img.shields.io/badge/Download-Nightly-purple?style=for-the-badge&logo=github&logoSize=auto" alt="Nightly release"></a>
  <a href="https://github.com/optiscaler/OptiScaler/wiki"><img src="https://img.shields.io/badge/Documentation-blue?style=for-the-badge&logo=gitbook&logoColor=white&logoSize=auto" alt="Wiki"></a>
</div>
<div align="center">
  <a href="https://github.com/optiscaler/OptiScaler/releases"><img src="https://img.shields.io/github/downloads/optiscaler/optiscaler/total?style=for-the-badge&logo=gitextensions&logoSize=auto&label=Total" alt="Total DL"></a>
  <a href="https://github.com/optiscaler/OptiScaler/releases/latest"><img src="https://img.shields.io/github/downloads/optiscaler/optiscaler/latest/total?style=for-the-badge&logo=gitextensions&logoSize=auto&label=Stable&color=green&logoColor=white" alt="Stable DL"></a>
  <a href="https://github.com/optiscaler/OptiScaler/releases/tag/nightly"><img src="https://img.shields.io/github/downloads/optiscaler/OptiScaler/nightly/total?style=for-the-badge&logo=gitextensions&logoColor=white&logoSize=auto&label=Nightly&color=purple" alt="Nightly DL"></a>
  <a href="https://github.com/optiscaler/OptiScaler/stargazers"><img src="https://img.shields.io/github/stars/optiscaler/optiscaler?style=for-the-badge&logo=githubsponsors&logoColor=white&label=S.T.A.R.S." alt="Stars"></a>
</div>


## About

**OptiScaler** is a tool that lets you replace upscalers in games that ***already support DLSS2+ / FSR2+ / XeSS*** ($`^1`$), as well as manage ***frame generation*** in already mentioned games _(either by replacing existing FG options or enabling it in DX12 games through experimental ***OptiFG***)_. It also offers extensive customization options for all users, including those with Nvidia GPUs using DLSS.

> [!CAUTION]
> * We've been informed about some **FAKE websites** presenting themselves as OptiScaler team, so we would like to strongly highlight that we **DO NOT HAVE an official website!**  
> * We **DON'T have an official manager app**, so please be careful when downloading or using them! And please don't bother us to provide support for something which isn't even ours!
> * Only **LEGIT places** are this Github, our Discord server and Nitec's NexusMods page.  
> * OptiScaler is **FREE**, any kind of monetary requirements are scams!  

> [!TIP]
> _For example, if a game has DLSS only, OptiScaler can be used to replace DLSS with XeSS or FSR 3.1 (also works for FSR2-only games, like The Outer Worlds Spacer's Choice, albeit requires manually providing nvngx_dlss.dll)._

**Key aspects of OptiScaler:**
- Enables usage of XeSS, FSR2, FSR3, **FSR4**$`^2`$ (_officially, RDNA4 and RDNA3 dGPUs only_) and DLSS in (temporal) upscaler-enabled games
- Allows users to fine-tune their upscaling experience with a wide range of tweaks and enhancements (RCAS & MAS, Output Scaling, DLSS Presets, Ratio & DRS Overrides etc.)
- Since v0.7.0+, added ***experimental DX12*** frame generation support with possible HUDfix solution ([**OptiFG**](#optifg--hudfix-experimental-hud-ghosting-fix))
- Supports [**Fakenvapi**](#installation) integration - enables Reflex hooking and injecting _Anti-Lag 2_ (RDNA1+ only), _LatencyFlex_ (LFX) or _XeLL_ - _bundled since 0.9_  
- Since v0.7.7, added support for **Nukem's** FSR3-FG mod [**dlssg-to-fsr3**](#installation), only supports games with ***native DLSS-FG*** - _bundled since 0.9_
- Since v0.7.8, added **ASI plugin loading** support (_disabled_ by default (`LoadAsiPlugins=` in INI), loads from customisable folder, default `plugins`)
- New project - [**OptiPatcher**](https://github.com/optiscaler/OptiPatcher) - an ASI Plugin for OptiScaler for enabling DLSS and DLSSG inputs without spoofing in ***supported games***.
- Since v0.7.8, OptiScaler is now automatically applying certain game patches for a better out-of-the-box experience
- Since v0.9.0, separated FG Inputs and Outputs, added XeFG and FSR4-FG support, as well as bundled Fakenvapi and Nukem's FSR3-FG mod
- For a detailed list of all features, check [Features](Features.md)


> [!IMPORTANT]
> _**Always check the [Wiki Compatibility list](https://github.com/optiscaler/OptiScaler/wiki) for known game issues and workarounds.**_  
> Also please check the  [***OptiScaler known issues***](#known-issues) at the end regarding **RTSS** compatibility.  
> A separate [***FSR4 Compatibility list***](https://github.com/optiscaler/OptiScaler/wiki/FSR4-Compatibility-List) is available for community-sourced tested games.  
> ***[3]** For **not bundled** items, please check [Installation](#installation).*  

> [!NOTE]
> ### Upscaler notes
> <details>
>  <summary><b>Click for [1], [2] </b></summary>  
>  
> **[1]** For **Unreal Engine** games, only UE XeSS -> Opti XeSS/FSR4 work  
>  
> *Regarding **XeSS** inputs, since **Unreal Engine plugin** does not provide depth, replacing in-game XeSS breaks other upscalers (e.g. Redout 2 as a XeSS-only game), but you can still apply RCAS sharpening to XeSS to reduce blurry visuals.* 
>
> *Regarding **FSR inputs**, FSR 3.1 is the first version with a fully standardised, forward-looking API and should be fully supported. Since FSR2 and FSR3 support custom interfaces, game support will depend on the developers' implementation. With Unreal Engine games, you might need [ini tweaks](https://github.com/optiscaler/OptiScaler/wiki/Unreal-Engine-Tweaks) for FSR inputs.*  
>
> **[2]** *Regarding **FSR4**, please check [FSR4 Compatibility list](https://github.com/optiscaler/OptiScaler/wiki/FSR4-Compatibility-List) for known supported games and general info.*
> 
> </details>


## Official Discord Server: [OptiScaler](https://discord.gg/wEyd9w4hG5)

*This project is based on [PotatoOfDoom](https://github.com/PotatoOfDoom)'s excellent [CyberFSR2](https://github.com/PotatoOfDoom/CyberFSR2).*

## How it works?
* OptiScaler acts as a middleware, it intercepts upscaler calls from the game (_**Inputs**_) and redirects them to the chosen upscaling backend (_**Output**_), allowing user to replace one technology with another one. **Inputs -> OptiScaler -> Outputs**  
* _Or put more bluntly, **Input** is the upscaler used in game settings, and **Output** the one selected in Opti Overlay._
* _Same goes for FG options which are separated into **FG Input** and **FG Output**._

> [!NOTE]
> * Pressing **`Insert`** should open the Optiscaler **Overlay** in-game with all of the options (_`ShortcutKey=` can be changed in the INI file, or under **Keybinds** in the overlay_). 
> * Pressing **`Page Up`** shows the performance stats overlay in the top left, and can be cycled between different modes with **`Page Down`** (_keybinds customisable in the overlay_).  
> * If Opti overlay is instantly disappearing after trying Insert a few times, maybe try **`Alt + Insert`** ([reported workaround](https://github.com/optiscaler/OptiScaler/issues/484) for alternate keyboard layouts).

![inputs_and_outputs](https://github.com/user-attachments/assets/7ff37fd7-515f-488d-99ff-faa586e206fc)

## Which APIs and Upscalers are Supported?
Currently **OptiScaler** can be used with DirectX 11, DirectX 12 and Vulkan, but each API has different sets of supported upscalers.  
[**OptiFG**](#optifg--hudfix-experimental-hud-ghosting-fix) currently **only supports DX12** and is explained in a separate paragraph.

#### For DirectX 12
- XeSS (Default)
- FSR 2.1.2, 2.2.1
- FSR 3.X (and FSR 2.3.X)
- FSR 4.X (via FSR 3.X/4, _officially RDNA4 and RDNA3 dGPUs only_)
- DLSS

#### For DirectX 11
- FSR 2.2.1 (Default, native DX11)
- FSR 3.1.2 (unofficial port to native DX11)
- DLSS (native DX11)
- XeSS 2.X (native DX11, _Intel ARC only_)
- XeSS, FSR 2.1.2, 2.2.1, FSR 3.X w/Dx12 (_via D3D11on12_)$`^1`$
- FSR 4.X (via FSR 3.X/4 w/Dx12 interop, _officially RDNA4 and RDNA3 dGPUs only_)

> [!NOTE]
> <details>
>  <summary><b>Expand for [1]</b></summary>
>
> _**[1]** These implementations use a background DirectX12 device to be able to use DX12-only upscalers. There's a performance penalty up to 10-ish % for this method, but allows many more upscaler options. Also native DX11 implementation of FSR 2.2.1 is a backport from Unity renderer and has its own problems of which some were fixed by OptiScaler._
> </details>

#### For Vulkan
- FSR 4.X (via FSR 3.X/4 w/Dx12 interop, _officially RDNA4 and RDNA3 dGPUs only_)
- FSR2 2.1.2 (Default), 2.2.1
- FSR3 3.1 (and FSR2 2.3.2)
- DLSS
- XeSS 2.x

#### OptiFG + HUDfix (experimental HUD ghosting fix) 
**OptiFG** was added with **v0.7** and is **only supported in DX12**. 
It's an **experimental** way of adding FG to games without native Frame Generation, or can also be used as a last case scenario if the native FG is not working properly.  
* Currently supports FSR3-FG (requires HUDfix to avoid HUD ghosting), XeFG and FSR4-FG (ML model deals with the HUD, so may or may not require HUDfix).

For more information on OptiFG and how to use it, please check the Wiki page - [OptiFG](https://github.com/optiscaler/OptiScaler/wiki/OptiFG).


## Installation
> [!CAUTION]
> _**Warning**: **Do not use this mod with online games.** It may trigger anti-cheat software and cause bans!_

> [!IMPORTANT]
> **For installation steps, please check the [**Wiki**](https://github.com/optiscaler/OptiScaler/wiki)**  

## Configuration
Please check [this](Config.md) document for configuration parameters and explanations. If your GPU is not an Nvidia one, check [GPU spoofing options](Spoofing.md) *(Will be updated)*

## Known Issues

> [!NOTE]
> **For a list of known issues, please check the [**Wiki**](https://github.com/optiscaler/OptiScaler/wiki)**.
> 
> Also worth checking the [Compatibility List](https://github.com/optiscaler/OptiScaler/wiki/Compatibility-List) for possible game issues and their fixes.

## Compilation

### Requirements
* Visual Studio 2022

### Instructions
* Clone this repo with **all of its submodules**.
* Open the OptiScaler.sln with Visual Studio 2022.
* Build the project

## Thanks
* @PotatoOfDoom for CyberFSR2
* @Artur for DLSS Enabler and helping me implement NVNGX api correctly
* @LukeFZ & @Nukem for their great mods and sharing their knowledge 
* @FakeMichau for continous support, testing and feature creep
* @QM for continous testing efforts and helping me to reach games
* @TheRazerMD for continous testing and support
* @Cryio, @krispy, @krisshietala, @Lordubuntu, @scz, @Veeqo for their hard work on (now outdated) [compatibility matrix](https://docs.google.com/spreadsheets/d/1qsvM0uRW-RgAYsOVprDWK2sjCqHnd_1teYAx00_TwUY)
* And the whole DLSS2FSR community for all their support

## Credit
This project uses [FreeType](https://gitlab.freedesktop.org/freetype/freetype) licensed under the [FTL](https://gitlab.freedesktop.org/freetype/freetype/-/blob/master/docs/FTL.TXT)

## Sponsors
<table>
 <tbody>
  <tr>
   <td align="center"><img alt="[SignPath]" src="https://avatars.githubusercontent.com/u/34448643" height="30"/></td>
   <td>Free code signing on Windows provided by <a href="https://signpath.io/">SignPath.io</a>, certificate by <a href="https://signpath.org/">SignPath Foundation</a></td>
  </tr>
 </tbody>
</table>

