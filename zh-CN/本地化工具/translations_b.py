# -*- coding: utf-8 -*-
"""
OptiScaler 汉化词条 - 第二批：提示语、预设说明、方案说明等长文本
"""

T = {}

# ---------- DLSS / FSR 预设说明 ----------
T.update({
    r"Whatever the game uses": "跟随游戏设置",
    r"Intended for Performance/Balanced/Quality modes.\nAn older variant best suited to combat ghosting...\nRemoved on recent versions!": "面向性能/平衡/画质档位。\n较老的变体，最擅长抑制残影…\n新版驱动中已移除！",
    r"Intended for Ultra Performance mode.\nSimilar to Preset A...\nRemoved on recent versions!": "面向超高性能档位。\n与预设 A 类似…\n新版驱动中已移除！",
    r"Intended for Performance/Balanced/Quality modes.\nGenerally favors current frame information...\nRemoved on recent versions!": "面向性能/平衡/画质档位。\n倾向于使用当前帧信息…\n新版驱动中已移除！",
    r"Default preset for Performance/Balanced/Quality modes;\ngenerally favors image stability.\nRemoved on recent versions!": "性能/平衡/画质档位的默认预设；\n倾向于画面稳定性。\n新版驱动中已移除！",
    r"DLSS 3.7+, a better D preset\nRemoved on recent versions!": "DLSS 3.7+，更好的 D 预设\n新版驱动中已移除！",
    r"Default preset for Ultra Performance and DLAA modes\nRemoved on recent versions!": "超高性能与 DLAA 档位的默认预设\n新版驱动中已移除！",
    r"Similar to preset K. Preset J might exhibit slightly\nless ghosting...\n1st Gen Transformer": "与预设 K 类似。预设 J 的残影可能\n略少一些…\n第一代 Transformer",
    r"Default preset for DLAA/Balanced/Quality modes...\n1st Gen Transformer": "DLAA/平衡/画质档位的默认预设…\n第一代 Transformer",
    r"Default for Ultra Perf mode\n2nd Gen Transformers": "超高性能档位的默认预设\n第二代 Transformer",
    r"Default for Perf mode\n2nd Gen Transformer": "性能档位的默认预设\n第二代 Transformer",
    r"Latest supported by the dll": "该 DLL 支持的最新预设",
    r"Preset A\nRemoved on recent versions!": "预设 A\n新版驱动中已移除！",
    r"Preset B\nRemoved on recent versions!": "预设 B\n新版驱动中已移除！",
    r"Preset C\nRemoved on recent versions!": "预设 C\n新版驱动中已移除！",
    r"Default model, Transformer": "默认模型，Transformer",
    r"Latest Transformer model\nMust use if DoF guide is needed": "最新的 Transformer 模型\n需要景深引导时必须使用",
    r"Preset 3 is meant for Performance\n": "预设 3 面向性能档位\n",
    r"Preset 4 is meant for DRS\n": "预设 4 面向动态分辨率（DRS）\n",
    r"Preset 5 is meant for Ultra Performance": "预设 5 面向超高性能档位",
    r"Bottom right: Detail Protection Takedown": "右下角：细节保护取舍视图",
    r"with value close to 1.0f can decrease temporal ghosting.\n": "值接近 1.0f 时可减轻时间性残影。\n",
    r"Decreasing this could result in more thin feature pixels flickering.": "调低该值可能导致更多细小特征像素闪烁。",
    r"Bottom right: HUDless resource": "右下角：无 HUD 资源",
})

# ---------- 帧生成方案说明 ----------
T.update({
    r"Upscaler must be enabled\n\nCan be used with any FG Output, but might be imperfect with some\nTo prevent UI glitching, HUDfix required": "必须启用超分\n\n可用于任意帧生成输出，但部分情况下效果可能不完美\n为避免 UI 异常，需要开启 HUD 修复",
    r"DLSSG via Streamline": "通过 Streamline 的 DLSSG",
    r"Can be used with any FG Output\n\nRequires enabling DLSS-FG in game settings\nSupports HUDless out of the box\n\nLimited to games that use Streamline": "可用于任意帧生成输出\n\n需要在游戏设置中启用 DLSS 帧生成\n开箱即用支持无 HUD 画面\n\n仅限使用 Streamline 的游戏",
    r"DLSSG via Nvngx": "通过 Nvngx 的 DLSSG",
    r"Limited to variants of FSR FG\n\nRequires enabling DLSS-FG in game settings\nSupports HUDless out of the box\nUses Streamline swapchain for pacing": "仅限部分 FSR 帧生成变体\n\n需要在游戏设置中启用 DLSS 帧生成\n开箱即用支持无 HUD 画面\n使用 Streamline 交换链进行节奏控制",
    r"Can be used with any FG Output\n\nRequires enabling FSR-FG in game settings\nSupports HUDless out of the box": "可用于任意帧生成输出\n\n需要在游戏设置中启用 FSR 帧生成\n开箱即用支持无 HUD 画面",
    r"FSR3/4-FG, RDNA4 autoupgrades to FSR4-FG\n\nFSR4-FG sometimes better/worse than XeFG": "FSR3/4 帧生成，RDNA4 会自动升级为 FSR4-FG\n\nFSR4-FG 有时比 XeFG 更好，有时更差",
    r"DLSSG output\nCan be used in conjuction with Nukem's for example": "DLSSG 输出\n例如可与 Nukem 的方案配合使用",
    r"XeFG - heaviest, but best universal FG\n\nXeFG 3 overall deals best with HUD\n\nEnable UI Composition if HUD ghosting": "XeFG — 开销最大，但通用性最好的帧生成\n\nXeFG 3 对 HUD 的处理整体最佳\n\n若出现 HUD 残影请启用 UI 合成",
    r"No real DLSSG, unsupported hardware\nOnly Nvngx FG replacements available": "无原生 DLSSG，硬件不支持\n仅可使用 Nvngx 帧生成替代方案",
    r"None (Real DLSSG)": "无（原生 DLSSG）",
    r"Real DLSSG, For RTX 40xx and above": "原生 DLSSG，需要 RTX 40 系列及以上",
    r"FSR 3 MFG mod": "FSR 3 多帧生成模组",
    r"FSR 3/4 FG using the FFX upgrade\n\n": "使用 FFX 升级版的 FSR 3/4 帧生成\n\n",
    r"Partially based on Nukems, uses SL swapchain\n": "部分基于 Nukem 的方案，使用 Streamline 交换链\n",
    r"Possibly better performance and frame pacing compared to FSR-FG output": "相比 FSR-FG 输出，性能和帧节奏可能更好",
    r"Use if FSR4-FG is supported, otherwise stick to Enabler\n\n": "支持 FSR4-FG 时使用，否则沿用 Enabler\n\n",
    r"FFX used for the middle fake frame, Enabler for the rest\n\n": "中间那张插值帧由 FFX 生成，其余由 Enabler 生成\n\n",
    r"2x - FFX\n3x - Enabler\n4x - FFX + Enabler\n5x - Enabler\n6x - FFX + Enabler\n\n": "2x - FFX\n3x - Enabler\n4x - FFX + Enabler\n5x - Enabler\n6x - FFX + Enabler\n\n",
    r"Due to pacing, only odd number of fake frames are able to use FFX": "受节奏控制限制，只有奇数倍的插值帧才能使用 FFX",
    r"Uses frametimes provided by\nDLSSG or FSR-FG ": "使用由 DLSSG 或 FSR-FG\n提供的帧时间 ",
    r"Uses frametimes calculated by Opti": "使用由 Opti 计算的帧时间",
    r"Let XeFG to handle frametimes": "交给 XeFG 处理帧时间",
})

# ---------- 低延迟 / HUD 修复 / 缩放算法说明 ----------
T.update({
    r"The safest, but might not reduce latency well": "最稳妥，但延迟改善可能有限",
    r"Improves latency, but in some cases will lower FPS more than expected": "能改善延迟，但某些情况下会比利预期更多地降低帧率",
    r"Best when can be used, some games are not compatible (e.g. Cyberpunk)\n": "可用时效果最好，部分游戏不兼容（例如《赛博朋克 2077》）\n",
    r"and will fallback to Aggressive": "并会回退到激进模式",
    r"Follow in-game": "跟随游戏设置",
    r"Enable anti-ghosting correction": "启用抗残影校正",
    r"Temporal HUD pin": "时间性 HUD 固定",
    r"Enable temporal HUD pinning (present-backbuffer stability)": "启用时间性 HUD 固定（提升呈现后备缓冲稳定性）",
    r"HUD OF interpolation (0=legacy pin-present, 1=OF warp)": "HUD 光流插值（0=传统固定呈现，1=光流扭曲）",
    r"Ignore UI texture": "忽略 UI 纹理",
    r"Ignore dedicated DLSSG.UI texture (force legacy HUD path)": "忽略专用的 DLSSG.UI 纹理（强制走传统 HUD 路径）",
    r"Pin DLSSG.Backbuffer to subframe-1 snapshot across MFG frame": "在 MFG 帧间把 DLSSG.Backbuffer 固定为次帧-1 快照",
    r"Antighosting red tint": "抗残影红染调试",
    r"Debug: red tint on corrected pixels": "调试：对被校正像素加红色标记",
    r"Antighosting split screen": "抗残影分屏对比",
    r"Debug: split screen comparison": "调试：分屏对比",
    r"Frame index line": "帧序号线",
    r"Camera MV debug": "相机运动向量调试",
    r"Debug: blue tint where camera MV fallback is used": "调试：在相机运动向量回退处加蓝色标记",
    r"Debug: trapezoid zone visualization": "调试：梯形区域可视化",
    r"When not set OptiScaler controls it via upscalers HDR flag": "未设置时由 OptiScaler 通过超分方案的 HDR 标志控制",
    r"Target res and total ratio at the bottom (max. total 3.0!)": "目标分辨率与总倍率显示在底部（总倍率上限 3.0！）",
    r"Default option.\nGood enough image quality and very fast.": "默认选项。\n画质足够好，速度非常快。",
    r"Fastest traditional option.\nProduces a very soft/blurry image, but might be okay for downscaling.": "最快的传统算法。\n画面很软、偏模糊，但用于降采样尚可。",
    r"Designed primarily for downscaling.\nRetains good contrast with minimal artefacts, but softer than Lanczos.": "主要为降采样设计。\n对比度保持良好、伪影极少，但比 Lanczos 更软。",
    r"Lighter and faster than Lanczos3.\nLess prone to ringing artefacts, but slightly blurrier.": "比 Lanczos3 更轻更快。\n更不易产生振铃伪影，但略模糊一些。",
    r"Heavier version of Lanczos2.\nOffers the sharpest image, but is the most prone to ringing.\nConsidered the best along with Kaiser3.": "Lanczos2 的加重版本。\n画面最锐利，但最容易出现振铃。\n与 Kaiser3 并称最佳。",
    r"Similar to Lanczos2.\nSmoother and less prone to artefacts than Lanczos, but slightly blurrier.": "与 Lanczos2 类似。\n更平滑、伪影更少，但略模糊一些。",
    r"Similar to Lanczos3.\nFar less prone to artefacting than Lanczos3, but much heavier on the GPU.\nConsidered the best along with Lanczos3.": "与 Lanczos3 类似。\n伪影远少于 Lanczos3，但对 GPU 负担重得多。\n与 Lanczos3 并称最佳。",
    r"Specialised to prevent artifacts.\nEliminates harsh halos for a natural look, but can appear slightly soft.": "专为抑制伪影设计。\n消除生硬光晕、观感自然，但可能略显柔和。",
    r"Only FSR1 and Bicubic are supported when Ratio is below 1.0.": "比例低于 1.0 时仅支持 FSR1 与双三次（Bicubic）。",
    r"Higher values can reduce tearing but may increase latency and cap FPS.\n": "更高的数值可减少撕裂，但可能增加延迟并限制帧率。\n",
    r"For most games, use 0 for lowest latency or 1 for normal VSync.": "多数游戏请选 0 获得最低延迟，或选 1 使用普通垂直同步。",
    r"Non-Linear sRGB": "非线性 sRGB",
    r"Non-Linear PQ": "非线性 PQ",
    r"FSR Anti-Lag 2.0": "FSR Anti-Lag 2.0",
})

# ---------- 启动提示 / 通知弹窗 ----------
T.update({
    r"That's likely unintended and will lead to big OptiScaler.log\n": "这通常不是有意为之，会让 OptiScaler.log 变得非常大\n",
    r"Please disable logging to file and delete OptiScaler.log": "请关闭文件日志并删除 OptiScaler.log",
    r"Trace logging still active": "跟踪级日志仍在开启",
    r"D3D11 %s| %s %d.%d.%d%s": "D3D11 %s| %s %d.%d.%d%s",
    r"| Input: %s": "| 输入：%s",
    r"| Spoof: %s": "| 伪装：%s",
})

# ---------- 未接入界面但属于同一批的说明文字 ----------
T.update({
    r"fallback for menu input. ": "作为菜单输入的兜底方案。",
    r"A local InputHwnd can improve menu input, but robust game input blocking still requires an ": "使用本地 InputHwnd 可以改善菜单输入，但要可靠地拦截游戏输入仍然需要一个",
    r"in-process input module.": "进程内的输入模块。",
})
