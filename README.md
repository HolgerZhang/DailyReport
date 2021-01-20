# DailyReport

Daily health report automated program. 每日打卡自动化程序

v1.3 by holger

coding: UTF-8

有关实现细节详见[链接](https://holgerbest.top/2021/01/19/python-selenium/)

> 感谢 [@ygLance](https://github.com/ygLance) 和 [@TTL2000](https://github.com/TTL2000) 的测试。

### 使用前注意

- python3 环境依赖：
  - selenium3.x (pip install selenium)
  - APScheduler (pip install apscheduler) 【v1.2新增依赖】
- 下载Chrome驱动程序：[https://chromedriver.storage.googleapis.com/index.html?path=87.0.4280.88/](https://chromedriver.storage.googleapis.com/index.html?path=87.0.4280.88/)
- 手动创建一个存放浏览器驱动的目录，如：`C:\ChromeDriver` , 将下载的浏览器驱动文件（解压后）chromedriver丢到该目录下。
- 添加环境变量：此电脑–>属性–>系统设置–>高级–>环境变量–>系统变量–>Path，将 `C:\ChromeDriver` 目录添加到Path的值中。
- Linux/Unix/macOS: 直接将解压得到的驱动文件 chromedriver 拷贝到 `/usr/loacl/bin` 目录下即可。

### 使用

从 main.py 运行。首次运行以及更新后会提示根据注释（`_notes`）配置 user.json 中的个人信息。

> Linux后台执行方法：`nohup python3 -u main.py >DailyReport.log 2>&1 &`
> 
> Windows后台执行方法（无黑框）：
> - 在项目根目录下新建bat文件，内容为： `python.exe main.py >DailyReport.log `
> - 在任意目录下新建vbs文件，内容为：
>   ~~~vbs
>   DIM objShell
>   set objShell=wscript.createObject("wscript.shell")
>   iReturn=objShell.Run("cmd.exe /C \path\to\bat_file.bat", 0, TRUE)
>   ~~~
> - 运行vbs文件即可。

使用方法：【**从v1.3开始，main.py中需要显式加载配置文件和检查更新（如示例代码）**】

1. 单次执行

~~~python
import bot
import api

api.检查更新()  # v1.3开始需要联网加载数据
bot.load()  # v1.3开始需要显式加载配置
打卡机器人 = bot.DailyReport()
if 打卡机器人.需要登录():
    打卡机器人.登录()
打卡机器人.打卡()
~~~

2. 定时执行（默认）

首次运行以及更新后会提示根据注释（`_notes`）配置 scheduler.json 中的定时信息。

~~~python
import bot
import api
import scheduler

def 更新():
    api.检查更新()  # v1.3开始需要联网加载数据
    bot.load()  # v1.3开始需要显式加载配置
    scheduler.load()

def 作业():
    更新()
    打卡机器人 = bot.DailyReport()
    if 打卡机器人.需要登录():
        打卡机器人.登录()
    打卡机器人.打卡()

if __name__ == '__main__':
    更新()
    scheduler.调度(作业)
~~~

### 更新说明

- v1.0  第一代，实现基本功能。
- v1.1  具体页面中的属性使用json保存，与代码解耦，使后续升级和调整对代码的改动最小；使用json保存用户数据并添加注释；优化代码结构，减少代码冗余；增加输出执行过程，帮助用户运行出错时检查问题。
- v1.2  添加json配置文件的版本控制；添加定时任务功能（非阻塞的后台调度器，cron触发，执行作业），添加 scheduler.json 配置定时信息。
- v1.21 由于网站更新，更新mapping（务必升级）
- v1.3  新增json配置文件联网更新和软件版本检查（于每次打卡前检查；这一特性目前处于测试阶段，可以通过命令行添加 `--miss-feature` 参数来阻止每次打卡前的更新检查，但是首次运行时的更新检查不可取消），从这一版本起，不再在源码中附带配置json，首次运行时提示用户更新，**原有配置文件不受影响，无需删除**。

### API

- 根地址：[https://api.holgerbest.top/DailyReport/](https://api.holgerbest.top/DailyReport/)
- `mapping.json`（元素选择配置）：[mapping.json](https://api.holgerbest.top/DailyReport/mapping.json)
- `user.json`（用户信息配置，首次使用需填写）：[user.json](https://api.holgerbest.top/DailyReport/user.json)
- `scheduler.json`（定时任务配置，首次使用需填写）：[scheduler.json](https://api.holgerbest.top/DailyReport/scheduler.json)
- 版本号API：[https://api.holgerbest.top/DailyReport/version/](https://api.holgerbest.top/DailyReport/version/)
- 提示信息API：[https://api.holgerbest.top/msgbox.html?msg=Text](https://api.holgerbest.top/msgbox.html?msg=Text)

**配置文件更新算法【Beta】** （`def __merge(old_data: dict, new_data: dict) -> (dict, bool)`）

> 该算法有待于完善的测试，且运行效率不高。

- 合并old_data，new_data两配置数据（dict类型）
- 配置数据的键类型为str，值类型为str、dict、list、float中的一种。
- 要求：old_data中所有的键值对都会保存，除非：
  - 对于new_data和old_data中共有的键：
    - 若值为dict类型，合并方法相同（即递归合并）；
    - 若值为float类型，不相等则覆盖old_data中对应数据；
    - 若值为str、list类型，则new_data中不为空且不相等的数据覆盖原数据。
  - 对于new_data中新增加的键，直接将键值对添加到合并结果。
- 要求不改变old_data，new_data两配置数据，而是生成一个新的dict作为第一个返回值。
- 如果发生了覆盖和新增，要求第二个返回值返回True，否则返回False。

### TODO List

- [x] json配置文件热更新。*v1.3版本实现*
- [ ] 监听json文件变化，变化后自动更新bot。