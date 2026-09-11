#!/usr/bin/env bash

show_help() {
    echo ""
    echo "用法：$0 [选项]"
    echo ""
    echo "选项："
    echo "  --filename=<string>        指定 OptiScaler.dll 的目标文件名，可选值："
    echo "                            - dxgi.dll"
    echo "                            - winmm.dll"
    echo "                            - version.dll"
    echo "                            - dbghelp.dll"
    echo "                            - d3d12.dll"
    echo "                            - wininet.dll"
    echo "                            - winhttp.dll"
    echo "                            - OptiScaler.asi"
    echo ""
    echo "  --overwrite=<y|n>       是否覆盖已存在的文件（y/n）"
    echo "  --using_nvidia=<y|n>    是否为 Nvidia 显卡（y/n）"
    echo "  --using_dlss=<y|n>      是否使用 DLSS 输入/伪装（y/n）"
    echo "  -h, --help              显示本帮助信息"
    echo ""
    echo "示例："
    echo "  $0 --filename=dxgi.dll --overwrite=y --using_nvidia=n --using_dlss=y"
    echo ""
    exit 0
}

for arg in "$@"; do
    case "$arg" in
        -h|--help) show_help ;;
        --filename=*) selected_filename="${arg#*=}" ;;
        --overwrite=*) overwrite_choice="${arg#*=}" ;;
        --using_nvidia=*) using_nvidia="${arg#*=}" ;;
        --using_dlss=*) using_dlss="${arg#*=}" ;;
    esac
done
clear

echo " ::::::::  :::::::::  ::::::::::: :::::::::::  ::::::::   ::::::::      :::     :::        :::::::::: :::::::::  "
echo ":+:    :+: :+:    :+:     :+:         :+:     :+:    :+: :+:    :+:   :+: :+:   :+:        :+:        :+:    :+: "
echo "#+:    +:+ +:+    +:+     +:+         +:+     +:+        +:+         +:+   +:+  +:+        +:+        +:+    +:+ "
echo "+#+    +:+ +#++:++#+      +#+         +#+     +#++:++#++ +#+        +#++:++#++: +#+        +#++:++#   +#++:++#:  "
echo "+#+    +#+ +#+            +#+         +#+            +#+ +#+        +#+     +#+ +#+        +#+        +#+    +#+ "
echo "#+#    #+# #+#            #+#         #+#     #+#    #+# #+#    #+# #+#     #+# #+#        #+#        #+#    #+# "
echo " ########  ###            ###     ###########  ########   ########  ###     ### ########## ########## ###    ### "
echo ""
echo "复制文件的功力不俗……"
echo ""

# 取得脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPTISCALER_FILE="$SCRIPT_DIR/OptiScaler.dll"

# 删除多余文件
rm -f "$SCRIPT_DIR/!! EXTRACT ALL FILES TO GAME FOLDER !!" 2>/dev/null
rm -f "$SCRIPT_DIR/setup_windows.bat" 2>/dev/null

# 检查 OptiScaler.dll 是否存在
if [ ! -f "OptiScaler.dll" ]; then
    echo "未找到 OptiScaler \"OptiScaler.dll\" 文件！"
    echo "请确认已把 OptiScaler 的全部文件解压到游戏目录。"
    echo ""
    echo "若是虚幻引擎（Unreal Engine）游戏，请在以下位置寻找游戏主程序："
    echo "- <path-to-game>/Game-or-Project-name/Binaries/Win64/"
    echo "- 请忽略 Engine 文件夹"
    echo ""
    read -p "按回车键退出..."
    exit 1
fi

# 虚幻引擎检测（无界面模式会跳过）
if [ -d "$SCRIPT_DIR/Engine" ] && [ -z "$selected_filename" ]; then
    echo "检测到 Engine 文件夹。如果这是虚幻引擎游戏，请把 OptiScaler 解压到 #CODENAME#/Binaries/Win64"
    echo ""

    while true; do
        read -p "是否继续安装到当前文件夹？[y/n]：" continue_choice
        continue_choice=$(echo "$continue_choice" | tr -d ' ')

        if [ "$continue_choice" = "y" ] || [ "$continue_choice" = "Y" ]; then
            break
        elif [ "$continue_choice" = "n" ] || [ "$continue_choice" = "N" ]; then
            echo "已取消安装。"
            read -p "按回车键退出..."
            exit 0
        fi
    done
fi

select_filename() {
    # 若已指定合法文件名则直接跳过
    if [ -n "$selected_filename" ]; then
        case "$selected_filename" in
            dxgi.dll|winmm.dll|version.dll|dbghelp.dll|d3d12.dll|wininet.dll|winhttp.dll|OptiScaler.asi)
                return
                ;;
            *)
                echo "文件名无效：$selected_filename"
                exit 1
                ;;
        esac
    fi
    
    while true; do
        echo ""
        echo "请为 OptiScaler 选择一个文件名（默认为 dxgi.dll）："
        echo " [1] dxgi.dll"
        echo " [2] winmm.dll"
        echo " [3] version.dll"
        echo " [4] dbghelp.dll"
        echo " [5] d3d12.dll"
        echo " [6] wininet.dll"
        echo " [7] winhttp.dll"
        echo " [8] OptiScaler.asi"

        read -p "请输入 1-8（直接回车使用默认值）：" filename_choice

        case "$filename_choice" in
            ""|"1")
                selected_filename="dxgi.dll"
                ;;
            "2")
                selected_filename="winmm.dll"
                ;;
            "3")
                selected_filename="version.dll"
                ;;
            "4")
                selected_filename="dbghelp.dll"
                ;;
            "5")
                selected_filename="d3d12.dll"
                ;;
            "6")
                selected_filename="wininet.dll"
                ;;
            "7")
                selected_filename="winhttp.dll"
                ;;
            "8")
                selected_filename="OptiScaler.asi"
                ;;
            *)
                clear
                echo "Invalid choice. Please select a valid option."
                echo ""
                continue
                ;;
        esac

        # 检查目标文件是否已存在
        if [ -f "$selected_filename" ]; then
            echo ""
            echo "警告：当前文件夹中已存在 $selected_filename。"
            echo ""
            
            if [ -n "$overwrite_choice" ]; then
                if [[ "$overwrite_choice" =~ ^(yes|y)$ ]]; then
                    break
                else
                    echo "文件已存在，且 overwrite_choice=$overwrite_choice，退出。"
                    exit 1
                fi
            fi

            while true; do
                read -p "是否覆盖它？[y/n]：" overwrite_choice
                overwrite_choice=${overwrite_choice,,} 

                if [[ "$overwrite_choice" =~ ^(yes|y)$ ]]; then
                    break 2  # 跳出两层循环
                elif [[ "$overwrite_choice" =~ ^(no|n)$ ]]; then
                    clear
                    break  # 跳出内层循环，重新选择文件名
                else
                    clear
                    echo "输入无效，请输入 'y' 或 'n'。"
                fi
            done
	    else
            break  # 文件不存在，可以直接继续
        fi
    done
}

select_filename

# 尝试检测 Nvidia 显卡
NVIDIA_DETECTED=false
if command -v nvidia-smi >/dev/null 2>&1; then
    if nvidia-smi >/dev/null 2>&1; then
        NVIDIA_DETECTED=true
        echo "检测到 Nvidia 显卡。"
    fi
fi

while [ -z "$using_nvidia" ]; do
    echo ""
    if [ "$NVIDIA_DETECTED" = true ]; then
        default_value="y"
        read -r -p "你使用的是 Nvidia 显卡吗 [Y/n]：" using_nvidia
    else
        default_value="n"
        read -r -p "你使用的是 Nvidia 显卡吗 [y/N]：" using_nvidia
    fi

    using_nvidia=${using_nvidia,,}
    using_nvidia=${using_nvidia:-$default_value}
    
    if [[ "$using_nvidia" =~ ^(no|n)$ ]]; then
        while [ -z "$using_dlss" ]; do
            echo ""
            read -r -p "是否使用 DLSS 输入？（会启用伪装，DLSS 帧生成与 Reflex→AL2 需要它）[Y/n]：" using_dlss

            using_dlss=${using_dlss,,}
            using_dlss=${using_dlss:-y}

            if [[ "$using_dlss" =~ ^(no|n)$ ]]; then
                # 关闭伪装
                config_file="OptiScaler.ini"
                if [ ! -f "$config_file" ]; then
                    echo "未找到配置文件：$config_file"
                    read -p "按回车键继续..."
                else
                    # 用 sed 把 Dxgi=auto 改成 Dxgi=false
                    sed -i 's/Dxgi=auto/Dxgi=false/g' "$config_file"
                    echo "已在配置文件中关闭伪装。"
                fi
                break
            elif [[ "$using_dlss" =~ ^(yes|y)$ ]]; then
                break
            else
                echo "输入无效，请输入 'y' 或 'n'。"
                continue
            fi
        done
        break
    elif [[ "$using_nvidia" =~ ^(yes|y)$ ]]; then
        break
    else
        echo "输入无效，请输入 'y' 或 'n'。"
        continue
    fi
done

# 重命名 OptiScaler 文件
echo ""
if [ "$overwrite_choice" = "y" ] || [ "$overwrite_choice" = "Y" ]; then
    echo "正在删除原有的 $selected_filename……"
    rm -f "$selected_filename"
fi

echo "正在把 OptiScaler 文件重命名为 $selected_filename……"
if ! mv "$OPTISCALER_FILE" "$selected_filename"; then
    echo ""
    echo "错误：无法把 OptiScaler 文件重命名为 $selected_filename。"
    echo "请检查文件权限后重试。"
    read -p "按回车键退出..."
    exit 1
fi

# 生成卸载脚本
create_uninstaller() {
    cat > "remove_optiscaler.sh" << 'EOF'
#!/usr/bin/env bash

show_help() {
    echo ""
    echo "用法：$0 [选项]"
    echo ""
    echo "选项："
    echo "  --remove=<y|n>    确认卸载（y/n）"
    echo "  -h, --help        显示本帮助信息"
    echo ""
    exit 0
}

for arg in "$@"; do
    case "$arg" in
        -h|--help) show_help ;;
        --remove=*) remove_choice="${arg#*=}" ;;
    esac
done

clear
echo " ::::::::  :::::::::  ::::::::::: :::::::::::  ::::::::   ::::::::      :::     :::        :::::::::: :::::::::  "
echo ":+:    :+: :+:    :+:     :+:         :+:     :+:    :+: :+:    :+:   :+: :+:   :+:        :+:        :+:    :+: "
echo "#+:    +:+ +:+    +:+     +:+         +:+     +:+        +:+         +:+   +:+  +:+        +:+        +:+    +:+ "
echo "+#+    +:+ +#++:++#+      +#+         +#+     +#++:++#++ +#+        +#++:++#++: +#+        +#++:++#   +#++:++#:  "
echo "+#+    +#+ +#+            +#+         +#+            +#+ +#+        +#+     +#+ +#+        +#+        +#+    +#+ "
echo "#+#    #+# #+#            #+#         #+#     #+#    #+# #+#    #+# #+#     #+# #+#        #+#        #+#    #+# "
echo " ########  ###            ###     ###########  ########   ########  ###     ### ########## ########## ###    ### "
echo ""
echo "复制文件的功力不俗……"
echo ""

if [ -z "$remove_choice" ]; then
    read -p "确定要卸载 OptiScaler 吗？[y/n]：" remove_choice
fi

if [ "$remove_choice" = "y" ] || [ "$remove_choice" = "Y" ]; then
    echo ""
    echo "正在删除 OptiScaler 文件……"
    
    # 删除 OptiScaler 相关文件
    rm -f OptiScaler.log
    rm -f OptiScaler.ini
    rm -f SELECTED_FILENAME_PLACEHOLDER
    rm -f fakenvapi.dll
    rm -f fakenvapi.ini
    rm -f fakenvapi.log
    rm -f dlssg_to_fsr3_amd_is_better.dll
    rm -f dlssg_to_fsr3.log
    
    # 删除目录
    rm -rf D3D12_Optiscaler
    rm -rf DlssOverrides
    rm -rf Licenses
    
    echo ""
    echo "OptiScaler 已卸载完成！"
    echo ""
    
    # 删除本卸载脚本自身
    rm -f "$0"
else
    echo ""
    echo "操作已取消。"
    echo ""
fi

if [ $# -eq 0 ]; then
    read -p "按回车键退出..."
fi
EOF

    # 把占位符替换成实际选择的文件名
    sed -i "s/SELECTED_FILENAME_PLACEHOLDER/$selected_filename/g" "remove_optiscaler.sh"
    
    # 赋予卸载脚本执行权限
    chmod +x "remove_optiscaler.sh"
    
    echo ""
    echo "已生成卸载脚本：remove_optiscaler.sh"
    echo ""
}

# 生成卸载脚本
create_uninstaller

# 安装成功提示
clear
echo " OptiScaler 安装完成……"
echo ""
echo "  ___                 "
echo " (_         '        "
echo " /__  /)   /  () (/  "
echo "         _/      /    "
echo ""

# 显示 Wine 的 DLL 覆盖设置说明
echo "Linux / Wine 用户请注意："
echo "你可能需要把重命名后的 DLL 加入 Wine 的 DLL 覆盖列表"
echo "例如在 Steam 中，把下面这行加入启动选项："
echo ""
echo "WINEDLLOVERRIDES=$selected_filename=n,b %COMMAND%"
echo ""
echo "请记住：Insert 键打开 OptiScaler 叠加界面，Page Up/Down 查看性能统计"
echo ""

# 收尾：删除安装脚本自身
if [ $# -eq 0 ]; then
    read -p "按回车键退出..."
fi

rm -f "$0"

exit 0
