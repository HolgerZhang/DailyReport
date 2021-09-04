# DailyReport (stable)

Daily health report automated program. 每日打卡自动化程序

v2.2 by holger

coding: UTF-8

有关实现细节详见[链接](https://holgerbest.top/2021/01/19/python-selenium/)

> 感谢 [@ygLance](https://github.com/ygLance) 和 [@TTL2000](https://github.com/TTL2000) 的测试。

### 使用前注意

> v2.x 不再向下兼容 [v1.x](https://github.com/HolgerZhang/DailyReport/tree/v1-end-of-life) 的部分配置文件以及启动方法
> 
> v2.1 及以前所有版本的支持周期均已停止，请尽快升级至 v2.2 版本

- 环境依赖：带有 pip 的 Python3 环境；系统装有 **最新版** [Chrome 浏览器](https://www.google.cn/intl/zh-CN/chrome/)
- 支持系统：Windows x64 | Linux x64 | macOS(理论上支持但未经测试，不包括M1版本)
- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp) （该页面也会在打卡结束时停留10秒）

#### 免责声明

- 每日打卡自动化程序 DailyReport（下简称“此软件”）仅供自动化测试使用，使用时不应该带有扰乱正常秩序的目的，不得作为商业目的使用；
- 此软件基于 AGPL-3.0 开源协议，引用此项目请保留开源协议，不得恶意修改（包括但不限于源代码、配置文件等）；
- 此软件使用时需要保持开机并联网，且需保证网络通畅，能够访问目标网站。使用此软件时需留意日志文件信息以及自行 [查询](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp) 是否打卡成功。由于网络问题、目标页面更新等导致的打卡失败、不能连续打卡等问题，此软件以及作者不承担任何责任；
- 其余未尽事宜，此软件以及作者保留解释权利；
- 使用此软件，默认接受以上声明；如不接受，请删除本软件。

### 使用

1. 阅读《免责声明》，接受方可继续。
1. 运行 `python3 setup.py` 下载并安装依赖
2. 运行 `python3 run.py` 开始使用；运行 `python3 run.pyw` 以不显示CMD窗口 (仅在 Windows 系统有效)

- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp)
- 添加参数 `--no-update` 关闭自动检查更新特性
- 添加参数 `--no-monitor` 关闭文件变更自动加载特性
- 添加参数 `--once` 以单次运行程序
- （调试用）添加参数 `--DEBUG` 以在 bot 执行时输出调试信息

> Tip： Windows 后台执行方法（无黑框）
> - 在项目根目录下新建bat文件，内容为： `python.exe run.py`
> - 在任意目录下新建vbs文件，内容为：
>   ~~~vbs
>   DIM objShell
>   set objShell=wscript.createObject("wscript.shell")
>   iReturn=objShell.Run("cmd.exe /C \path\to\bat_file.bat", 0, TRUE)
>   ~~~
> - 运行vbs文件即可。
> 
> 或者直接运行 `run.pyw` 文件。
> 
> Linux 系统后台运行方法：使用 nohup `nohup python3 run.py >> /dev/null 2>&1 &`
> 结束运行请自行kill：`ps -aux | grep 'python3 run.py'` 记录pid，`kill <pid>`

### 更新说明

- v2.0 (stable end-of-life) **全面重构**。将业务逻辑与代码分离，便于后续升级；支持为多人打卡，向 user 配置文件 information 中新增格式相同的 JSON 对象即可；全新日志模块，输出、异常信息一目了然；具备安装程序，一键安装依赖。
- v2.1 (fatal-error end-of-life) 修复自带的 Chrome 驱动过于老旧的问题；修复一定概率的网页元素定位失败的问题；打卡结束时将结果停留展示 10 秒；添加输出调试信息选项。【存在严重BUG：有一定概率定位元素发生偏移，导致打卡地点不受控制，强烈建议升级】
- v2.2 (bug fix, further testing required) 修复 2.1 版本的 BUG；执行出错自动重复5次，防止网络问题导致的打卡失败；优化系统稳定性。【有待进一步测试】可能存在 mapping 文件的问题，建议删除原有 data/mapping.json 文件重新下载（下载链接： [mapping](https://api.holgerbest.top/DailyReport/v2/mapping/) ），并删除 .cmp_dat 文件夹。此问题将于下一稳定版测试并解决。

### 从 v1.x 升级

不建议与 v1.x 项目合并，而应该作为一个新的项目使用。

- scheduler 配置不受影响，可直接替换；
- user 配置建议仅保留information中的个人信息，替换到新版本 user 配置文件的相应位置。

### Q&A

- 运行 setup 报错：找不到库 requests
  - 解决办法：预先手动安装 requests：`pip install requests`
- 运 行setup 后弹窗提示：请安装或更新Chrome
  - 解决办法：请保证电脑中安装了最新版本的Chrome浏览器
- 运行失败后弹窗：捕获异常，log 文件显示异常信息为：NoSuchElementException
  - 解决办法：检查 user 信息是否有误
- 运行失败后弹窗：捕获未知异常；或捕获异常，log 文件显示异常信息不为 NoSuchElementException
  - 解决办法：请删除日志文件后运行 run.py 添加 `--DEBUG` 参数复现该错误，并将日志文件和程序输出发送至作者[邮箱](mailto:holgerzhang@outlook.com) ，注意在日志中抹去敏感信息（如学号、密码、家庭住址等）
- 我想要立刻执行一次打卡
  - 解决办法：运行 run.py 添加 `--once` 参数
- 我想要手动填写体温数据【功能不再提供支持，请手动打卡】

### API v2

- 根地址：[https://api.holgerbest.top/DailyReport/v2/](https://api.holgerbest.top/DailyReport/v2/)
- `data/mapping.json`（配置文件，首次启动下载）：[mapping](https://api.holgerbest.top/DailyReport/v2/mapping/)
- `data/user.json`（用户信息配置文件，首次启动下载，需填写信息）：[user](https://api.holgerbest.top/DailyReport/v2/user/)
- `data/scheduler.json`（定时任务配置文件，首次启动下载，需填写信息）：[scheduler](https://api.holgerbest.top/DailyReport/v2/scheduler/)
- 版本号API：[https://api.holgerbest.top/DailyReport/v2/version/](https://api.holgerbest.top/DailyReport/v2/version/)
- 提示信息API：[https://api.holgerbest.top/msgbox.html?msg=在这里键入提示信息](https://api.holgerbest.top/msgbox.html?msg=在这里键入提示信息)

### TODO List

- [ ] ~~添加 GUI~~【暂无计划】
- [ ] 将 bot_core 分离为独立项目【v3分支进行中】
