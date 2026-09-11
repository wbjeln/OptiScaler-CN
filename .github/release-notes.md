## OptiScaler 简体中文版

把开源画质增强注入工具 [OptiScaler](https://github.com/OptiScaler/OptiScaler) 全项目汉化，
并由 GitHub Actions 云端编译成**解压即用**的 Windows 版本。

### 下载

| 附件 | 用途 |
| --- | --- |
| **`OptiScaler-CN.zip`** | **成品运行包** —— 解压到游戏目录即可使用 |
| `OptiScaler-CN-source.zip` | 汉化后的完整源码（GPLv3 要求随二进制一并提供） |
| `localization.patch` | 「上游锁定版本 → 汉化版」的差异补丁。上游更新后，把它应用到新版上游即可自动合并大部分汉化改动，详见《更新上游.md》 |

### 安装（3 步）

1. 把包内**全部文件**解压到**游戏主程序 exe 所在目录**
   （虚幻引擎游戏通常是 `<游戏目录>\<项目名>\Binaries\Win64`，**不要**解压进 `Engine`）
2. 双击 **`setup_windows.bat`**，按中文提示选择注入文件名
   （默认 `dxgi.dll` 兼容性最好；Vulkan 游戏选 `winmm.dll`）
3. 启动游戏，默认按 **`Insert`** 键呼出设置菜单

详细的安装说明与常见问题排查见包内 **`使用说明.txt`**，配置项逐条解释见 `文档/`。

### 汉化内容

- 设置菜单、提示弹窗 —— 全中文
- `OptiScaler.ini` 配置注释 —— 全中文（**键名与取值与官方完全一致，配置文件可通用**）
- `setup_windows.bat` / `setup_linux.sh` 安装脚本提示 —— 全中文
- 中文字体（思源黑体子集）**已内嵌进 DLL**，无需另外安装字体
- 叠加界面的窗口标题会显示 `... 简体中文版`
- 附带**一键卸载器**（卸载 OptiScaler.bat），只删确认属于 OptiScaler 的文件，
  不会误删游戏或 ReShade 自带的同名 DLL

功能逻辑与官方版本完全一致，未做任何改动。数值版本号保持为 `10.0.0`。

### 本次构建的自动校验结果

构建流程会在编译完成后自动验证汉化确实生效（任一不通过即判定失败）：

- DLL 中含中文界面串与「简体中文版」版本标识
- `OptiScaler.ini` 中文注释行数 > 500
- `setup_windows.bat` 含中文提示且为 CRLF 换行
- `setup_linux.sh` 含中文提示且不含 CR（CRLF 会让 Linux 报 `bad interpreter`）

### 授权

GNU GPLv3（与上游一致），全文见包内 `LICENSE-GPLv3.txt`。
内嵌的思源黑体子集以 SIL Open Font License 1.1 授权。
本汉化版由第三方制作，**与 OptiScaler 原作者无关**，仅供学习交流使用，
因使用本软件产生的一切后果由使用者自行承担。

> 原始项目：<https://github.com/OptiScaler/OptiScaler>
