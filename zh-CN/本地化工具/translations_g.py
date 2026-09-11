# -*- coding: utf-8 -*-
"""
OptiScaler 汉化词条 - 第七批：ShowHelpMarker 提示气泡（下）
键取自抽取结果原文，含 \n 与行尾空格，请勿随意改动。
"""

T = {}

T.update({
    r"Enable FSR3.1-FG Debug view\n\nTop left: Game Motion Vectors\nTop middle: GMV Depth\nTop right: Optical Flow MV\nMiddle: Interpolated frame only\nBottom left: Disocclusion mask\nBottom middle: Interpolation source (w/o UI)\nBottom right: HUDless resource": "启用 FSR3.1-FG 调试视图\n\n左上：游戏运动向量\n中上：游戏运动向量深度\n右上：光流运动向量\n中间：仅插值帧\n左下：去遮挡遮罩\n中下：插值来源（不含 UI）\n右下：无 HUD 资源",
    r"Forces Borderless display mode\n\nFor best results, set fullscreen \nresolution to your display resolution\nMight cause some instability issues.\n\nNEEDS GAME RESTART TO BE ACTIVE!": "强制使用无边框显示模式\n\n为获得最佳效果，请把全屏分辨率\n设置为显示器的原生分辨率\n可能引发一些稳定性问题。\n\n需要重启游戏才能生效！",
    r"Extended format checks for possible HUDless\nMight cause crashes and slowdowns!": "对可能属于无 HUD 画面的资源做扩展格式检查\n可能导致崩溃和性能下降！",
    r"Enables capturing of resources before shader execution.\nIncrease HUDless capture chances, but might cause capturing of unnecessary resources.": "在着色器执行前捕获资源。\n可提高无 HUD 画面的捕获成功率，但可能捕获到无关资源。",
    r"Fix for DLSS-D wrong depth inputs": "修复 DLSS-D 深度输入错误",
    r"Flip Velocity & Depth resources of Unity games": "翻转 Unity 游戏的速度与深度资源",
    r"Use height difference as offset": "使用高度差作为偏移",
    r"Block rarely used resources from using as HUDless \nto prevent flickers and other issues\n\nHUDfix enable/disable will reset the block list!": "阻止很少使用的资源被当作无 HUD 画面，\n以避免闪烁等问题\n\n开启/关闭 HUD 修复会重置屏蔽列表！",
    r"Relax resolution checks for HUDless by 32 pixels \nHelps games which use black borders for some \nresolutions and screen ratios (e.g. Witcher 3)": "把无 HUD 画面的分辨率检查放宽 32 像素\n有助于那些在特定分辨率和屏幕比例下\n使用黑边的游戏（例如《巫师 3》）",
    r"Always track resources, might cause performance issues\n, but also might fix HUDFix related crashes!": "始终跟踪资源，可能导致性能问题，\n但也可能修复与 HUD 修复相关的崩溃！",
    r"Disable tracking of CreateRenderTargetView\nThis might help filtering of wrong HUDless resources": "禁用对 CreateRenderTargetView 的跟踪\n有助于过滤掉误判的无 HUD 资源",
    r"Disable tracking of CreateShaderResourceView\nThis might help filtering of wrong HUDless resources": "禁用对 CreateShaderResourceView 的跟踪\n有助于过滤掉误判的无 HUD 资源",
    r"Disable tracking of CreateUnorderedAccessView\nThis might help filtering of wrong HUDless resources": "禁用对 CreateUnorderedAccessView 的跟踪\n有助于过滤掉误判的无 HUD 资源",
    r"Disable tracking of OMSetRenderTargets\nThis might help filtering of wrong HUDless resources": "禁用对 OMSetRenderTargets 的跟踪\n有助于过滤掉误判的无 HUD 资源",
    r"Disable tracking of SetComputeRootDescriptorTable\nThis might help filtering of wrong HUDless resources": "禁用对 SetComputeRootDescriptorTable 的跟踪\n有助于过滤掉误判的无 HUD 资源",
    r"Disable tracking of SetGraphicsRootDescriptorTable\nThis might help filtering of wrong HUDless resources": "禁用对 SetGraphicsRootDescriptorTable 的跟踪\n有助于过滤掉误判的无 HUD 资源",
    r"Disable tracking of DrawInstanced\nThis might help filtering of wrong HUDless resources": "禁用对 DrawInstanced 的跟踪\n有助于过滤掉误判的无 HUD 资源",
    r"Disable tracking of DrawIndexedInstanced\nThis might help filtering of wrong HUDless resources": "禁用对 DrawIndexedInstanced 的跟踪\n有助于过滤掉误判的无 HUD 资源",
    r"Disable tracking of Dispatch\nThis might help filtering of wrong HUDless resources": "禁用对 Dispatch 的跟踪\n有助于过滤掉误判的无 HUD 资源",
    r"Make a copy of motion vectors to use with OptiFG\nFor preventing corruptions that might happen": "复制一份运动向量供 OptiFG 使用\n用于防止可能出现的画面错乱",
    r"Make a copy of depth to use with OptiFG\nFor preventing corruptions that might happen": "复制一份深度供 OptiFG 使用\n用于防止可能出现的画面错乱",
    r"Depth values will be divided to this value": "深度值将除以该数值",
    r"Use mutex to prevent desync of FG and crashes\nDisabling might improve the perf but decrease stability": "使用互斥锁防止帧生成失步与崩溃\n关闭可能提升性能，但稳定性下降",
    r"Makes a copy of the depth buffer\nCan fix broken visuals in some games on AMD GPUs under Windows\nCan cause stutters, so best to use only when necessary": "复制一份深度缓冲\n可修复 Windows 下部分 AMD 显卡游戏的画面异常\n可能导致卡顿，建议仅在必要时使用",
    r"Required for Debug flags to work correctly": "调试标志正常工作的必要前提",
    r"Might be required for some sets of DispatchFlags": "某些 DispatchFlags 组合可能需要",
    r"Do not use HUDless set at ffxConfig": "不使用 ffxConfig 中设置的无 HUD 画面",
    r"Do not use HUDless set at ffxDispatch": "不使用 ffxDispatch 中设置的无 HUD 画面",
    r"Might help achieve better image quality": "可能有助于获得更好的画质",
    r"Might help achieve better image quality\nAnd potentially less ghosting": "可能有助于获得更好的画质\n并可能减少残影",
    r"FSR Anti-Lag 2.0 is the new name for AntiLag 2\nDon't ask me why": "FSR Anti-Lag 2.0 是 AntiLag 2 的新名字\n别问我为什么",
    r"By default, FSR Anti-Lag 2.0/XeLL is used when available.\nThis setting lets you force LatencyFlex instead": "默认会优先使用 FSR Anti-Lag 2.0/XeLL。\n此设置可改为强制使用 LatencyFlex",
    r"Allows XeLL to work without FG on non-Intel cards.\n\nDisables FG options\n\nRequires a restart": "让 XeLL 在非 Intel 显卡上无需帧生成也能生效。\n\n会禁用帧生成相关选项\n\n需要重启",
    r"Ignores the value sent by the game\nand uses the value set below": "忽略游戏传入的值\n改用下方设置的值",
})

T.update({
    r"Enable OptiScaler's sharpening filter\nBy default uses a sharpening value provided by the game\nSelect 'Override' under 'Sharpness' and adjust the slider\nto change it\n\nSome upscalers have their own sharpness filter, so this\noption is not always needed": "启用 OptiScaler 的锐化滤镜\n默认使用游戏提供的锐度值\n勾选“锐度”下的“覆盖”并调整滑条即可修改\n\n部分超分方案自带锐化滤镜，\n因此不一定需要开启此项",
    r"Use AMD's RCAS\nModified to add Contrast parameter\nand MAS support": "使用 AMD 的 RCAS\n已修改以增加对比度参数\n并支持 MAS",
    r"Use Depth Aware Sharpening (RCAS)\nSmarter sharpening with less artifacts,\nbut also heavier\n\nThe farther away is the object, the more\nsharpening is applied": "使用深度感知锐化（RCAS）\n更智能、伪影更少，\n但开销更大\n\n物体距离越远，\n应用的锐化越强",
    r"Use Depth Aware Sharpening (DAS)\nDepth-aware directional adaptive luma sharpener\nSmarter sharpening with less artifacts,\nbut also heavier\n\nThe farther away is the object, the more\nsharpening is applied": "使用深度感知锐化（DAS）\n深度感知的方向自适应亮度锐化器\n更智能、伪影更少，\n但开销更大\n\n物体距离越远，\n应用的锐化越强",
    r"Enables sharpness adjustments according to the motion": "根据运动情况自动调整锐化",
    r"Enable DA + MAS debug views\nBlue tint for DA detected edges\n\nMore red areas will have more sharpness applied\nGreen areas will get reduced sharpness": "启用 DA + MAS 调试视图\nDA 检测到的边缘显示为蓝色\n\n偏红区域会施加更强的锐化\n偏绿区域会减弱锐化",
    r"Clamps the final image to the [0, 1] range.\n\nPrevents overshoot artifacts such as bright halos or negative colors.\nRecommended for LDR pipelines; optional for HDR depending on tone-mapping.\n\nWhen not set OptiScaler controls it via upscalers HDR flag": "把最终画面钳制在 [0, 1] 区间。\n\n可防止亮光晕、负色等过冲伪影。\n推荐 LDR 流程使用；HDR 流程可选，取决于色调映射方式。\n\n未设置时由 OptiScaler 通过超分方案的 HDR 标志控制",
    r"Ignores small depth differences before edge detection.\n\nHigher values reduce flickering and noise from minor depth changes, but may soften real geometry edges.\nLower values preserve fine detail but can cause unstable or noisy edge detection.": "在边缘检测前忽略细微的深度差异。\n\n数值越高，可减少由微小深度变化引起的闪烁和噪点，但可能柔化真实的几何边缘。\n数值越低，保留更多细节，但边缘检测可能不稳定或出现噪点。",
    r"Controls how strongly sharpening is reduced across depth edges.\n\nHigher values more aggressively prevent sharpening across object boundaries (reduces halos).\nLower values allow more sharpening to pass across edges (sharper but riskier).": "控制跨深度边缘时锐化被削弱的程度。\n\n数值越高，越会阻止锐化跨越物体边界（减少光晕）。\n数值越低，允许更多锐化越过边缘（更锐利但风险更高）。",
    r"Controls sharpness at high contrast areas.": "控制高对比区域的锐度。",
    r"Positive values decrease sharpness at high contrast areas.\nNegative values increase sharpness at high contrast areas.": "正值会降低高对比区域的锐度。\n负值会提高高对比区域的锐度。",
    r"Areas that are more red will have more sharpness applied\nGreen areas will get reduced sharpness": "偏红区域会施加更强的锐化\n偏绿区域会减弱锐化",
    r"Maximum amount of sharpness that motion can add or remove.\n\nNegative values reduce sharpening in motion (recommended).\nPositive values increase sharpening in motion.\n\nThe final adjustment scales with motion and is capped at this value.": "运动可增加或减少锐化量的上限。\n\n负值表示运动中降低锐化（推荐）。\n正值表示运动中提高锐化。\n\n最终调整量随运动幅度变化，并以此值为上限。",
    r"Minimum motion required before motion-based sharpening adjustment begins.\n\nHigher values ignore small movements (more stable).\nLower values react to subtle motion (more sensitive).": "开始进行运动锐化调整所需的最小运动量。\n\n数值越高，越会忽略微小移动（更稳定）。\n数值越低，对细微运动越敏感。",
    r"Defines the motion range over which the effect ramps from zero to full strength.\n\nValues above the threshold are mapped into this range.\nLarger values make the response smoother and more gradual.\nSmaller values make the effect react more quickly and aggressively.": "定义效果从零递增到最强所需的运动范围。\n\n超过阈值的部分会被映射到该范围内。\n数值越大，响应越平滑渐进。\n数值越小，反应越迅速激进。",
    r"Overrides every upscaler preset with the set value\n\n1.5x on a 1080p screen means an internal res of 720p\n1080 / 1.5 = 720": "用设定值覆盖所有超分预设\n\n在 1080p 屏幕上 1.5 倍意味着内部渲染分辨率 720p\n1080 / 1.5 = 720",
    r"Lets you override each preset's ratio individually\nNote that not every game supports every quality preset\n\n1.5x on a 1080p screen means internal resolution of 720p\n1080 / 1.5 = 720": "允许为每个预设单独覆盖比例\n注意并非所有游戏都支持所有画质档位\n\n在 1080p 屏幕上 1.5 倍意味着内部渲染分辨率 720p\n1080 / 1.5 = 720",
    r"Upscales the image internally to a higher output resolution\nthen downscales it back to your display resolution\n\nValues <1.0 make the upscaler cheaper\nValues >1.0 make image sharper at the cost of performance\n\nIf greyed out, please check Git Wiki - Unreal Engine tweaks\n\nTarget res and total ratio at the bottom (max. total 3.0!)": "先在内部把画面放大到更高的输出分辨率，\n再降采样回你的显示器分辨率\n\n数值 <1.0 可减轻超分负担\n数值 >1.0 画质更锐利，但性能开销更大\n\n若此项为灰色，请查阅 Git Wiki 的虚幻引擎调整说明\n\n目标分辨率与总倍率显示在底部（总倍率上限 3.0！）",
})

T.update({
    r"Some Unreal Engine games need this\n\nTry using if colours flickering or\nobjects have ghosting trails": "部分虚幻引擎游戏需要开启\n\n若出现颜色闪烁或\n物体拖影，可以尝试开启",
    r"Allows the use of a Reactive mask\nKeep in mind that a Reactive mask sent to DLSS\nwill not produce a good image in combination with FSR/XeSS": "允许使用反应遮罩\n请注意：把反应遮罩传给 DLSS，\n再与 FSR/XeSS 组合时画质通常不好",
    r"Option disabled because the game doesn't provide a Reactive mask": "该选项已禁用，因为游戏未提供反应遮罩",
    r"You shouldn't need to change it": "通常不需要改动此项",
    r"Might help with purple hue in some games": "可能有助于解决部分游戏画面偏紫的问题",
    r"Mostly a fix for Unreal Engine games\nTop left part of the screen will be blurry": "主要针对虚幻引擎游戏的修复\n开启后屏幕左上角会变模糊",
    r"Fix for games that send motion data with preapplied jitter": "针对已预置抖动就发送运动数据的游戏的修复",
    r"Values above 0 activate usage of Reactive mask": "大于 0 的值会启用反应遮罩",
    r"Extended sliders limit for quality presets\n\nUsing this option changes resolution detection logic\nand might cause issues and crashes!": "扩展画质预设的滑条范围\n\n使用此项会改变分辨率检测逻辑，\n可能引发问题和崩溃！",
    r"Fix for games ignoring official DRS limits": "修复游戏忽略官方 DRS 限制的问题",
    r"Force V-Sync On/Off & Sync Interval options": "强制开关垂直同步，并提供同步间隔选项",
    r"Apply same override value to all textures": "对所有纹理应用相同的覆盖值",
    r"Apply override value as scale multiplier\nWhen using scale mode, please use positive\noverride values to increase sharpness!": "把覆盖值作为倍率使用\n使用倍率模式时，请填正值\n才能提升清晰度！",
    r"Override all textures mipmap values\nNormally OptiScaler only overrides\nbelow zero mipmap values!": "覆盖所有纹理的 mipmap 值\n通常 OptiScaler 只覆盖\n小于 0 的 mipmap 值！",
    r"Update comparison filters": "修改比较采样过滤器",
    r"Update min/max filters": "修改 min/max 过滤器",
    r"Skip updating of point filters": "跳过点采样过滤器的修改",
    r"Can help with blurry textures in broken games\nNegative values will make textures sharper\nPositive values will make textures more blurry\n\nHas a small performance impact": "可改善画面异常游戏中的纹理模糊\n负值会让纹理更锐利\n正值会让纹理更模糊\n\n对性能有轻微影响",
})

T.update({
    r"Controls the DXGI Present sync interval, which determines how\nthe swap chain waits for vertical refresh.\n\n0  = Present immediately, no VSync wait.\n1  = Sync to every refresh, normal VSync.\n2+ = Present every N refreshes, reducing effective frame rate.\n\nHigher values can reduce tearing but may increase latency and cap FPS.\nFor most games, use 0 for lowest latency or 1 for normal VSync.": "控制 DXGI Present 的同步间隔，决定交换链\n如何等待垂直刷新。\n\n0  = 立即呈现，不等待垂直同步。\n1  = 每次刷新都同步，即普通垂直同步。\n2+ = 每 N 次刷新呈现一次，会降低实际帧率。\n\n数值越大越能减少撕裂，但可能增加延迟并限制帧率。\n多数游戏请用 0（最低延迟）或 1（普通垂直同步）。",
    r"Click to open the OptiScaler Wiki page\nin your default browser\n\nCompatibility list with known game issues\nand workarounds, FG options explained\nand other useful info": "点击用默认浏览器打开\nOptiScaler Wiki 页面\n\n其中包含游戏兼容性列表、已知问题\n与解决办法、帧生成选项说明\n以及其他实用信息",
    r"Enable FSR3.1-FG Debug view\n\nTop left: Game Motion Vectors": "启用 FSR3.1-FG 调试视图\n\n左上：游戏运动向量",
    r"The safest, but might not reduce latency well": "最稳妥，但延迟改善可能有限",
    r"Improves latency, but in some cases will lower FPS more than expected": "能改善延迟，但某些情况下帧率下降可能超出预期",
})
