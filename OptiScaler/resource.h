//{{NO_DEPENDENCIES}}
// Microsoft Visual C++ generated include file.
// Used by OptiScaler.rc
//
#ifdef _DEBUG
#define VER_BUILD_DATE "Debug Build"
#define VER_BUILD_COMMIT "Debug"
#else
#include "resource_build_date.h"
#include "resource_build_commit.h"
#endif // !_DEBUG

#define VS_VERSION_INFO 1

// Next default values for new objects
//
#ifdef APSTUDIO_INVOKED
#ifndef APSTUDIO_READONLY_SYMBOLS
#define _APS_NEXT_RESOURCE_VALUE 101
#define _APS_NEXT_COMMAND_VALUE 40001
#define _APS_NEXT_CONTROL_VALUE 1001
#define _APS_NEXT_SYMED_VALUE 101
#endif
#endif

#define STRINGIZE_(s) #s
#define STRINGIZE(s) STRINGIZE_(s)

#define VER_MAJOR_VERSION 10
#define VER_MINOR_VERSION 0
#define VER_HOTFIX_VERSION 0
#define VER_BUILD_NUMBER 1

#define VER_DEV_RELEASE
// #define VER_PRE_RELEASE

#define VER_FILE_VERSION VER_MAJOR_VERSION, VER_MINOR_VERSION, VER_HOTFIX_VERSION, VER_BUILD_NUMBER
#define VER_FILE_VERSION_STR                                                                                           \
    STRINGIZE(VER_MAJOR_VERSION) "." STRINGIZE(VER_MINOR_VERSION) "." STRINGIZE(VER_HOTFIX_VERSION) "." STRINGIZE(VER_BUILD_NUMBER)
#define OPTI_VERSION STRINGIZE(VER_MAJOR_VERSION) "." STRINGIZE(VER_MINOR_VERSION) "." STRINGIZE(VER_HOTFIX_VERSION)

#define VER_PRODUCT_VERSION VER_FILE_VERSION

// 汉化版标识。刻意只加在「给人看」的版本串上：
//   · OPTI_VERSION 是纯 "x.y.z"，会被传给 DLSS / XeSS / FSR 的引擎注册接口
//     （见 inputs/*.cpp 里的 OPTI_VERSION 参数），版本更新检查也依赖它，
//     所以必须与上游完全一致，不能加任何后缀。
//   · VER_PRODUCT_VERSION_STR 只用于日志与叠加界面的窗口标题
//     （menu_common.cpp 里的 windowTitle），在这里标注汉化版是安全的。
#define VER_LOCALIZED_SUFFIX " 简体中文版"

#ifdef VER_DEV_RELEASE
#define VER_PRODUCT_VERSION_STR                                                                                        \
    STRINGIZE(VER_MAJOR_VERSION) "." STRINGIZE(VER_MINOR_VERSION) "." STRINGIZE(VER_HOTFIX_VERSION) "-dev (" VER_BUILD_COMMIT ") (" VER_BUILD_DATE ")" VER_LOCALIZED_SUFFIX
#elif VER_PRE_RELEASE
#define VER_PRODUCT_VERSION_STR                                                                                        \
    STRINGIZE(VER_MAJOR_VERSION) "." STRINGIZE(VER_MINOR_VERSION) "." STRINGIZE(VER_HOTFIX_VERSION) "-pre" STRINGIZE(VER_BUILD_NUMBER) " (" VER_BUILD_COMMIT ") (" VER_BUILD_DATE ")" VER_LOCALIZED_SUFFIX
#else
#define VER_PRODUCT_VERSION_STR                                                                                        \
    STRINGIZE(VER_MAJOR_VERSION) "." STRINGIZE(VER_MINOR_VERSION) "." STRINGIZE(VER_HOTFIX_VERSION) "-final (" VER_BUILD_COMMIT ")" VER_LOCALIZED_SUFFIX
#endif // VER_PRE_RELEASE

#define VER_PRODUCT_NAME "OptiScaler v" VER_PRODUCT_VERSION_STR
