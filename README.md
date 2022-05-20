<!--
    coding = utf-8
    author: holger version: 2.5
    license: AGPL-3.0
    belong: DailyReport-BasicDataFile
-->

# DailyReport (stable)

Daily health report automated program. 每日打卡自动化程序【苏大】

v2.5 by HolgerZhang

with [SUMSC/email-sender](https://github.com/SUMSC/email-sender) v0.1.2

coding: UTF-8

有关实现细节详见[链接](https://holgerbest.top/2021/01/19/python-selenium/)

> 感谢 [@ygLance](https://github.com/ygLance) 和 [@TTL2000](https://github.com/TTL2000) 的测试。

### Version 4 正式发布！

经过前期测试， [Version 4](https://github.com/HolgerZhang/DailyReport/tree/v4) 版本的 [正式版](https://github.com/HolgerZhang/DailyReport/releases/latest) 已经发布并全面推送。新版本包含大量新功能更新、性能优化与错误修复，并提供了编译版本，强烈建议升级！

新版本特性：

- 新版本重构，优化代码结构；
- 支持多人多线程打卡；
- 邮件中隐藏密码；
- 新增浏览器无界面模式；
- 新增进程守护实用工具DailyReport.Watcher对进程管理，支持文件变更自动重载。

> v2.5 的支持截至2022年6月；结束支持后，该分支将随时被标记为 End of Life。

### 使用前注意

> v2.x 不再向下兼容 [v1.x](https://github.com/HolgerZhang/DailyReport/tree/v1-end-of-life) 的部分配置文件以及启动方法
> 
> v2.5 不再向下兼容 [v2](https://github.com/HolgerZhang/DailyReport/tree/v2) 分支较早版本的启动方法，建议全新安装
> 
> v2.4 及以前所有版本的支持周期均已停止，请尽快升级至 v2.5 版本

- 环境依赖：带有 pip 的 Python 3 环境；系统装有 **最新版** [Chrome 浏览器](https://www.google.cn/intl/zh-CN/chrome/)
- 支持系统：Windows (x86 64 bit) | Linux (x86 64 bit) | macOS (Intel / Apple Silicon)
  > 受 Chrome driver 的限制，不支持 Arm 架构的 Windows 与 Linux；暂不支持无图形化界面的服务器系统。
- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp) （该页面也会在打卡结束时停留10秒）

#### 免责声明

- 每日打卡自动化程序 DailyReport（下简称“此软件”）仅供自动化测试使用，使用时不应该带有扰乱正常秩序的目的，不得作为商业目的使用；
- 此软件只适用于自动化测试等有关技术等用途。<strong>如果你出现身体不适、身处疫情地区等等情况，请及时反映情况，不得瞒报！！</strong>
- 此软件基于 AGPL-3.0 开源协议，引用此项目请保留开源协议并开放源代码，不得恶意修改（包括但不限于源代码、配置文件等）；
- 此软件使用时需要保持开机并联网，且需保证网络通畅，能够访问目标网站。使用此软件时需留意日志文件信息以及自行 [查询](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp) 是否打卡成功。由于网络问题、目标页面更新等导致的打卡失败、不能连续打卡等问题，此软件以及作者不承担任何责任；
- 其余未尽事宜，此软件以及作者保留解释权利；
- 使用此软件，默认接受以上声明；如不接受，请删除本软件。

### 使用【v2.5+使用必看】

1. 阅读《免责声明》，接受方可继续。
2. 运行 `python3 -m pip install -r requirements.txt'` 安装依赖，（需要升级pip版本到22.0.3）

   升级方法 `python3 -m pip install --upgrade pip`

3. 运行 `python3 main.py --initialize` 初始化并下载配置文件，首次运行请预先配置 data 目录下 json 文件
4. 运行 `python3 main.py` 开始使用； 

    后台运行方法：使用 nohup `nohup python3 main.py >> /dev/null 2>&1 &`；
    结束运行请自行kill：`ps -aux | grep 'python3 main.py'` 记录pid，`kill <pid>`

- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp)
- 添加参数 `-u` 或 `--update-only` 手动更新配置文件
- 添加参数 `-m` 或 `--disable-monitor` 关闭文件变更自动加载特性
- 添加参数 `-o` 或 `--once` 以单次运行程序
- 添加参数 `-l` 或 `--local` 彻底关闭自动检查更新特性，而是使用本地存在的文件
- 添加参数 `-idx INDEX` 或 `--user-index INDEX` 使程序只为用户编号（从0开始）为 INDEX 的用户打卡（为负数则为所有人打卡）
- 使用环境变量 `BOT_CORE_DEBUG=TRUE` 以在 bot 执行时输出调试信息
- 使用环境变量 `BOT_CORE_NO_GUI=TRUE` 以关闭弹窗提醒

### 更新说明

- v2.0 (end-of-life) **全面重构**。将业务逻辑与代码分离，便于后续升级；支持为多人打卡，向 user 配置文件 information 中新增格式相同的 JSON 对象即可；全新日志模块，输出、异常信息一目了然；具备安装程序，一键安装依赖。
- v2.1 (fatal-error end-of-life) 修复自带的 Chrome 驱动过于老旧的问题；修复一定概率的网页元素定位失败的问题；打卡结束时将结果停留展示 10 秒；添加输出调试信息选项。【存在严重BUG：有一定概率定位元素发生偏移，导致打卡地点不受控制，强烈建议升级】
- v2.2 (bug fix end-of-life) 修复 2.1 版本的 BUG；执行出错自动重复5次，防止网络问题导致的打卡失败；优化系统稳定性。可能存在 mapping 文件的问题，建议删除原有 data/mapping.json 文件重新下载（下载链接： [mapping](https://api.holgerbest.top/DailyReport/v2/mapping/) ），并删除 .cmp_dat 文件夹。
- v2.3 (end-of-life) 新增对 Apple Silicon 的支持；日志分级，优化输出；优化系统稳定性。
- v2.4 (error-existed end-of-life) 新增邮件提醒（ 源自：[SUMSC/email-sender](https://github.com/SUMSC/email-sender) ），打卡成功或失败会向指定邮箱发送邮件，需配置邮箱，参考原项目。
- v2.5 (stable) 修复 Bot 当元素未找到时模拟点击不抛出异常的问题；非核心脚本重构，缩减脚本数量，优化命令行参数体验；完美支持彻底关闭自动检查更新；新增支持手动更新配置文件；新增支持只为特定某个用户编号（从0开始）的用户打卡；将邮件配置作为系统配置项之一进行管理（监听更新，不监听变更）；其他优化。

### Q&A

- 运行 setup 报错：找不到库 requests
  - 解决办法：预先手动安装 requests：`pip install requests`
- 运行setup 后弹窗提示：请安装或更新Chrome
  - 解决办法：请保证电脑中安装了**最新**版本的Chrome浏览器
- 运行失败后弹窗：捕获异常，log 文件显示异常信息为：NoSuchElementException
  - 解决办法：检查 user 信息是否有误
- 运行失败后弹窗：捕获未知异常；或捕获异常，log 文件显示异常信息不为 NoSuchElementException
  - 解决办法：联系作者[邮箱](mailto:holgerzhang@outlook.com) 
- 我想要立刻执行一次打卡
  - 解决办法：运行 main.py 添加 `--once` 参数
- 我想要手动填写体温数据【请手动打卡 :) 】

### API v2

- 根地址：[https://api.holgerbest.top/DailyReport/v2/](https://api.holgerbest.top/DailyReport/v2/)
- `data/mapping.json`（配置文件，首次启动下载）：[mapping](https://api.holgerbest.top/DailyReport/v2/mapping/)
- `data/user.json`（用户信息配置文件，首次启动下载，需填写信息）：[user](https://api.holgerbest.top/DailyReport/v2/user/)
- `data/scheduler.json`（定时任务配置文件，首次启动下载，需填写信息）：[scheduler](https://api.holgerbest.top/DailyReport/v2/scheduler/)
- `data/mail.json`（邮件配置文件，首次启动下载，需填写信息）：[mail](https://api.holgerbest.top/DailyReport/v2/mail/)
- 版本号API：[https://api.holgerbest.top/DailyReport/v2/version/](https://api.holgerbest.top/DailyReport/v2/version/)
- 提示信息API：[https://api.holgerbest.top/msgbox.html?msg=在这里键入提示信息](https://api.holgerbest.top/msgbox.html?msg=在这里键入提示信息)
