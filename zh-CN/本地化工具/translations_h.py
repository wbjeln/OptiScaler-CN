# -*- coding: utf-8 -*-
"""
OptiScaler 汉化词条 - 第八批：长句拼接后的完整键与遗漏项
"""

T = {}

T.update({
    # 多段拼接的长句（源码里被拆成多个相邻字面量，这里给出合并后的完整键）
    r"That's likely unintended and will lead to big OptiScaler.log\nPlease disable logging to file and delete OptiScaler.log": "这通常不是有意为之，会让 OptiScaler.log 变得非常大\n请关闭文件日志并删除 OptiScaler.log",
    r"Please select %s as upscaler from game\noptions and load a save game to enable Opti settings.\nUpscalers don't always work in menus.": "请在游戏选项中把超分方案选为 %s\n并载入一个存档以启用 Opti 设置。\n超分功能在主菜单中不一定生效。",
    r"Each internal FSR4 preset is tuned for a specific resolution.\nSelecting an FSR4 preset won't change the in-game\nupscaler preset!!!\n\nPreset 0 is meant for FSR Native AA\nPreset 1 is meant for Quality/Ultra Quality\nPreset 2 is meant for Balanced\nPreset 3 is meant for Performance\nPreset 4 is meant for DRS\nPreset 5 is meant for Ultra Performance": "每个内部 FSR4 预设都针对特定分辨率调校。\n选择 FSR4 预设不会改变游戏内的\n超分预设！！！\n\n预设 0 面向 FSR 原生 AA\n预设 1 面向画质/超高画质\n预设 2 面向平衡\n预设 3 面向性能\n预设 4 面向动态分辨率\n预设 5 面向超高性能",
    r"FSR 3/4 FG using the FFX upgrade\n\nPartially based on Nukems, uses SL swapchain\nPossibly better performance and frame pacing compared to FSR-FG output": "使用 FFX 升级版的 FSR 3/4 帧生成\n\n部分基于 Nukem 的方案，使用 Streamline 交换链\n相比 FSR-FG 输出，性能和帧节奏可能更好",
    r"Use if FSR4-FG is supported, otherwise stick to Enabler\n\nFFX used for the middle fake frame, Enabler for the rest\n\n2x - FFX\n3x - Enabler\n4x - FFX + Enabler\n5x - Enabler\n6x - FFX + Enabler\n\nDue to pacing, only odd number of fake frames are able to use FFX": "支持 FSR4-FG 时使用，否则沿用 Enabler\n\n中间那张插值帧由 FFX 生成，其余由 Enabler 生成\n\n2x - FFX\n3x - Enabler\n4x - FFX + Enabler\n5x - Enabler\n6x - FFX + Enabler\n\n受节奏控制限制，只有奇数倍的插值帧才能使用 FFX",
    r"Best when can be used, some games are not compatible (e.g. Cyberpunk)\nand will fallback to Aggressive": "可用时效果最好，部分游戏不兼容（例如《赛博朋克 2077》）\n此时会回退到激进模式",
    r"Enable FSR3.1-FG Debug view\n\nTop left: Game Motion Vectors\nTop middle: GMV Depth\nTop right: Optical Flow MV\nMiddle: Interpolated frame only\nBottom left: Disocclusion mask\nBottom middle: Interpolation source (w/o UI)\nBottom right: HUDless resource": "启用 FSR3.1-FG 调试视图\n\n左上：游戏运动向量\n中上：游戏运动向量深度\n右上：光流运动向量\n中间：仅插值帧\n左下：去遮挡遮罩\n中下：插值来源（不含 UI）\n右下：无 HUD 资源",
    r"2x - FFX\n3x - Enabler\n4x - FFX + Enabler\n5x - Enabler\n6x - FFX + Enabler\n\n": "2x - FFX\n3x - Enabler\n4x - FFX + Enabler\n5x - Enabler\n6x - FFX + Enabler\n\n",
    r"FFX used for the middle fake frame, Enabler for the rest\n\n": "中间那张插值帧由 FFX 生成，其余由 Enabler 生成\n\n",
    r"FSR 3/4 FG using the FFX upgrade\n\n": "使用 FFX 升级版的 FSR 3/4 帧生成\n\n",
    r"Partially based on Nukems, uses SL swapchain\n": "部分基于 Nukem 的方案，使用 Streamline 交换链\n",
    r"Due to pacing, only odd number of fake frames are able to use FFX": "受节奏控制限制，只有奇数倍的插值帧才能使用 FFX",
    r"Decreasing this could result in more thin feature pixels flickering.": "调低该值可能导致更多细小特征像素闪烁。",
    r"Bottom right: Detail Protection Takedown": "右下角：细节保护取舍视图",
    r"Bottom right: HUDless resource": "右下角：无 HUD 资源",
    r"Higher values can reduce tearing but may increase latency and cap FPS.\n": "更高的数值可减少撕裂，但可能增加延迟并限制帧率。\n",
    r"For most games, use 0 for lowest latency or 1 for normal VSync.": "多数游戏请选 0 获得最低延迟，或选 1 使用普通垂直同步。",
    r"Enable FSR3.1-FG Debug view\n\nTop left: Game Motion Vectors": "启用 FSR3.1-FG 调试视图\n\n左上：游戏运动向量",

    # 遗漏的界面文字
    r"OptiCopers, assemble!": "Opti 扛压军团，集合！",
    r"Depth as ValidNow": "深度视作 ValidNow",
    r"Velocity as ValidNow": "速度视作 ValidNow",
    r"HUDless as ValidNow": "无 HUD 视作 ValidNow",
    r"DE Ver: %d.%d.%d.%d   GB Ver: %d.%d": "DE 版本：%d.%d.%d.%d   GB 版本：%d.%d",
    r"Low latency timings, whole frame: %.1fms": "低延迟时序，整帧：%.1fms",
    r"Reflex timings, whole frame: %.1fms": "Reflex 时序，整帧：%.1fms",
    r"nvngx replacement: %s": "nvngx 替代：%s",
    r"FSR Hooks: %s": "FSR 挂钩：%s",
    r"nvngx_dlss : %s": "nvngx_dlss ：%s",
    r"nvngx_dlssd : %s": "nvngx_dlssd ：%s",
    r"nvngx.dll: %s": "nvngx.dll：%s",
})
