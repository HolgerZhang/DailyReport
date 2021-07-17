# DailyReport

Daily health report automated program. 每日打卡自动化程序

v2.1 by holger

coding: UTF-8

有关实现细节（v1.x）详见[链接](https://holgerbest.top/2021/01/19/python-selenium/)

> 感谢 [@ygLance](https://github.com/ygLance) 和 [@TTL2000](https://github.com/TTL2000) 的测试。

### 使用前注意

> v2.x 不再向下兼容 [v1.x](https://github.com/HolgerZhang/DailyReport/tree/main) 的部分配置文件以及启动方法
> 
> v2.1 前所有版本的支持周期均已停止，请尽快升级至 v2.1 版本

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

### 更新说明

- v1.0  第一代，实现基本功能。
- v1.1  具体页面中的属性使用json保存，与代码解耦，使后续升级和调整对代码的改动最小；使用json保存用户数据并添加注释；优化代码结构，减少代码冗余；增加输出执行过程，帮助用户运行出错时检查问题。
- v1.2  添加json配置文件的版本控制；添加定时任务功能（非阻塞的后台调度器，cron触发，执行作业），添加 scheduler.json 配置定时信息。
- v1.21 由于网站更新，更新mapping（务必升级）
- v1.3  新增json配置文件联网更新和软件版本检查（于每次打卡前检查；这一特性目前处于测试阶段，可以通过命令行添加 `--miss-feature` 参数来阻止每次打卡前的更新检查【v2.0版本已改为 `--no-update`】，但是首次运行时的更新检查不可取消），从这一版本起，不再在源码中附带配置json，首次运行时提示用户更新，**原有配置文件不受影响，无需删除**。
- v1.35 (stable end-of-life) 修复bug，新增接口。
- v1.4  (stable end-of-life) 新增定时检测json文件变化，变化后自动更新bot。
- v1.41 (long-term end-of-life) 修复文件监测时I/O过于频繁和输出日志过长的问题。如不需要实时监测配置文件变化功能只需手动修改 version.json 屏蔽升级提醒：`"VERSION": 1.4  ->  1.41`
- v2.0 (stable end-of-life) **全面重构**。将业务逻辑与代码分离，便于后续升级；支持为多人打卡，向 user 配置文件 information 中新增格式相同的 JSON 对象即可；全新日志模块，输出、异常信息一目了然；具备安装程序，一键安装依赖。
- v2.1 (long-term preview) 修复自带的 Chrome 驱动过于老旧的问题；修复一定概率的网页元素定位失败的问题；打卡结束时将结果停留展示 10 秒；添加输出调试信息选项。

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
- 我想要手动填写体温数据【不推荐】
  - 解决办法：打开 `data/mapping.json` ，定位到第 275 和 283 行，将 `random_float()` 分别改为用单引号包裹的上午体温和下午体温，注意保留前面的美元符号 `$` ，如 `"$'36.3'"`，如图：
    ![QAImg](https://i.loli.net/2021/02/11/zeBPacFSHqlQTjw.png)
    确保配置文件为最新，打开 run.py，注释第 28 行 `api.update()` 后，运行 run.py 并添加 `--once` 参数即可。
    不再希望手动填写体温数据，只需取消第 28 行 `api.update()` 的注释即可。
  - ~~说明：在 bot_core 解析 json 的能力得到增强后，将提供更为简洁的方法。~~

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