# 配置说明

> 原文：[Config.md](https://github.com/OptiScaler/OptiScaler/blob/master/Config.md) | 中文翻译仅供参考

本文档将尽可能详细地解释 `OptiScaler.ini` 以及游戏内菜单（打开菜单的快捷键为 **INSERT**）中的各项设置。

![游戏内菜单](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/menu043.png)

### 超分方案（Upscalers）

OptiScaler 支持 DirectX 11、DirectX 12 和 Vulkan 三种 API，并提供多种超分后端。你可以在 `OptiScaler.ini` 文件的 `[Upscalers]` 部分选择使用哪种超分方案。

```ini
[Upscalers]
; 为 DX11 游戏选择超分方案
; 可选：fsr22（原生 DX11）、xess（借助 DX12）、fsr21_12（DX11 借助 DX12）或 fsr22_12（DX11 借助 DX12）
; 默认（auto）为 fsr22
Dx11Upscaler=auto

; 为 DX12 游戏选择超分方案
; 可选：xess、fsr21 或 fsr22
; 默认（auto）为 xess
Dx12Upscaler=auto

; 为 Vulkan 游戏选择超分方案
; 可选：fsr21 或 fsr22
; 默认（auto）为 fsr21
VulkanUpscaler=auto
```

* `fsr21` 表示 FSR 2.1.2
* `fsr22` 表示 FSR 2.2.1
* `xess` 表示 XeSS

*对于 DirectX11，`fsr21_12`、`fsr22_12` 和 `xess` 这几个选项需要借助一个后台 DirectX12 设备来使用仅支持 DX12 的超分方案。此方法有约 10%–15% 的性能损失，但能提供更多超分选择。此外，原生 DX11 版 FSR 2.2.1 是从 Unity 渲染器反向移植的，自身存在一些问题，OptiScaler 规避了其中一部分。*

在游戏内菜单的 `Upscalers` 部分也可以选择超分方案。

![超分选择界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/Upscalers.png)

### 伪超采样（Pseudo SuperSampling）

从 OptiScaler 0.4 开始，`[Upscalers]` 下新增了伪超采样（伪超级采样）选项：

```ini
[Upscalers]
; 为 DX12 后端及"DX11 借助 DX12"的后端启用伪超采样
; true 或 false - 默认（auto）为 false
SuperSamplingEnabled=auto

; 伪超采样倍率
; 0.0 - 5.0 - 默认（auto）为 2.5
SuperSamplingMultiplier=auto
```

举例说明：假设游戏运行在 1080p，DLSS 预设选择 `Quality`，游戏会渲染一张 720p 的画面，连同其他必要输入信息一起交给超分器，输出 1080p 的画面。

如果开启伪超采样，则会用 `SuperSamplingMultiplier` 来计算超分器的目标渲染尺寸。以 720p 输入、默认倍率 2.5 为例，目标为 1800p。也就是说，超分器会把画面放大到 1800p 而不是 1080p，然后再由 OptiScaler 把输出画面降采样回 1080p。

![伪超采样示意图](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/pss.png)

由于超分目标分辨率更高，相比普通超分会有一定性能损失。但主观画质上，它可以以更高的性能档位接近 DLAA 的效果。

该选项可在游戏内菜单中实时调整。

![伪超采样配置](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/pss_config.png)

### Dx11withDx12 同步设置

对于 DirectX11 使用 `fsr21_12`、`fsr22_12` 和 `xess` 超分选项的情况，OptiScaler 会借助一个后台 DirectX12 设备来使用这些仅支持 DX12 的超分方案。这是一个非常小众的功能，在不稳定的 GPU 驱动上（尤其是 Intel）可能出问题。为了缓解或防止崩溃和画面异常，可以使用以下选项。

```ini
[Dx11withDx12]
; "DX11 借助 DX12"的同步方式
;
; 有效值为：
;   0 - 无同步                       （最快，最容易出错）
;   1 - Fence
;   2 - Fences + Flush
;   3 - Fences + Event
;   4 - Fences + Flush + Event
;   5 - 仅 Query

; 默认（auto）为 1
TextureSyncMethod=auto

; 默认（auto）为 5
CopyBackSyncMethod=auto

; 输出回拷同步发生在 Dx12 执行之前还是之后
; true 或 false - 默认（auto）为 true
SyncAfterDx12=auto

; 在创建 D11wDx12 功能时延迟部分操作以提高兼容性
; true 或 false - 默认（auto）为 false
UseDelayedInit=auto
```

下图展示了"Dx11 借助 Dx12"超分流程。黄色圆圈为同步点（或可能的同步点）。`SyncAfterDx12` 决定第二次同步发生的时机。

![dx11 with dx12 流程图](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/Dx11wDx12.png)

* `无同步`：顾名思义。
* `Fence`：使用共享 `Fence`（Signal & Wait）同步，发生在 GPU 上，速度相当快。
* `Fence + Event`：使用共享 `Fence`（Signal & Event）同步，`Event` 需要在 CPU 上等待，速度较慢。
* `Flush`：Signal 共享 Fence 后，Flush DX11 的 DeviceContext。
* `仅 Query`：使用 DX11 `Query` 同步，一般比 `Event` 快，但比 `Fence` 慢。

当使用 `Event` 同步输出时，`SyncAfterDx12=false` 通常性能更好。

**这些设置与游戏和硬件相关。默认值是在性能与画面稳定之间的折中，想要更高性能可能需要针对每个游戏自行微调。**

这些可在游戏内菜单中实时调整（`UseDelayedInit` 除外）。

![dx11 同步设置界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/dx11wdx12menu.png)

### XeSS 设置

```ini
[XeSS]
; 在初始化前预构建 XeSS 管线
; true 或 false - 默认（auto）为 true
BuildPipelines=auto

; 选择 XeSS 网络模型
; 0 = KPSS
; 1 = Splat
; 2 = Model 3
; 3 = Model 4
; 4 = Model 5
; 5 = Model 6
;
; 默认（auto）为 0
NetworkModel=auto

[CAS]
; 为 XeSS 启用 CAS 锐化
; true 或 false - 默认（auto）为 false
Enabled=auto

; 输入和输出的色彩空间转换
; 可选值见文末 - 默认（auto）为 0
ColorSpaceConversion=auto
```

`BuildPipelines` 参数允许在创建上下文时预构建 XeSS 管线，避免之后游戏过程中卡顿。

`NetworkModel` 用于选择 XeSS 超分使用的网络模型。**（目前对超分后的画面没有可见影响）**

#### CAS

XeSS 通常比其他超分方案输出的画面更"软"，且没有自带锐化选项来改善。因此 OptiScaler 允许你对最终画面应用 AMD 的 CAS 锐化滤镜，以平衡 XeSS 偏柔和的观感。不过 CAS 并不完美，在某些游戏中可能引发伪影或问题，例如泛光（Bloom）消失、画面色调偏移，甚至黑屏无图像。

![CAS 示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/cas.png)

1. 泛光效果消失
2. 画面色调改变

`ColorSpaceConversion` 用于修复色彩空间转换问题，但**几乎所有情况下**默认值都能正常工作。

可在游戏内菜单中实时调整。

![xess 设置界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/xess.png)

`Dump` 选项用于调试，会把 XeSS 的输入输出参数和纹理转储（dump）到游戏目录。

### FSR 设置

```ini
[FSR]
; 0.0 至 180.0 - 默认（auto）为 60.0
VerticalFov=auto

; 若未定义垂直 FOV，将用此值计算垂直 FOV
; 0.0 至 180.0 - 默认（auto）为关闭
HorizontalFov=auto
```

为提升画质，可以尝试用这些设置匹配你游戏的垂直或水平 FOV。默认垂直 FOV 为 60°，大多数情况下效果不错。

可在游戏内菜单中实时调整。

![fsr 设置界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/fsr.png)

### 锐度（Sharpness）

DLSS 早期有锐化选项，后来被移除了。因此有的游戏有锐度滑条，有的没有。通过这个选项，你可以关闭或开启最终画面的锐化。FSR 自带锐化，而 XeSS 需要开启上面的 CAS 选项。

```ini
[Sharpness]
; 用固定锐度值覆盖 DLSS 的锐度参数
; true 或 false - 默认（auto）为 false
OverrideSharpness=auto

; 锐化强度
; 取值范围 0.0 到 1.0 - 默认（auto）为 0.3
Sharpness=auto
```

可在游戏内菜单中实时调整。

![锐度设置界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/sharpness.png)

### 超分比例（Upscaling Ratios）

OptiScaler 提供多个覆盖和锁定超分比例的选项。

#### 超分比例覆盖（Upscale Ratio Override）

`UpscaleRatioOverride` 可以为所有画质预设统一指定一个超分比例。

```ini
[UpscaleRatio]
; 设为 true 以启用内部渲染分辨率覆盖
; true 或 false - 默认（auto）为 false
UpscaleRatioOverrideEnabled=auto

; 设为 true 以启用"将 DRS 最大分辨率限制为覆盖比例"功能
; true 或 false - 默认（auto）为 false
DrsMaxOverrideEnabled=auto

; 设置强制使用的超分比例
; 默认（auto）为 1.3
UpscaleRatioOverrideValue=auto
```

可以在游戏内菜单中修改并保存，但通常需要重启游戏或改变分辨率后才生效。

![超分比例界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/us_ratio.png)

#### 画质档位比例覆盖（Quality Ratio Override）

`QualityRatioOverride` 可以为每个画质档位分别覆盖超分比例。

```ini
[QualityOverrides]
; 设为 true 以启用自定义画质档位覆盖
; true 或 false - 默认（auto）为 false
QualityRatioOverrideEnabled=auto

; 为每个画质档位设置自定义超分比例
;
; 默认（auto）值：
; Ultra Quality（超高画质） : 1.3
; Quality（画质）           : 1.5
; Balanced（平衡）          : 1.7
; Performance（性能）       : 2.0
; Ultra Performance（超高性能） : 3.0
QualityRatioUltraQuality=auto
QualityRatioQuality=auto
QualityRatioBalanced=auto
QualityRatioPerformance=auto
QualityRatioUltraPerformance=auto
```

**如果两种覆盖同时启用，`UpscaleRatioOverride` 的优先级高于 `QualityRatioOverride`。**

启用 `DrsMaxOverrideEnabled` 后，对于支持 DRS（动态分辨率缩放）的游戏，会把最大内部渲染分辨率限制为默认渲染分辨率而非显示分辨率——相当于变相禁用 DRS。它对 `QualityRatioOverride` 和 `UpscaleRatioOverride` 均有效。

可以在游戏内菜单中修改并保存，但通常需要重启游戏或改变分辨率后才生效。

![画质比例界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/q_ratio.png)

### 初始化标志（Init Flags）

这些设置允许覆盖 DLSS 的初始化标志（init flags），用于修复某些问题。

```ini
[Depth]
; 强制向初始化标志添加 INVERTED_DEPTH
; true 或 false - 默认（auto）为 DLSS 自身的值
DepthInverted=auto

[Color]
; 强制向初始化标志添加 ENABLE_AUTOEXPOSURE
; 部分虚幻引擎游戏需要此项，可修复颜色问题（尤其是暗部区域）
; true 或 false - 默认（auto）为 DLSS 自身的值
AutoExposure=auto

; 强制向初始化标志添加 HDR_INPUT_COLOR
; true 或 false - 默认（auto）为 DLSS 自身的值
HDR=auto

[MotionVectors]
; 强制向初始化标志添加 JITTERED_MV
; true 或 false - 默认（auto）为 DLSS 自身的值
JitterCancellation=auto

; 强制向初始化标志添加 HIGH_RES_MV
; true 或 false - 默认（auto）为 DLSS 自身的值
DisplayResolution=auto

[Hotfix]
; 强制从初始化标志中移除 RESPONSIVE_PIXEL_MASK
; true 或 false - 默认（auto）为 true
DisableReactiveMask=auto
```

启用 `AutoExposure` 有助于改善画面过暗或颜色发白的问题。

![曝光修复示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/exposure.png)

有反馈称启用 `HDR` 可以改善某些游戏中的紫色偏色。

启用 `DisableReactiveMask` 在部分游戏中对 FSR 后端有帮助，但通常弊大于利，因此默认关闭。

有些游戏可能设置错误的游戏运动向量大小标志，导致镜头移动时出现过度动态模糊。开启或关闭 `DisplayResolution` 可能有助于解决。

![运动向量标志错误示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/mv_wrong.png)

可在游戏内菜单中实时调整。

![初始化标志界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/init_flags.png)

### 资源屏障（Resource Barriers，仅 DX12）

有些游戏（尤其是虚幻引擎）把处于错误状态的输入资源传给 DLSS，导致画面问题（尤其在 AMD 硬件上）。通常 OptiScaler 会尝试检测引擎类型并自动启用对应修复，但有些游戏上报的引擎信息不正确。此时下面的 ini 参数可以帮助解决问题。

![画面异常示例](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/christmas.png)

**⚠️ 在这里设置错误的资源状态可能导致崩溃！**

```ini
[Hotfix]
; 颜色纹理的资源状态修复，用于解决 AMD 显卡上的彩虹色问题（多为虚幻引擎游戏）
; 对于 AMD 上的 UE 游戏，设为 D3D12_RESOURCE_STATE_RENDER_TARGET (4)
; 默认（auto）为禁用状态修正
ColorResourceBarrier=auto

; 运动向量的资源状态，从此状态修正为 D3D12_RESOURCE_STATE_NON_PIXEL_SHADER_RESOURCE（多用于调试）
; 默认（auto）为禁用状态修正
MotionVectorResourceBarrier=auto

; 深度纹理的资源状态，从此状态修正为 D3D12_RESOURCE_STATE_NON_PIXEL_SHADER_RESOURCE（多用于调试）
; 默认（auto）为禁用状态修正
DepthResourceBarrier=auto

; 颜色蒙版纹理的资源状态，从此状态修正为 D3D12_RESOURCE_STATE_NON_PIXEL_SHADER_RESOURCE（多用于调试）
; 默认（auto）为禁用状态修正
ColorMaskResourceBarrier=auto

; 曝光纹理的资源状态，从此状态修正为 D3D12_RESOURCE_STATE_NON_PIXEL_SHADER_RESOURCE（多用于调试）
; 默认（auto）为禁用状态修正
ExposureResourceBarrier=auto

; 输出纹理的资源状态，从此状态修正为 D3D12_RESOURCE_STATE_UNORDERED_ACCESS（多用于调试）
; 默认（auto）为禁用状态修正
OutputResourceBarrier=auto
```

可在游戏内菜单中实时调整。

![资源屏障界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/rb.png)

### Mipmap LOD Bias 覆盖（仅 DX12）

为了获得更清晰的纹理，可以通过此设置覆盖 `MipmapLodBias`。-15 最锐利，+15 最模糊。

```ini
[Hotfix]
; 覆盖纹理的 mipmap lod bias
; -15.0 - 15.0 - 默认（auto）为禁用
MipmapBiasOverride=auto
```

**调整 MipmapLODBias 会影响性能！**

可在游戏内菜单中调整，需要更改分辨率后才会生效。

![mipmap 界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/mipmap.png)

### 恢复根签名（Restore Root Certificates，仅 DX12）

此热修复基于原版 CyberFSR2 的恢复 ComputeRootSignature 逻辑，我还额外加了恢复 ComputeRootSignature 的选项。目前我还没发现有游戏需要这些选项。

```ini
[Hotfix]
; 在超分完成后恢复最后使用的 compute 签名
; true 或 false - 默认（auto）为 false
RestoreComputeSignature=auto

; 在超分完成后恢复最后使用的 graphics 签名
; true 或 false - 默认（auto）为 false
RestoreGraphicSignature=auto
```

可在游戏内菜单中实时调整。

![根签名界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/cs.png)

### 日志（Logging）

```ini
[Log]
; 日志开关
; true 或 false - 默认（auto）为 true
LoggingEnabled=auto

; 日志文件，如未指定则在当前目录生成 log_xess_xxxx.log
;LogFile=./CyberXess.log

; 文件日志的详细级别
; 0 = Trace / 1 = Debug / 2 = Info / 3 = Warning / 4 = Error
; 默认（auto）为 2 = Info
LogLevel=auto

; 输出日志到控制台（出于性能考虑，控制台日志级别始终为 2 (Info)）
; true 或 false - 默认（auto）为 false
LogToConsole=auto

; 输出日志到文件
; true 或 false - 默认（auto）为 false
LogToFile=auto

; 输出日志到 NVNGX API
; true 或 false - 默认（auto）为 false
LogToNGX=auto

; 打开控制台窗口显示日志
; true 或 false - 默认（auto）为 false
OpenConsole=auto
```

可在游戏内菜单中实时调整。

![日志界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/logging.png)

### 菜单（Menu）

```ini
[Menu]
; 游戏内 ImGui 菜单缩放
; 1.0 至 2.0 - 默认（auto）为 1.0
Scale=auto
```

可在游戏内菜单中实时调整。

![菜单缩放界面](https://raw.githubusercontent.com/OptiScaler/OptiScaler/master/images/ui_scale.png)
