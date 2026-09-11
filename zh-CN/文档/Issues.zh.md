# 已知问题

> 原文：[Issues.md](https://github.com/OptiScaler/OptiScaler/blob/master/Issues.md) | 中文翻译仅供参考

## 游戏内菜单

如果无法打开游戏内菜单，请依次排查：

1. 确认你已在游戏选项中启用了 DLSS、XeSS 或 FSR
2. 如果使用旧版安装方式，请在**游戏进行中**（有 3D 渲染发生时）尝试打开菜单
3. 如果你正在使用 RTSS（MSI Afterburner、CapFrameX），请开启 RTSS 的下图所示设置，并尝试更新 RTSS。
   ![RTSS 设置](https://github.com/optiscaler/OptiScaler/assets/35529761/8afb24ac-662a-40ae-a97c-837369e03fc7)

* 有些游戏不会释放鼠标控制，这种情况下键盘和手柄操作通常仍然可用。
* 在某些系统与游戏的组合下，打开旧版游戏内菜单可能导致游戏崩溃或画面错乱（尤其在虚幻引擎 5 游戏中）。

![Banishers 示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/banishers.png)<br>*《Banishers: Ghosts of New Eden》*

* 修改设置大多数情况没问题，但可能导致崩溃（尤其是切换后端或重新初始化后端时）。
* 在 Unity 引擎游戏中，旧版游戏内菜单会上下颠倒。

![画面颠倒示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/upsidedown.png)<br>*《森林之子（Sons of the Forest）》*

## DirectX 11 借助 DirectX12 的超分方案

这类实现通过后台 DirectX12 设备来使用仅支持 DX12 的超分方案。此方法有约 10%–15% 的性能损失，但能提供更多超分选择。

## 曝光纹理（Exposure Texture）

有时游戏的曝光纹理格式无法被超分器识别。最常见表现为颜色被"压碎"（尤其在暗部区域）。

![曝光问题示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/exposure.png)<br>*《古墓丽影：暗影》*

大多数情况下，在 `OptiScaler.ini` 中启用 `AutoExposure=true`，或在游戏内菜单的 `Init Parameters` 中选择 `Auto Exposure`，即可解决。

## 资源屏障（Resource Barriers）

已知虚幻引擎的 DLSS 插件会以错误的状态发送资源。通常 OptiScaler 会从 NVSDK 检查引擎信息，并为虚幻引擎游戏自动启用必要的修复，但有些游戏上报的引擎信息不正确。此问题通常表现为屏幕底部出现彩色色块。

![彩色色块示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/christmas.png)<br>*《深岩银河（Deep Rock Galactic）》*

解决方法：在 `OptiScaler.ini` 中设置 `ColorResourceBarrier=4`，或在游戏内菜单的 `Resource Barriers (Dx12)` 中把 `Color` 选为 `RENDER_TARGET`。

## XeSS 黑屏/花屏或崩溃

有用户反馈使用 XeSS 超分后端时出现黑屏/花屏（仅 UI 可见）或崩溃（例如《漫威银河护卫队》）。在某些情况下，下载最新版 [DirectX Shader Compiler](https://github.com/microsoft/DirectXShaderCompiler/releases)，并把其中 `bin\x64\` 下的 `dxcompiler.dll`、`dxil.dll` 解压到游戏 exe 旁，即可解决。

## Minecraft RTX

XeSS 1.1 与《我的世界 RTX》兼容性最好。但也有反馈称，借助[各种启动器](https://github.com/MCMrARM/mc-w10-version-launcher/releases)可以使用 1.2 及以上版本。

## Linux 上的着色器编译错误

如果你在 Linux 上使用 OptiScaler，并且在使用 `RCAS`、`Reactive Mask Bias` 或 `Output Scaling` 时遇到问题，日志中大概率会出现如下信息：

```
CompileShader error compiling shader : <anonymous>:83:26: E5005: Function "rcp" is not defined.
```

解决方法：使用菜单中的 `Precompiled Shaders`（预编译着色器）选项，或通过 `WineTricks` / `ProtonTricks` 安装 `d3dcompiler_47`。OptiScaler 的这些功能使用自定义着色器，并依赖该编译器文件在运行时编译着色器。

## 性能问题

* 总体而言，XeSS 对 GPU 的负担比 FSR 更重，即使在 Intel Arc 显卡上，性能更低也是正常现象。
* 由于伪装成 Nvidia 显卡以启用 DLSS，一些游戏会走 Nvidia 优化过的代码路径，可能导致在其他显卡上性能下降。

## 显示分辨率运动向量（Display Resolution Motion Vectors）

有时游戏会设置错误的 `DisplayResolution` 初始化标志，导致过度动态模糊。开启或重置 `DisplayResolution` 有助于解决。

![运动向量问题示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/mv_wrong.png)<br>*《深岩银河（Deep Rock Galactic）》*

## 画面错乱与崩溃

如前所述，伪装 Nvidia 显卡可能让游戏走上特殊代码路径，造成画面错乱。如有可能，请禁用伪装，在这些情况下改用 FSR 或 XeSS 输入。

![画面错乱示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/talos.png)<br>*《塔罗斯的法则 2（The Talos Principle 2）》*

* 还有崩溃问题，尤其是开启光线追踪时。
