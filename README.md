# DailyReport

Daily health report automated program. 每日打卡自动化程序

v1.1 by holger

coding: UTF-8

有关实现细节详见[链接](https://holgerbest.top/2021/01/19/python-selenium/)

### 使用前注意

- Python先安装selenium3.x (pip install selenium)
- 之后下载Chrome驱动程序：[https://chromedriver.storage.googleapis.com/index.html?path=87.0.4280.88/](https://chromedriver.storage.googleapis.com/index.html?path=87.0.4280.88/)
- 手动创建一个存放浏览器驱动的目录，如：`C:\ChromeDriver` , 将下载的浏览器驱动文件（解压后）chromedriver丢到该目录下。
- 添加环境变量：此电脑–>属性–>系统设置–>高级–>环境变量–>系统变量–>Path，将 `C:\ChromeDriver` 目录添加到Path的值中。
- Linux/Unix/macOS: 直接将解压得到的驱动文件 chromedriver 拷贝到 `/usr/loacl/bin` 目录下即可。

### 使用

从 main.py 运行，不要修改 mapping.json 文件。运行前先根据注释（`_notes`）配置 user.json 中的个人信息。

> 可以配置系统计划任务、crontab等定时执行。

使用方法：

~~~python
import bot

打卡机器人 = bot.DailyReport()
if 打卡机器人.需要登录():
    打卡机器人.登录()
打卡机器人.打卡()
~~~

### 新版本变化

- v1.0  第一代，实现基本功能。
- v1.1  具体页面中的属性使用json保存，与代码解耦，使后续升级和调整对代码的改动最小；使用json保存用户数据并添加注释；优化代码结构，减少代码冗余；增加输出执行过程，帮助用户运行出错时检查问题。
