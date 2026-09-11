# GPU 伪装（Spoofing）

> 原文：[Spoofing.md](https://github.com/OptiScaler/OptiScaler/blob/master/Spoofing.md) | 中文翻译仅供参考 _（英文原文标注：本文将会更新）_

除了第一代 DLSS2 游戏之外，几乎所有游戏都会对 Nvidia 显卡做某种校验，通过后才会开放 DLSS 选项。
为了绕过这些校验，模组作者们开发了一些工具。

## Windows

### Nvapi（FakeNvapi）

要伪装 Nvapi 调用，可以使用 FakeNvapi。某些游戏（如《古墓丽影：暗影》等）需要它才能开启 DLSS 支持。

另外一个**重大加分项**：最新版 FakeNvapi 增加了对 AMD AntiLag 2 与 LatencyFlex 的支持，可在支持 Nvidia Reflex 的游戏中降低输入延迟。

##### 用法

把 `nvapi64.dll` 放在 OptiScaler 旁边，并在 `OptiScaler.ini` 中设置 `OverrideNvapiDll=true`。注意：仅当 OptiScaler 以 non-nvngx 方式（即不是以 `nvngx.dll` 形式）运行时才有效。

不通过 OptiScaler 单独使用时：
需要把 `nvapi64.dll` 文件放到 `%WINDIR%\System32`，但**请务必小心！**
* 如果你是 Nvidia 用户，请**先备份原始文件**，模组使用结束后再还原。
* 切勿在联机游戏中使用此模组，可能导致反作弊问题甚至封号。

##### 下载

[FakeNvapi](https://github.com/FakeMichau/fakenvapi/releases)

### DXGI

OptiScaler 内置了 DXGI 伪装选项，在以 non-nvngx 方式（非 `nvngx.dll`）运行时默认启用。

#### d3d12-proxy

另外，要伪装 DXGI 适配器校验，也可以使用 d3d12-proxy。这个模组会把你的显卡上报为 RTX 4090。

##### 用法

只需把 dxgi.dll 文件放到游戏可执行文件旁边。

##### 下载

[d3d12-proxy](https://github.com/cdozdil/d3d12-proxy/releases)

### Vulkan

OptiScaler 以 non-nvngx 方式（非 `nvngx.dll`）运行时内置了 Vulkan 伪装选项。
Vulkan 伪装默认关闭，需要时请在 `OptiScaler.ini` 中启用。

```ini
; 启用 Vulkan 的 Nvidia 显卡伪装
; true 或 false - 默认（auto）为 false
Vulkan=auto

; 启用 Vulkan 的 Nvidia 扩展伪装
; true 或 false - 默认（auto）为 false
VulkanExtensionSpoofing=auto
```

#### vulkan-spoofer

另外，要伪装 `GetPhysicalDeviceProperties` 校验，可以使用 vulkan-spoofer。这个模组会把你的显卡上报为 RTX 4090。
兼容性不太稳定：《无人深空》可用（但与最新的 streamline 补丁不兼容），《毁灭战士：永恒》则不可用。

##### 用法

只需把 version.dll 文件放到游戏可执行文件旁边。

##### 下载

[vulkan-spoofer](https://github.com/cdozdil/vulkan-spoofer/releases)

## Linux

在 Linux 上可以直接使用 Wine 和 DXVK 内置的伪装机制。

### DirectX 与 Vulkan

要做 DXGI 和 Vulkan 伪装，只需在游戏可执行文件旁创建一个内容如下的 `dxvk.conf` 文件，或直接从[这里](https://raw.githubusercontent.com/cdozdil/CyberXeSS/imgui-intergration/dxvk.conf)下载：

```ini
dxgi.customVendorId = 10de
dxgi.hideAmdGpu = True
dxgi.hideNvidiaGpu = False
dxgi.customDeviceId = 2684
dxgi.customDeviceDesc = "NVIDIA GeForce RTX 4090"
```

### NVAPI

使用 Proton 时，要伪装 NVAPI，请设置环境变量 `PROTON_FORCE_NVAPI=1`。

## Goghor 的 DLSS Unlocker 模组

Goghor 为大量游戏制作了 DLSS Unlocker 模组，可以在他的 [Nexus 主页](https://www.nexusmods.com/spidermanmilesmorales/users/12564231?tab=user+files&BH=0)找到。
据我所知，对于《毁灭战士：永恒》，他的模组仍然是开启 DLSS 的唯一方法。
