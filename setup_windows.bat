REM Setup OptiScaler for your game
@echo off
chcp 65001 >nul 2>nul
cls
echo  ::::::::  :::::::::  ::::::::::: :::::::::::  ::::::::   ::::::::      :::     :::        :::::::::: :::::::::  
echo :+:    :+: :+:    :+:     :+:         :+:     :+:    :+: :+:    :+:   :+: :+:   :+:        :+:        :+:    :+: 
echo +:+    +:+ +:+    +:+     +:+         +:+     +:+        +:+         +:+   +:+  +:+        +:+        +:+    +:+ 
echo +#+    +:+ +#++:++#+      +#+         +#+     +#++:++#++ +#+        +#++:++#++: +#+        +#++:++#   +#++:++#:  
echo +#+    +#+ +#+            +#+         +#+            +#+ +#+        +#+     +#+ +#+        +#+        +#+    +#+ 
echo #+#    #+# #+#            #+#         #+#     #+#    #+# #+#    #+# #+#     #+# #+#        #+#        #+#    #+# 
echo  ########  ###            ###     ###########  ########   ########  ###     ### ########## ########## ###    ### 
echo.
echo 原力与此脚本同在……
echo v3.0-pre1
echo.

del "!! README_EXTRACT ALL FILES TO GAME FOLDER !!.txt" 2>nul

setlocal enabledelayedexpansion

if exist OptiScaler.sln (
    echo 检测到 OptiScaler.sln 或 .git 文件！
    echo.
    echo 如果目录里存在 .sln 或 .git 文件，恭喜你，你手上这份是源码。
	echo 请改为下载正式发布的 OptiScaler。
	echo.
    echo 提示 - 请使用 GitHub 的 Releases 页面，或者 RTFM :^)
	echo.
    echo.
	echo 附注：如果你既拿到了 OptiScaler.dll 又拿到了 .sln，请高抬贵手删掉 .sln，重新运行本 BAT 安装脚本，然后听天由命。
	echo.
    goto end
)

if not exist OptiScaler.dll (
    echo 未找到 OptiScaler 的 OptiScaler.dll 文件！
    echo 最可能是文件夹权限问题。以管理员身份重新运行本 BAT 可能会顺利一些。
    echo.
	echo 或者
	echo.
    echo 如果 OptiScaler.dll 确实存在，请手动将其重命名为受支持的文件名（例如 dxgi.dll 或 winmm.dll），到此就完成了！
	echo 重命名之后无需再次运行本安装脚本。
	echo.
    echo.
    goto end
)

REM 检查是否存在 0.9 之前的旧版附加文件，以及已有的 Opti 安装
set "OLD_FILES_FOUND=0"
set "OPTI_DLL_LIST="
if exist nvapi64.dll set "OLD_FILES_FOUND=1"
if exist nvngx.dll set "OLD_FILES_FOUND=1"
if exist OptiScaler.asi set "OLD_FILES_FOUND=1"
if exist "Remove OptiScaler.bat" set "OLD_FILES_FOUND=1"
if exist "Remove_OptiScaler.bat" set "OLD_FILES_FOUND=1"

for %%F in (dxgi.dll winmm.dll d3d12.dll dbghelp.dll version.dll wininet.dll winhttp.dll) do (
    if exist "%%F" (
        set "origname="
        for /f "tokens=*" %%P in ('powershell -NoProfile -Command "(Get-Item '%%F').VersionInfo.OriginalFilename"') do (
            set "origname=%%P"
        )
        if /i "!origname!"=="OptiScaler.dll" (
            set "OLD_FILES_FOUND=1"
            set "OPTI_DLL_LIST=!OPTI_DLL_LIST! %%F"
        )
    )
)

if "!OLD_FILES_FOUND!"=="1" (
    echo 警告：检测到可能存在的旧版 OptiScaler 文件！
    if exist nvapi64.dll echo   - nvapi64.dll
    if exist nvngx.dll echo   - nvngx.dll
    if exist OptiScaler.asi echo   - OptiScaler.asi
	if exist "Remove OptiScaler.bat" echo   - Remove OptiScaler.bat
    if exist "Remove_OptiScaler.bat" echo   - Remove_OptiScaler.bat
    for %%F in (!OPTI_DLL_LIST!) do echo   - %%F （原始文件名：OptiScaler.dll）
    echo.
    echo 这些文件可能与当前版本的 OptiScaler 冲突。
    echo 建议将其删除。
    echo.
    echo 是否删除这些文件？
    echo.
	echo [1] 是
    echo [2] 否
    echo.
	set /p "USER_CHOICE=等待输入 - "
	echo.
    if /i "!USER_CHOICE!"=="1" (
        if exist nvapi64.dll (
            del nvapi64.dll
            echo 已删除 nvapi64.dll
        )
        if exist nvngx.dll (
            del nvngx.dll
            echo 已删除 nvngx.dll
        )
        if exist OptiScaler.asi (
            del OptiScaler.asi
            echo 已删除 OptiScaler.asi
        )
		if exist "Remove OptiScaler.bat" (
            del "Remove OptiScaler.bat"
            echo 已删除 Remove OptiScaler.bat
        )
        if exist "Remove_OptiScaler.bat" (
            del "Remove_OptiScaler.bat"
            echo 已删除 Remove_OptiScaler.bat
        )
        for %%F in (!OPTI_DLL_LIST!) do (
            del "%%F"
            echo 已删除 %%F
        )
        echo 完成！
    ) else (
        echo 已跳过删除。请注意这些文件可能引发问题。
    )
    echo.
)

REM 根据当前目录设置路径

set "optiScalerFile=.\OptiScaler.dll"
set setupSuccess=false

REM 检查是否存在 Engine 文件夹
if exist ".\Engine" (
    echo 检测到 Engine 文件夹。如果这是虚幻引擎游戏，请把 OptiScaler 解压到 #CODENAME#\Binaries\Win64
	echo 不要解压到 Engine 文件夹里！
	echo.
	echo 例如 - \Jedi Survivor\SwGame\Binaries\Win64、\Witchfire\Witchfire\Binaries\Win64
    echo.
    echo 是否继续安装到当前文件夹？
	echo. 
    echo [1] 是
    echo [2] 否
    echo.
	set /p continueChoice="等待输入 - "
    set continueChoice=!continueChoice: =!

    if "!continueChoice!"=="1" (
        goto selectFilename
    )

    goto end
)

REM 让用户为 OptiScaler 选择文件名
:selectFilename
echo.
echo 请为 OptiScaler 选择一个文件名（默认为 dxgi.dll，兼容性最好）：
echo （Vulkan 请用 winmm.dll；XGP／微软商店版用 winmm.dll 或 version.dll 可能更好）
echo.
echo  [1] dxgi.dll
echo  [2] winmm.dll
echo  [3] version.dll
echo  [4] dbghelp.dll
echo  [5] d3d12.dll
echo  [6] wininet.dll
echo  [7] winhttp.dll
echo  [8] OptiScaler.asi
echo.
set /p filenameChoice="请输入 1-8（直接回车使用默认值）： "

if "%filenameChoice%"=="" (
    set selectedFilename="dxgi.dll"
) else if "%filenameChoice%"=="1" (
    set selectedFilename="dxgi.dll"
) else if "%filenameChoice%"=="2" (
    set selectedFilename="winmm.dll"
) else if "%filenameChoice%"=="3" (
    set selectedFilename="version.dll"
) else if "%filenameChoice%"=="4" (
    set selectedFilename="dbghelp.dll"
) else if "%filenameChoice%"=="5" (
    set selectedFilename="d3d12.dll"
) else if "%filenameChoice%"=="6" (
    set selectedFilename="wininet.dll"
) else if "%filenameChoice%"=="7" (
    set selectedFilename="winhttp.dll"
) else if "%filenameChoice%"=="8" (
    set selectedFilename="OptiScaler.asi"
) else (
    echo 选择无效，请选择一个有效的选项。
    echo.
    goto selectFilename
)

if exist %selectedFilename% (
    echo.
    echo 警告：当前文件夹中已存在 %selectedFilename%。
    echo.
	echo 是否覆盖 %selectedFilename%？
	echo.
    echo [1] 是
    echo [2] 否
    echo.
	set /p overwriteChoice="等待输入 - "
    set overwriteChoice=!overwriteChoice: =!
    
    echo.
    if "!overwriteChoice!"=="1" (
        goto checkWine
    )

    goto selectFilename
)

REM wine 不支持 powershell
:checkWine
reg query HKEY_CURRENT_USER\Software\Wine\DllOverrides >nul 2>&1
if %errorlevel%==0 (
    echo.
    echo 检测到正在使用 wine，跳过伪装检查。
    echo 如有需要，可以在配置里设置 Dxgi=false 来关闭伪装
    echo.
    pause
    goto completeSetup
) 

if exist %windir%\system32\nvapi64.dll (
    echo.
    echo 检测到 Nvidia 驱动文件。
    set isNvidia=true
) else (
    set isNvidia=false
)

REM 询问用户的显卡类型
echo.
echo 你使用的是 Nvidia 显卡，还是 AMD／Intel 显卡？
echo.
echo [1] AMD／Intel
echo [2] Nvidia
echo.

:gpuPrompt
if "%isNvidia%"=="true" (
    set /p gpuChoice="请输入 1 或 2（已检测到 Nvidia）： "
) else (
    set /p gpuChoice="请输入 1 或 2（已检测到 AMD／Intel）： "
)

if "%gpuChoice%"=="1" goto gpuValid
if "%gpuChoice%"=="2" goto gpuValid
echo 输入无效，请输入 1 或 2。
echo.
goto gpuPrompt

:gpuValid

REM 如果是 Nvidia 就跳过伪装设置
if "%gpuChoice%"=="2" (
    goto completeSetup
)

REM 询问用户是否需要 DLSS 输入
echo.
echo 你是否打算用 DLSS 输入来替换为 FSR／XeSS？（会启用 Nvidia 伪装，DLSS-FG、Reflex 转 AntiLag2 都需要它）
echo 如果之后想改变设置，请编辑 OptiScaler.ini：设为 Dxgi=false 可关闭伪装，改回其他值即可恢复。
echo.
echo [1] 是
echo [2] 否
echo.
set /p enablingSpoofing="请输入 1 或 2（直接回车表示是）： "

set configFile=OptiScaler.ini
if "%enablingSpoofing%"=="2" (
    if not exist "%configFile%" (
        echo 未找到配置文件：%configFile%
        pause
    )

    powershell -Command "(Get-Content '%configFile%') -replace 'Dxgi=auto', 'Dxgi=false' | Set-Content '%configFile%'"
)

REM 决定是否运行 OptiPatcher
echo.
if "%gpuChoice%"=="1" (
    echo 检测到 AMD／Intel 显卡 - 开始检查 OptiPatcher。
    goto checkExistingOptiPatcher
)

:checkExistingOptiPatcher
set "foundOptiPatcher="
for %%F in (OptiScaler\plugins\*OptiPatcher*.asi) do (
    set "foundOptiPatcher=%%F"
)

if defined foundOptiPatcher (
    echo.
    echo 找到 OptiPatcher：!foundOptiPatcher!
    echo 如果现有版本工作正常，最好保留它。
	echo 是否重新下载可能更新的版本？
	echo.
    echo [1] 是
    echo [2] 否
    echo.
	set /p optiRedownload="等待输入 - "
        
    if /i "!optiRedownload!"=="1" (
        echo.
        echo 正在删除 !foundOptiPatcher!……
        del "!foundOptiPatcher!"
        goto checkOptiPatcher
    ) else (
        echo.
        echo 保留现有的 OptiPatcher - 跳过下载。
        goto completeSetup
    )
)

REM 未安装 - 继续下载
goto checkOptiPatcher

:checkOptiPatcher
REM 检查网络连通性
echo.
echo 正在检查 OptiPatcher 兼容性……
echo 如果卡住不动，请按 Ctrl+C 跳转到安装完成。

ping -n 1 -w 3000 github.com >nul 2>&1
if %errorlevel% neq 0 (
    echo 处于离线状态，或 GitHub 无法访问。跳过 OptiPatcher 检查。
    goto completeSetup
)

set "OPTI_MATCH=NO"
for /f "usebackq tokens=*" %%A in (`powershell -Command "& { $rawUrl = 'https://raw.githubusercontent.com/optiscaler/OptiPatcher/main/OptiPatcher/dllmain.cpp'; try { $code = (Invoke-WebRequest -Uri $rawUrl -UseBasicParsing).Content } catch { return 'ERR' }; $supported = @(); $ueMatches = [Regex]::Matches($code, 'CHECK_UE\s*\(\s*([a-zA-Z0-9_]+)\s*\)'); foreach ($m in $ueMatches) { $base = $m.Groups[1].Value; $supported += ($base + '-win64-shipping.exe').ToLower(); $supported += ($base + '-wingdk-shipping.exe').ToLower(); }; $directMatches = [Regex]::Matches($code, 'exeName\s*==\s*[\x22\x27]([^\x22\x27]+)[\x22\x27]'); foreach ($m in $directMatches) { $supported += $m.Groups[1].Value.ToLower(); }; $localFiles = Get-ChildItem *.exe | Select-Object -ExpandProperty Name; foreach ($file in $localFiles) { if ($supported -contains $file.ToLower()) { Write-Output 'YES'; exit; }; }; Write-Output 'NO'; }"`) do (
    set "OPTI_MATCH=%%A"
)

if "!OPTI_MATCH!"=="YES" (
    echo.
    echo 检测到 OptiPatcher 支持！
    echo 这是 Opti 系列插件，用于解锁 DLSS／DLSS-FG 输入，在受支持的游戏里可以免去伪装和性能开销。
    echo 更多信息请见 OptiPatcher 的 Github
    echo.
	echo 是否下载 OptiPatcher.asi？
    echo.
	echo [1] 是
    echo [2] 否
    echo.
	set /p downloadOptiPatcher="等待输入 - "
    set downloadOptiPatcher=!downloadOptiPatcher: =!
    
    if "!downloadOptiPatcher!"=="1" (
        echo.
        echo 正在准备 plugins 文件夹……
        if not exist "OptiScaler\plugins" mkdir "OptiScaler\plugins"
        
        echo 正在下载 OptiPatcher……
        echo 如果卡住不动，请按 Ctrl+C 跳转到安装完成。
        echo.
        powershell -Command "Invoke-WebRequest -Uri 'https://github.com/optiscaler/OptiPatcher/releases/download/rolling/OptiPatcher.asi' -OutFile 'OptiScaler\plugins\OptiPatcher.asi'"
        if errorlevel 1 goto completeSetup
        
        if exist "OptiScaler\plugins\OptiPatcher.asi" (
            echo OptiPatcher.asi 下载成功。
            echo 正在 OptiScaler.ini 中启用 ASI 加载……
            if exist "%configFile%" (
                powershell -Command "(Get-Content '%configFile%') -replace 'LoadAsiPlugins=auto', 'LoadAsiPlugins=true' | Set-Content '%configFile%'"
                echo 已在 OptiScaler.ini 中成功启用 ASI 加载！
            ) else (
                echo 警告：未找到 OptiScaler.ini，无法启用 LoadAsiPlugins。
            )
        ) else (
            echo 下载 OptiPatcher.asi 失败。
        )
     timeout /t 3
    )
)
echo.

goto completeSetup

:completeSetup
REM 重命名 OptiScaler 文件
echo.
if "!overwriteChoice!"=="1" (
    echo 正在移除原有的 %selectedFilename%……
    del /F %selectedFilename% 
)

echo 正在把 OptiScaler 文件重命名为 %selectedFilename%……
rename "%optiScalerFile%" %selectedFilename%
if errorlevel 1 (
    echo.
    echo 错误：无法把 OptiScaler 文件重命名为 %selectedFilename%。最可能是文件夹权限问题。
    echo 请手动把 OptiScaler.dll 重命名为 %selectedFilename%！之后无需再次运行本安装脚本。
    echo.
    goto end
)

goto create_uninstaller

:create_uninstaller_return

cls
echo  OptiScaler 安装完成……
echo.
echo   ___                 
echo  (_         '        
echo  /__  /)   /  () (/  
echo          _/      /    
echo.

set setupSuccess=true

:end
pause

if "%setupSuccess%"=="true" (
    del "setup_linux.sh"
    del "%~nx0"
)

exit /b

:create_uninstaller
setlocal DisableDelayedExpansion

(
echo @echo off
echo chcp 65001 ^>nul 2^>nul
echo setlocal EnableDelayedExpansion
echo cls
echo echo  ::::::::  :::::::::  ::::::::::: :::::::::::  ::::::::   ::::::::      :::     :::        :::::::::: :::::::::  
echo echo :+:    :+: :+:    :+:     :+:         :+:     :+:    :+: :+:    :+:   :+: :+:   :+:        :+:        :+:    :+: 
echo echo +:+    +:+ +:+    +:+     +:+         +:+     +:+        +:+         +:+   +:+  +:+        +:+        +:+    +:+ 
echo echo +#+    +:+ +#++:++#+      +#+         +#+     +#++:++#++ +#+        +#++:++#++: +#+        +#++:++#   +#++:++#:  
echo echo +#+    +#+ +#+            +#+         +#+            +#+ +#+        +#+     +#+ +#+        +#+        +#+    +#+ 
echo echo #+#    #+# #+#            #+#         #+#     #+#    #+# #+#    #+# #+#     #+# #+#        #+#        #+#    #+# 
echo echo  ########  ###            ###     ###########  ########   ########  ###     ### ########## ########## ###    ### 
echo echo.
echo echo 原力与此脚本同在……
echo echo v2.8 - 现已支持 OptiPatcher
echo echo.
echo REM 检查是否存在 OptiScaler 安装
echo set "OLD_FILES_FOUND=0"
echo set "OPTI_DLL_LIST="
echo if exist OptiScaler.asi set "OLD_FILES_FOUND=1"

echo for %%%%F in ^(dxgi.dll winmm.dll d3d12.dll dbghelp.dll version.dll wininet.dll winhttp.dll^) do ^(
echo     if exist "%%%%F" ^(
echo         set "origname="
echo         for /f "tokens=*" %%%%P in ^('powershell -NoProfile -Command "(Get-Item '%%%%F').VersionInfo.OriginalFilename"'^) do ^(
echo             set "origname=%%%%P"
echo         ^)
echo         if /i "!origname!"=="OptiScaler.dll" ^(
echo             set "OLD_FILES_FOUND=1"
echo             set "OPTI_DLL_LIST=!OPTI_DLL_LIST! %%%%F"
echo         ^)
echo     ^)
echo ^)

echo if "!OLD_FILES_FOUND!"=="1" ^(
echo     echo 检测到已有的 OptiScaler 安装！
echo     if exist OptiScaler.asi echo   - OptiScaler.asi
echo     for %%%%F in ^(!OPTI_DLL_LIST!^) do echo   - %%%%F - 原始文件名：OptiScaler.dll
echo     echo.
echo ^)

echo echo 是否移除 OptiScaler？
echo echo.
echo echo [1] 是
echo echo [2] 否
echo echo.
echo set /p removeChoice="等待输入 - "
echo echo.

echo if "%%removeChoice%%"=="1" ^(
echo     del OptiScaler.log
echo     del OptiScaler.ini
echo     del OptiScaler.asi
echo     for %%%%F in ^(!OPTI_DLL_LIST!^) do ^(del "%%%%F"^)
echo     del /Q Licenses\*
echo     rd Licenses
echo     del /Q OptiScaler\D3D12_Optiscaler\*
echo     rd OptiScaler\D3D12_Optiscaler
echo     del /Q OptiScaler\Streamline\*
echo     rd OptiScaler\Streamline
echo     del /Q OptiScaler\streamline\*
echo     rd OptiScaler\streamline
echo     echo.
echo     echo 如果存在 OptiPatcher 也一并删除
echo     del /Q OptiScaler\plugins\*
echo     rd OptiScaler\plugins
echo     echo.
echo     del /Q OptiScaler\*
echo     rd OptiScaler
echo     echo.
echo     echo OptiScaler 已移除！忽略那些提示文件不存在的警告。
echo     echo.
echo ^) else ^(
echo     echo.
echo     echo 操作已取消。
echo     echo.
echo ^)

echo.
echo pause
echo if "%%removeChoice%%"=="1" ^(
echo     del "%%~nx0"
echo ^)
) > "Remove_OptiScaler.bat"

endlocal
echo.
echo 卸载脚本已生成。
echo.

goto create_uninstaller_return
