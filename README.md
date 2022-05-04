<!--
    coding = utf-8
    author: holger
    version: 4.0.0
    license: AGPL-3.0
    belong: DailyReport-BasicDataFile
-->

# DailyReport (Beta)

Daily health report automated program. 每日打卡自动化程序（适用于苏大）

v4.0.0(Beta) by HolgerZhang

with [SUMSC/email-sender](https://github.com/SUMSC/email-sender)

coding: UTF-8

> 有关实现细节详见[链接](https://holgerbest.top/2021/01/19/python-selenium/)

> 感谢 [@ygLance](https://github.com/ygLance) 和 [@TTL2000](https://github.com/TTL2000) 的测试。

### 内测招募

重构的v4版本需要进一步测试，现面向SUDA在校生招募内测体验人员～

我们希望你：

- 能够流畅访问GitHub！
- 电脑装有Python3.8+（如果熟悉Python更好！）
- 爱折腾，善于发现问题（因为是内测，bug出现频率和更新频次会比较高）

加入内测你可以获得：

- 高效的每日自动打卡体验；
- 更快的bug修复频率；
- 一对一的7*24h帮助服务；
- 或许可以成为本项目的contributor。

如果您感兴趣，欢迎联系我的QQ：**453744187**！

### 使用前注意

> v4 不再向下兼容 [v2](https://github.com/HolgerZhang/DailyReport/tree/v2) 的配置文件以及启动方法；
> 
> [v3](https://github.com/HolgerZhang/DailyReport/tree/v3) 分支已弃用；
> 
> v2.5 为 [v2](https://github.com/HolgerZhang/DailyReport/tree/v2) 分支最后一个大版本更新，将继续支持至 v4 分支结束测试。

- 环境依赖：带有 pip 的 Python 3 环境；安装有浏览器（应为最新版，支持情况请查阅 [文档](https://www.selenium.dev/downloads/) ）
- 支持系统：Windows | Linux | macOS
- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp) （该页面也会在打卡结束时停留10秒）

#### 免责声明

- 每日打卡自动化程序 DailyReport（下简称“此软件”）仅供自动化测试使用，使用时不应该带有扰乱正常秩序的目的，不得作为商业目的使用；
- 此软件只适用于自动化测试等有关技术等用途。<strong>如果你出现身体不适、身处疫情地区等等情况，请及时反映情况，不得瞒报！！</strong>
- 此软件基于 AGPL-3.0 开源协议，引用此项目请保留开源协议并开放源代码，不得恶意修改（包括但不限于源代码、配置文件等）；
- 此软件使用时需要保持开机并联网，且需保证网络通畅，能够访问目标网站。使用此软件时需留意日志文件信息以及自行 [查询](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp) 是否打卡成功。由于网络问题、目标页面更新等导致的打卡失败、不能连续打卡等问题，此软件以及作者不承担任何责任；
- 其余未尽事宜，此软件以及作者保留解释权利；
- 使用此软件，默认接受以上声明；如不接受，请删除本软件。

### 使用方法

1. 阅读《免责声明》，接受方可继续。
2. 运行 `python3 -m pip install -r requirements.txt'` 安装依赖，（需要升级pip版本到22.0.3）

   升级方法 `python3 -m pip install --upgrade pip`

3. 首次运行请预先根据 configurations/introduction.general.json 配置 configurations 目录下 general.json 文件 （可参考 example.general.json ）；
   根据 configurations/introduction.user.json 配置 configurations 目录下 user.用户名.json 文件；
4. 运行 `python3 main.py --initialize` 初始化并下载配置文件；
5. 运行 `python3 main.py` 开始使用； 

    后台运行方法：使用 nohup `nohup python3 main.py >> /dev/null 2>&1 &`；
    结束运行请自行kill：`ps -aux | grep 'python3 main.py'` 记录pid，`kill <pid>`

- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp)
- 添加参数 `-o` 或 `--once` 以单次运行程序
- 添加参数 `-l` 或 `--local` 以关闭自动检查更新特性，而是使用本地存在的文件
- 添加参数 `-c CONFIG` 或 `--config CONFIG` 使程序只为用户编号（从0开始）为 INDEX 的用户打卡（为负数则为所有人打卡）
- 添加参数 `-u USER` 或 `--user USER` 来在用户配置文件的目录生成 "user.${USER}.json" 文件
- 使用环境变量 `BOT_CORE_DEBUG=TRUE` 以在 bot 执行时输出调试信息，并添加必要断点
- 使用环境变量 `EMAIL_SENDER_SLEEP_MAX_INT` 来修改邮件发送的最大休眠间隙（默认10秒）

### 更新说明

#### v4.0.0 (Beta)

##### BUILD.A002-HLO0313

- 新版本重构，优化代码结构；
- 实现多人多线程打卡；
- 完善了版本号的计算；
- 移除文件变更检测特性，延迟至每次执行时读取系统配置及用户信息文件；
- 增加虚拟屏幕的支持，用以支持在无显示设备的服务器端运行（仅支持Linux）；
- 基本支持目前主流的浏览器，最大限度契合 selenium 的适配情况。

已知问题：

- **Chrome**的支持最完整【推荐使用】；其余浏览器未经测试；
- Safari浏览器只适用于Mac平台；Mac下使用Safari运行存在异常 selenium.common.exceptions.WebDriverException 。

##### BUILD.A002-HOL0320

- 修复并发链接数过大导致的邮件发送失败的问题；
- 优化日志输出，方便定位问题；

##### BUILD.A002-HOL0321

- 邮件中隐藏密码；
- 优化｜修复并发链接数过大导致的邮件发送失败的问题；
- 优化邮件内容。

##### BUILD.A003-HOL0325

- 修复邮件重发时不能正确发送的问题；
- 修复邮件文本替换时可能造成的异常。

##### BUILD.3910-2.5.4-alpha

- 修复邮件文本替换的多次转义；
- 成功发送时不再向发件人发送邮件；
- 开始提供编译的文件。

### Q&A

- 运行 setup 报错：找不到库 requests
  - 解决办法：预先手动安装 requests：`pip install requests`
- 运行失败后弹窗：捕获异常，log 文件显示异常信息为：NoSuchElementException
  - 解决办法：检查 user 信息是否有误
- 运行失败后弹窗：捕获未知异常；或捕获异常，log 文件显示异常信息不为 NoSuchElementException
  - 解决办法：联系作者[邮箱](mailto:holgerzhang@outlook.com) 
- 我想要立刻执行一次打卡
  - 解决办法：运行 main.py 添加 `--once` 参数
- 我想要手动填写体温数据【请手动打卡 :) 】

### API v4

- 根地址：[https://api.holgerbest.top/DailyReport/v4/](https://api.holgerbest.top/DailyReport/v4/)
- `data/mapping.json`（配置文件，首次启动下载）：[mapping](https://api.holgerbest.top/DailyReport/v4/mapping/)
- `user.用户名.json`（用户配置文件，使用 -u 选项下载）：[user](https://api.holgerbest.top/DailyReport/v4/user/)
- 版本号API：[https://api.holgerbest.top/DailyReport/v4/version/](https://api.holgerbest.top/DailyReport/v2/version/)
