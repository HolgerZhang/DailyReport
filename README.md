# DailyReport

Daily health report automated program. 每日打卡自动化程序

v1.21 by holger

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

从 main.py 运行，不要修改 mapping.json 文件。运行前先根据注释（`_notes`）配置 user.json 中的个人信息。

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

使用方法：

1. 单次执行

~~~python
import bot

打卡机器人 = bot.DailyReport()
if 打卡机器人.需要登录():
    打卡机器人.登录()
打卡机器人.打卡()
~~~

2. 定时执行（默认）

运行前先根据注释（`_notes`）配置 scheduler.json 中的定时信息（默认每天9：30）。

~~~python
import bot
import scheduler

def 作业():
    打卡机器人 = bot.DailyReport()
    if 打卡机器人.需要登录():
        打卡机器人.登录()
    打卡机器人.打卡()

if __name__ == '__main__':
    scheduler.调度(作业)
~~~

### 更新说明

- v1.0  第一代，实现基本功能。
- v1.1  具体页面中的属性使用json保存，与代码解耦，使后续升级和调整对代码的改动最小；使用json保存用户数据并添加注释；优化代码结构，减少代码冗余；增加输出执行过程，帮助用户运行出错时检查问题。
- v1.2  添加json配置文件的版本控制；添加定时任务功能（非阻塞的后台调度器，cron触发，执行作业），添加 scheduler.json 配置定时信息。
- v1.21 由于网站更新，更新mapping（务必升级）

### TODO List

- [ ] json配置文件热更新，且不影响原有配置。（ [更新api](https://api.holgerbest.top/DailyReport) ）
- [ ] 监听json文件变化，变化后自动更新bot。