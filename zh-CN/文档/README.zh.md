# 关于 OptiScaler

> 原文：[README.md](https://github.com/OptiScaler/OptiScaler/blob/master/README.md) | 中文翻译仅供参考

## 目录

1. [关于](#关于)
2. [工作原理](#工作原理)
3. [支持的 API 和超分技术](#支持哪些-api-和超分技术)
4. [安装](#安装)
5. [已知问题](#已知问题)
6. [编译与致谢](#编译)
7. [Wiki（英文）](https://github.com/optiscaler/OptiScaler/wiki)

## 关于

**OptiScaler** 是一款工具，可以让玩家在 ***已支持 DLSS2+ / FSR2+ / XeSS***（注1）的游戏中**替换超分辨率方案**，并管理这些游戏的***帧生成***功能 _（既可以替换游戏自带的帧生成选项，也可以通过实验性的 ***OptiFG*** 为 DX12 游戏开启帧生成）_。它还为所有用户提供了丰富的自定义选项，包括使用 Nvidia 显卡、走 DLSS 路线的用户。

> [!CAUTION] ⚠️ 防诈骗提醒
> * 我们注意到有一些**假冒网站**自称是 OptiScaler 团队，因此在此强烈声明：我们**没有官方网站！**
> * 我们**没有官方管理器应用**，下载或使用此类软件请务必小心！也请不要为那些根本不是我们做的软件来找我们要支持！
> * 只有**正规渠道**：本 GitHub 仓库、我们的 Discord 服务器、Nitec 的 NexusMods 页面。
> * OptiScaler **完全免费**，任何形式的收费都是诈骗！

> [!TIP] 💡 举个例子
> 如果某款游戏只有 DLSS，OptiScaler 可以把 DLSS 替换成 XeSS 或 FSR 3.1（对只有 FSR2 的游戏同样有效，例如《天外世界：太空之选版》，但需要手动提供 nvngx_dlss.dll）。

**OptiScaler 的核心亮点：**

- 在有（时间性）超分选项的游戏中启用 XeSS、FSR2、FSR3、**FSR4**（注2，_官方仅支持 RDNA4 和 RDNA3 独显_）以及 DLSS
- 提供大量微调与增强选项，让玩家自定义超分体验（RCAS & MAS 锐化、输出缩放、DLSS 预设、比例与 DRS 覆盖等）
- 自 v0.7.0 起，加入***实验性 DX12*** 帧生成支持，并附带可能的 HUD 修复方案（[**OptiFG**](#optifg--hudfix实验性-hud-残影修复)）
- 支持 [**Fakenvapi**](#安装) 集成——启用 Reflex 钩子并注入 _Anti-Lag 2_（仅 RDNA1+）、_LatencyFlex_（LFX）或 _XeLL_——_自 0.9 起内置_
- 自 v0.7.7 起，支持 **Nukem 的** FSR3-FG 模组 [**dlssg-to-fsr3**](#安装)，仅支持***原生 DLSS-FG*** 的游戏——_自 0.9 起内置_
- 自 v0.7.8 起，支持 **ASI 插件加载**（默认_关闭_，可通过 INI 中的 `LoadAsiPlugins=` 开启，从可自定义的目录加载，默认为 `plugins`）
- 新项目——[**OptiPatcher**](https://github.com/optiscaler/OptiPatcher)——一个 OptiScaler 的 ASI 插件，可在***受支持的游戏***中无需伪装即可启用 DLSS 与 DLSSG 输入
- 自 v0.7.8 起，OptiScaler 会自动为部分游戏打补丁，提供更好的开箱即用体验
- 自 v0.9.0 起，帧生成输入与输出分离，加入 XeFG 和 FSR4-FG 支持，并内置 Fakenvapi 与 Nukem 的 FSR3-FG 模组
- 完整功能列表请查看 [功能特性（Features.md 中文版）](Features.zh.md)

> [!IMPORTANT] ❗ 重要
> _**使用前请务必查看 [Wiki 兼容性列表](https://github.com/optiscaler/OptiScaler/wiki)，了解已知的游戏问题与解决方法。**_
> 另请查看文末关于 **RTSS** 兼容性的 [***OptiScaler 已知问题***](Issues.zh.md)。
> 社区维护的 FSR4 游戏测试列表见：[***FSR4 兼容性列表***](https://github.com/optiscaler/OptiScaler/wiki/FSR4-Compatibility-List)。
> ***[3]*** 对于**未内置**的组件，请查看[安装](#安装)部分。

> [!NOTE] 📝 超分技术补充说明
>
> <details>
> <summary><b>点击展开 注1、注2</b></summary>
>
> **[1]** 对于 **Unreal Engine（虚幻引擎）** 游戏，只有 UE 的 XeSS → Opti 的 XeSS/FSR4 可用。
>
> *关于 **XeSS 输入**：由于虚幻引擎插件不提供深度信息，替换游戏内的 XeSS 会导致其他超分方案失效（例如只支持 XeSS 的《Redout 2》），但你仍然可以对 XeSS 应用 RCAS 锐化来缓解画面模糊。*
>
> *关于 **FSR 输入**：FSR 3.1 是第一个完全标准化、面向未来的 API 版本，应当能被完整支持。由于 FSR2 和 FSR3 支持自定义接口，具体支持情况取决于开发者的实现方式。虚幻引擎游戏可能需要对 FSR 输入进行 [ini 调整](https://github.com/optiscaler/OptiScaler/wiki/Unreal-Engine-Tweaks)。*
>
> **[2]** *关于 **FSR4**，请查看 [FSR4 兼容性列表](https://github.com/optiscaler/OptiScaler/wiki/FSR4-Compatibility-List) 了解已支持的游戏与相关信息。*
>
> </details>

## 官方 Discord 服务器：[OptiScaler](https://discord.gg/wEyd9w4hG5)

*本项目基于 PotatoOfDoom 的优秀项目 [CyberFSR2](https://github.com/PotatoOfDoom/CyberFSR2)。*

## 工作原理

* OptiScaler 充当中间件：拦截游戏发出的超分调用（_**输入 / Input**_），并把它们转发给所选的超分后端（_**输出 / Output**_），从而让玩家把一种超分技术替换成另一种。流程为：**输入 → OptiScaler → 输出**
* _说得直白一点：**输入**就是游戏设置里选择的超分方案，**输出**就是你在 OptiScaler 覆盖层（Overlay）里选择的方案。_
* _帧生成选项同理，分为 **帧生成输入（FG Input）** 和 **帧生成输出（FG Output）**。_

> [!NOTE] 📝
> * 按 **`Insert`** 键应可在游戏中打开 OptiScaler **覆盖层菜单**（`ShortcutKey=` 可在 INI 文件中修改，或在覆盖层的 **Keybinds** 中修改）。
> * 按 **`Page Up`** 会在左上角显示性能统计覆盖层，按 **`Page Down`** 可在不同模式间切换（按键均可在覆盖层中自定义）。
> * 如果按 Insert 几次后 Opti 覆盖层都一闪而过/立即消失，可以试试 **`Alt + Insert`**（针对部分键盘布局的[已知解决方法](https://github.com/optiscaler/OptiScaler/issues/484)）。

![输入与输出示意图](https://github.com/user-attachments/assets/7ff37fd7-515f-488d-99ff-faa586e206fc)

## 支持哪些 API 和超分技术？

目前 **OptiScaler** 可用于 DirectX 11、DirectX 12 和 Vulkan，但每种 API 支持的超分方案不同。
[**OptiFG**](#optifg--hudfix实验性-hud-残影修复) 目前**仅支持 DX12**，详见后文单独段落。

#### DirectX 12

- XeSS（默认）
- FSR 2.1.2、2.2.1
- FSR 3.X（以及 FSR 2.3.X）
- FSR 4.X（通过 FSR 3.X/4，_官方仅支持 RDNA4 和 RDNA3 独显_）
- DLSS

#### DirectX 11

- FSR 2.2.1（默认，原生 DX11）
- FSR 3.1.2（非官方移植的原生 DX11 版）
- DLSS（原生 DX11）
- XeSS 2.X（原生 DX11，_仅 Intel ARC 显卡_）
- XeSS、FSR 2.1.2、2.2.1、FSR 3.X（DX12 版，_通过 D3D11on12_）（注1）
- FSR 4.X（通过 FSR 3.X/4 的 DX12 互操作，_官方仅支持 RDNA4 和 RDNA3 独显_）

> [!NOTE] 📝
> <details>
> <summary><b>点击展开 注1</b></summary>
>
> _**[1]** 这些实现通过在后台创建 DirectX12 设备来使用仅支持 DX12 的超分方案。此方法会有约 10% 左右的性能损失，但换来更多超分选项。另外，原生 DX11 版 FSR 2.2.1 是从 Unity 渲染器反向移植的，自身存在一些问题，OptiScaler 已修复其中一部分。_
>
> </details>

#### Vulkan

- FSR 4.X（通过 FSR 3.X/4 的 DX12 互操作，_官方仅支持 RDNA4 和 RDNA3 独显_）
- FSR2 2.1.2（默认）、2.2.1
- FSR3 3.1（以及 FSR2 2.3.2）
- DLSS
- XeSS 2.x

#### OptiFG + HUDfix（实验性 HUD 残影修复）

**OptiFG** 于 **v0.7** 加入，**仅支持 DX12**。
它是一种**实验性**手段，可为没有原生帧生成的游戏添加帧生成；也可以在原生帧生成工作不正常时作为最后的兜底方案。

* 目前支持 FSR3-FG（需要开启 HUDfix 以避免 HUD 残影）、XeFG 和 FSR4-FG（由 ML 模型处理 HUD，可能需要也可能不需要 HUDfix）。

更多关于 OptiFG 的信息与使用方法，请查看 Wiki 页面：[OptiFG（英文）](https://github.com/optiscaler/OptiScaler/wiki/OptiFG)。

## 安装

> [!CAUTION] ⚠️ 警告
> _**切勿在联机游戏中使用本模组！** 它可能触发反作弊系统并导致封号！_

> [!IMPORTANT] ❗
> **具体安装步骤请查看 [Wiki（英文）](https://github.com/optiscaler/OptiScaler/wiki)**

## 配置

配置参数与详细说明请查看 [配置说明（Config.md 中文版）](Config.zh.md)。如果你的显卡不是 Nvidia 的，请查看 [GPU 伪装选项（Spoofing.md 中文版）](Spoofing.zh.md) _（英文原文标注：将会更新）_。

## 已知问题

> [!NOTE] 📝
> **已知问题列表请查看 [Wiki（英文）](https://github.com/optiscaler/OptiScaler/wiki)**。
>
> 另外建议查看 [兼容性列表](https://github.com/optiscaler/OptiScaler/wiki/Compatibility-List)，了解可能的兼容性问题及修复方法。

## 编译

### 环境要求

* Visual Studio 2022

### 步骤

* 克隆本仓库时**务必连同所有子模块（submodules）一起**。
* 用 Visual Studio 2022 打开 OptiScaler.sln。
* 编译项目即可。

## 鸣谢

* @PotatoOfDoom——CyberFSR2
* @Artur——DLSS Enabler，以及帮助我正确实现 NVNGX API
* @LukeFZ 与 @Nukem——出色的模组与知识分享
* @FakeMichau——持续的支持、测试与功能推进
* @QM——持续的测试工作，帮我接触到许多游戏
* @TheRazerMD——持续的测试与支持
* @Cryio、@krispy、@krisshietala、@Lordubuntu、@scz、@Veeqo——在（现已过时的）[兼容性矩阵](https://docs.google.com/spreadsheets/d/1qsvM0uRW-RgAYsOVprDWK2sjCqHnd_1teYAx00_TwUY)上的辛勤付出
* 以及整个 DLSS2FSR 社区的支持

## 版权说明

本项目使用了 [FreeType](https://gitlab.freedesktop.org/freetype/freetype)，遵循 [FTL 许可证](https://gitlab.freedesktop.org/freetype/freetype/-/blob/master/docs/FTL.TXT)。

## 赞助者

<table>
 <tbody>
  <tr>
   <td align="center"><img alt="SignPath" src="https://avatars.githubusercontent.com/u/34448643" height="30"/></td>
   <td>Windows 平台的免费代码签名由 <a href="https://signpath.io/">SignPath.io</a> 提供，证书由 <a href="https://signpath.org/">SignPath Foundation</a> 颁发</td>
  </tr>
 </tbody>
</table>
