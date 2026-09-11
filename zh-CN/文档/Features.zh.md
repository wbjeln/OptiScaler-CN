# 功能特性

> 原文：[Features.md](https://github.com/OptiScaler/OptiScaler/blob/master/Features.md) | 中文翻译仅供参考

## 功能列表

* 支持多种超分后端（XeSS、FSR 2.1.2、FSR 2.2.1、FSR 3.1 与 DLSS）
* 0.7.0 及以上版本提供实验性帧生成支持（OptiFG，基于 FSR）
* 支持 DLSS 3.7 及以上版本（请查看[安装说明](https://github.com/OptiScaler/OptiScaler#install-as-non-nvngx)）
* 在 Nvidia 显卡上支持 DLSS-D（光线重建 / Ray Reconstruction）（支持切换预设并使用 OptiScaler 增强）
* 可实时修改 DLSS / DLSS-D 预设
* 支持 XeSS v1.3.x 的 Ultra Performance、NativeAA 模式（**注意：不使用 XeSS 1.3.x 的默认缩放比例，而是沿用旧版比例**）
* 提供[游戏内菜单](Config.zh.md)，可实时调节并保存设置（快捷键为 **INSERT**）
* 与 [DLSS Enabler](https://www.nexusmods.com/site/mods/757) 完全集成，支持 DLSS-FG
* 为所有 DX12 与 DX11 超分后端提供 **RCAS** 锐化与 **MAS**（运动自适应锐化，Motion Adaptive Sharpening）支持
* 为运行于 DX12 与 DX11 的后端提供 **输出缩放（Output Scaling）** 选项（0.5x 至 3.0x）
* 支持 DXGI 伪装（以 `dxgi.dll` 方式运行时），伪装成 Nvidia 显卡（并带有 XeSS 检测，可在 Intel Arc 显卡上启用 XMX）
* 支持 Vulkan 伪装（需在 `nvngi.ini` 中启用），伪装成 Nvidia 显卡（在《毁灭战士：永恒》中无效）
* 支持加载指定的 `nvapi64.dll` 文件（非 nvngx 模式下）
* 支持加载指定的 `nvngx_dlss.dll` 文件（非 nvngx 模式下）
* 支持覆盖缩放比例（Upscaling Ratios）
* 支持 DRS 范围覆盖
* 针对虚幻引擎 + AMD 显卡的[彩色灯光问题](Config.zh.md)自动修复
* 针对[曝光纹理（exposure texture）信息缺失](Config.zh.md)的自动修复
* 可修改游戏中的 [Mipmap Lod Bias](Config.zh.md) 值
* 支持 [Fakenvapi](https://github.com/FakeMichau/fakenvapi) 集成，启用 Reflex 钩子并注入 Anti-Lag 2 或 LatencyFlex（LFX）
* 支持 Nukem 的 FSR 帧生成模组 [dlssg-to-fsr3](https://github.com/Nukem9/dlssg-to-fsr3)（自 0.7.7 版起）

**为绕过 DLSS 3.7 的签名校验要求，OptiScaler 采用了 [DLSS Enabler](https://www.nexusmods.com/site/mods/757?tab=description) 作者 **Artur** 开发的方法。**
