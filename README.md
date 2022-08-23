<!--
    coding = utf-8
    author: holger
    version: 4.0.1
    license: AGPL-3.0
    belong: DailyReport-BasicDataFile
-->

# DailyReport (stable)

Daily health report automated program. 每日打卡自动化程序（适用于苏州大学）

**推荐** 👉 [下载编译发行版本](https://github.com/HolgerZhang/DailyReport/releases/latest)

v4.0.1 by HolgerZhang

> 感谢 [@ygLance](https://github.com/ygLance) 和 [@TTL2000](https://github.com/TTL2000) 的测试。


## 特性一览

- 基于模拟点击（selenium）的自动化健康打卡；
- 定时任务功能：可指定时间进行打卡；
- 支持为多人打卡；
- 执行出错自动重复5次，防止网络问题导致的打卡失败；
- 邮件提醒：打卡成功或失败会向指定邮箱发送邮件，需配置邮箱；
- 自动更新打卡配置，配置文件长期维护；
- 自动初始化系统；
- 保存系统执行日志；
- 【新增】实现多人多线程打卡；
- 【新增】邮件中隐藏密码；
- 【新增】浏览器无界面模式，后台静默执行；
- 【新增】检测配置文件变化并自动重载。


## 使用前注意

> v4 不再向下兼容 [v2](https://github.com/HolgerZhang/DailyReport/tree/v2) 的配置文件以及启动方法；

- 源码版本环境依赖：带有 pip 的 Python 3.8+ 环境；安装有浏览器（应为最新版，支持情况请查阅 [文档](https://www.selenium.dev/downloads/) ）
- [编译发行版本](https://github.com/HolgerZhang/DailyReport/releases/latest) 支持平台：Windows (x86_64/arm64)，Linux (x86_64，实验性)，macOS (Intel/Apple Silicon)
- 支持浏览器：Chrome，Edge，Firefox （仅Chrome支持自动驱动下载）
- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp)

### 免责声明

- 每日打卡自动化程序 DailyReport（下简称“此软件”）仅供自动化测试使用，使用时不应该带有扰乱正常秩序的目的，不得作为商业目的使用；
- 此软件只适用于自动化测试等有关技术等用途。<strong>如果你出现身体不适、身处疫情地区等等情况，请及时反映情况，不得瞒报！！</strong>
- 此软件基于 AGPL-3.0 开源协议，引用此项目请保留开源协议并开放源代码，不得恶意修改（包括但不限于源代码、配置文件等）；
- 此软件使用时需要保持开机并联网，且需保证网络通畅，能够访问目标网站。使用此软件时需留意日志文件信息以及自行 [查询](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp) 是否打卡成功。由于网络问题、目标页面更新等导致的打卡失败、不能连续打卡等问题，此软件以及作者不承担任何责任；
- 其余未尽事宜，此软件以及作者保留解释权利；
- 使用此软件，默认接受以上声明；如不接受，请删除本软件。

## 使用方法

### 使用方法（从源码运行）

1. 阅读《免责声明》，接受方可继续。
2. 运行 `python3 -m pip install -r requirements.txt'` 安装依赖
3. 运行 `python3 main.py --initialize` 初始化并下载配置文件；
4. 首次运行请预先根据 configurations/introduction.general.json 配置 configurations 目录下 general.json 文件 （可参考 example.general.json ）；
   根据 configurations/introduction.user.json 配置 configurations 目录下 user.用户名.json 文件；
5. 运行 `python3 main.py` 或添加参数运行开始使用。

### 使用方法（编译发行版本，DailyReport主程序）

1. 阅读《免责声明》，接受方可继续。
2. [下载](https://github.com/HolgerZhang/DailyReport/releases/latest) 压缩包并解压。
3. 在命令行（PowerShell/CMD/bash/zsh等）运行DailyReport程序：
   1. 运行 `./DailyReport --initialize` 初始化并下载配置文件;
   2. 首次运行请预先根据 configurations/introduction.general.json 配置 configurations 目录下 general.json 文件 （可参考 example.general.json ）；
   根据 configurations/introduction.user.json 配置 configurations 目录下 user.用户名.json 文件；
   3. 运行 `./DailyReport` 或添加参数运行开始使用。

### main.py/DailyReport主程序的运行参数

- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp)
- 添加参数 `-o` 或 `--once` 以单次运行程序
- 添加参数 `-l` 或 `--local` 以关闭自动检查更新特性，而是使用本地存在的文件
- 添加参数 `-c CONFIG` 或 `--config CONFIG` 从指定的配置文件运行，默认为 "configurations/general.json" （主程序不监听配置文件的变化）
- 添加参数 `-u USER` 或 `--user USER` 来在用户配置文件的目录生成 "user.${USER}.json" 文件

### 进程守护实用工具DailyReport.Watcher的使用方法

本程序（未编译的watch.py/已编译的DailyReport.Watcher）仅适用于编译发行版本的DailyReport主程序。

主要功能：以默认的方式启动并管理计算机上的所有DailyReport进程；
监听配置文件的修改、移动和删除变化，并自动重载DailyReport进程；
可以指定DailyReport程序位置以及用户自定义配置文件general.json的位置。

在命令行运行DailyReport.Watcher程序即可，运行该程序不需要手动运行DailyReport主程序。

参数说明：

- 参数 `-c CONFIG` 或 `--config CONFIG` 从指定的配置文件运行，默认为运行目录下的 "configurations/general.json"
- 参数 `-e EXE` 或 `--exe EXE` 来指定DailyReport程序位置，默认为为运行目录下的 "DailyReport"（Windows） 或 "DailyReport"（其他）
- 参数 `-o true|false` 或 `--output true|false` 来指定DailyReport是否输出运行信息（默认为输出）。

### 实验性功能列表

以下功能因测试覆盖率不足、专为开发人员设计等原因，尚处于实验性阶段，不保证功能的可用性。

- 【Linux服务器版】 程序对Linux服务器等无显示设备的硬件平台的支持处于实验性阶段。
- 【自动初始化Edge/Firefox驱动程序】 因尚未解决固定API的问题，暂不支持自动下载驱动程序，需要根据提示手动下载。
- 【调试模式】 （开发人员选项）使用环境变量 `BOT_CORE_DEBUG=TRUE` 以在 bot 执行时输出调试信息，并添加必要断点。
- 【图形化模式】 （开发人员选项）使用环境变量 `BOT_CORE_DISPLAY=TRUE` 来使用浏览器的图形化界面（默认使用无界面模式）。
- 【可变邮件休眠时间】 （开发人员选项）使用环境变量 `EMAIL_SENDER_SLEEP_MAX_INT` 来修改邮件发送的最大休眠间隙（默认10秒）。
- 【阻止驱动程序初始化】 （开发人员选项）定义环境变量 `_BOT_BUILD_NOT_DOWNLOAD` 来阻止初始化时下载驱动程序。

## 更新说明

#### v4.0.1

内部版本号：BUILD.4010-2.8.21
正式版本号：4.0.1-beta-FIX01

- 【优化】Mapping更新
- 【优化】修复了若干影响使用体验的bug
- 【优化】更新编译脚本

对于不使用进程守护实用工具DailyReport.Watcher的 v4 正式版（stable/RTM）的用户，仅需替换 `data/version.json` 文件，并再次初始化即可。

#### v4.0.0

内部版本号：BUILD.3990-2.5.15
正式版本号：4.0-stable

- 【重构】新版本重构，优化代码结构；
- 【新增】实现多人多线程打卡；
- 【新增】邮件中隐藏密码；
- 【新增】浏览器无界面模式，默认启用；
- 【新增】进程守护实用工具DailyReport.Watcher（watcher.py），可以对编译版本的进程进行简单的管理，独占支持general文件变更自动重载功能；
- 【新增】提供编译的文件(build.sh，需要pip、zip命令的支持)；
- 【优化】完善了版本号的计算，加入扩展版本号；
- 【优化】每次执行时读取系统配置及用户信息文件；
- 【优化】调整日志输出，方便定位问题；
- 【优化】修复并发链接数过大导致的邮件发送失败的问题；
- 【优化】优化邮件内容；
- 【优化】修复邮件重发时不能正确发送的问题；
- 【优化】修复邮件文本替换时可能造成的异常；
- 【优化】修复邮件文本替换的多次转义；
- 【优化】成功发送时不再向发件人发送邮件；
- 【优化】完整支持全平台的Chrome、Edge以及FireFox浏览器（不包括驱动初始化），移除对其余浏览器的支持；
- 【优化】修复DailyReport.Watcher工具在Windows平台上存在的bug；
- 【优化】优化DailyReport.Watcher工具的细节与稳定性。

整合的历史版本：v4.0.0(BUILD.A001)，BUILD.A002-HLO0313，BUILD.A002-HOL0320，BUILD.A002-HOL0321，BUILD.A003-HOL0325，BUILD.3910-2.5.4-alpha，BUILD.3980-2.5.13-alpha，BUILD.3981-2.5.13，BUILD.3983-2.5.14(for watcher)，BUILD.3984-2.5.14，BUILD.3985-2.5.15。

## 其他

### Q&A

- 运行失败，日志显示异常信息为：NoSuchElementException
  - 解决办法：检查 user 信息是否有误
- 浏览器有关的错误
  - 解决办法：更新浏览器后请及时更新驱动程序（Chrome可以使用-i选项初始化）
- 我想要立刻执行一次打卡
  - 解决办法：运行时添加 `--once` 参数

### 本项目使用到的外部API网址（v4版本）

- 根地址：[https://api.holgerbest.top/DailyReport/v4/](https://api.holgerbest.top/DailyReport/v4/)
- `data/mapping.json`（配置文件，初始化以及检查更新时下载）：[https://api.holgerbest.top/DailyReport/v4/mapping/](https://api.holgerbest.top/DailyReport/v4/mapping/)
- `user.用户名.json`（用户配置文件，使用 -u 选项下载）：[https://api.holgerbest.top/DailyReport/v4/user/](https://api.holgerbest.top/DailyReport/v4/user/)
- 版本号API：[https://api.holgerbest.top/DailyReport/v4/version/](https://api.holgerbest.top/DailyReport/v4/version/)


### 历史版本

- [v4-FIX01]
- [v4(RTM)](https://github.com/HolgerZhang/DailyReport/releases/tag/v4.0.0-RTM) | 结束支持时间：与v4.0稳定版相同；
- [v4(RC2/RC2p)](https://github.com/HolgerZhang/DailyReport/releases/tag/v4.0.0-RC2) | 结束支持时间：2022-05-20；
- [v4(RC1)](https://github.com/HolgerZhang/DailyReport/releases/tag/v4.0.0-RC1) | 结束支持时间：2022-05-20；
- [v4(RC-pre-3980)](https://github.com/HolgerZhang/DailyReport/releases/tag/v4.0.0-3980-2.5.13-alpha) | 结束支持时间：2022-05-20；
- [v4(Beta-3910)](https://github.com/HolgerZhang/DailyReport/releases/tag/v4.0.0-3910-2.5.4-alpha) | 结束支持时间：2022-05-20；
- [v2.5](https://github.com/HolgerZhang/DailyReport/releases/tag/v2.5) | 结束支持时间：2022-06-01；
- [v2.4](https://github.com/HolgerZhang/DailyReport/releases/tag/v2.4) | 已经结束支持；
- [v2.3](https://github.com/HolgerZhang/DailyReport/releases/tag/v2.3) | 已经结束支持；
- [v2.1](https://github.com/HolgerZhang/DailyReport/releases/tag/v2.1) | 已经结束支持；
- [v3.0](https://github.com/HolgerZhang/DailyReport/releases/tag/v3.0) | 已经结束支持；
- [v2.0](https://github.com/HolgerZhang/DailyReport/releases/tag/v2.0) | 已经结束支持。

### 版本说明与计划

第一位版本号为主要版本，包含大量功能更新与问题修复，版本不向下兼容，启用新的分支；
第二位版本号为迭代版本，包含在下一主要版本开发计划前的新功能更新与及时的问题修复，在同一主要版本内向下兼容；
第三位版本号为更新版本，只包含问题修复，不含新的功能更新。

v4.1主要计划：

- 进程守护实用工具DailyReport.Watcher新增对源码运行的进程进行管理；
- 进程守护实用工具DailyReport.Watcher新增对系统内多个进程并行运行的支持；
- 主程序 `--local` 模式增强计划，支持在无外网的校园网内完整运行。

v4.2主要计划：

- 进程守护实用工具DailyReport.Watcher的图形化支持；
- ……
