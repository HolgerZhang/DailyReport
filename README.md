# DailyReport (preview)

Daily health report automated program. 每日打卡自动化程序

<strong>开发计划暂停，本分支缺少稳定性测试可能存在 BUG ，请移步 v2.1 版本</strong>
  
v3.0 (preview) by holger

coding: UTF-8

基于 WebBot（尚未完全开源）构建，该版本为 WebBot 的演示项目，在预定义工作区 Workspaces/DailyReport 实现 v2.x 以及 v1.41 的大部分功能。

了解有关 WebBot 的更多使用方法，参见根目录下的 usage.txt，make_workspace.py，run_workspace.py

有关实现细节（v1.x）详见[链接](https://holgerbest.top/2021/01/19/python-selenium/)

> 感谢 [@ygLance](https://github.com/ygLance) 和 [@TTL2000](https://github.com/TTL2000) 的测试。

### 使用前注意

> v3.x 不再向下兼容 [v2.x](https://github.com/HolgerZhang/DailyReport/tree/v2) 以及更低版本的配置文件，但 [v1.41](https://github.com/HolgerZhang/DailyReport/releases/tag/v1.41) 、 [v2.0](https://github.com/HolgerZhang/DailyReport/releases/tag/v2.0) 为长期支持版本，依旧提供更新

- 环境依赖：带有 pip 的 Python3 环境；系统装有 [Chrome 浏览器](https://www.google.cn/intl/zh-CN/chrome/)
- 支持系统：Windows x64 | Linux x64 | macOS(理论上支持但未经测试，不包括M1版本)
- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp)

#### 免责声明

- 每日打卡自动化程序 DailyReport（下简称“此软件”）仅供自动化测试使用，使用时不应该带有扰乱正常秩序的目的，不得作为商业目的使用；
- 此软件基于 AGPL-3.0 开源协议，引用此项目请保留开源协议，不得恶意修改（包括但不限于源代码、配置文件等）；
- 此软件使用时需要保持开机并联网，且需保证网络通畅，能够访问目标网站。使用此软件时需留意日志文件信息以及自行 [查询](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp) 是否打卡成功。由于网络问题、目标页面更新等导致的打卡失败、不能连续打卡等问题，此软件以及作者不承担任何责任；
- 其余未尽事宜，此软件以及作者保留解释权利；
- 使用此软件，默认接受以上声明；如不接受，请删除本软件。

### 使用

1. 阅读《免责声明》，接受方可继续。
2. 运行 `dependency_install.py` 下载并安装依赖；
3. 配置 `Workspaces/DailyReport/data/configuration.xml` 文件中的信息；
4. 运行 `run_workspace.py Workspaces/DailyReport` 开始使用。

- 每日请自行检查是否打卡成功： [检查连接](http://dk.suda.edu.cn/default/work/suda/jkxxtb/dkjl.jsp)
- 添加参数 `--once` 以单次运行程序

> 来自 v1.x 版本的Tip： Windows 后台执行方法（无黑框）
> - 在项目根目录下新建bat文件，内容为： `python.exe run.py`
> - 在任意目录下新建vbs文件，内容为：
>   ~~~vbs
>   DIM objShell
>   set objShell=wscript.createObject("wscript.shell")
>   iReturn=objShell.Run("cmd.exe /C \path\to\bat_file.bat", 0, TRUE)
>   ~~~
> - 运行vbs文件即可。

### 更新说明

- v1.0  第一代，实现基本功能。
- v1.1  具体页面中的属性使用json保存，与代码解耦，使后续升级和调整对代码的改动最小；使用json保存用户数据并添加注释；优化代码结构，减少代码冗余；增加输出执行过程，帮助用户运行出错时检查问题。
- v1.2  添加json配置文件的版本控制；添加定时任务功能（非阻塞的后台调度器，cron触发，执行作业），添加 scheduler.json 配置定时信息。
- v1.21 由于网站更新，更新mapping（务必升级）
- v1.3  新增json配置文件联网更新和软件版本检查（于每次打卡前检查；这一特性目前处于测试阶段，可以通过命令行添加 `--miss-feature` 参数来阻止每次打卡前的更新检查【v2.0版本已改为 `--no-update`】，但是首次运行时的更新检查不可取消），从这一版本起，不再在源码中附带配置json，首次运行时提示用户更新，**原有配置文件不受影响，无需删除**。
- v1.35 (stable) 修复bug，新增接口。
- v1.4  (stable) 新增定时检测json文件变化，变化后自动更新bot。
- v1.41 (long-term) 修复文件监测时I/O过于频繁和输出日志过长的问题。如不需要实时监测配置文件变化功能只需手动修改 version.json 屏蔽升级提醒：`"VERSION": 1.4  ->  1.41`
- v2.0 (stable) **全面重构**。将业务逻辑与代码分离，便于后续升级；支持为多人打卡，向 user 配置文件 information 中新增格式相同的 JSON 对象即可；全新日志模块，输出、异常信息一目了然；具备安装程序，一键安装依赖。
- v3.0 (preview) WebBot 全面升级，该版本为 WebBot 的演示项目，在预定义工作区 Workspaces/DailyReport 实现 v2.0 以及 v1.41 的大部分功能。

> v3.0 版本是基于 v2.0 升级的，对于 v2.0 存在的 bug 依旧存在。
> 
> 由于 v3 分支开发暂缓，bug 无法得到及时修复，请使用 v2 分支的最新版本作为日常使用环境。
> 
> 已知 BUGs：Windows 系统下命令行参数可能会解析为 Python 解释器的参数；与 v2.0 相同的 bug。


### 从 v1.x/v2.x 升级

不建议与 v1.x/v2.x 项目合并，而应该作为一个新的项目使用。

- 配置全面升级，详见 Workspace/DailyReport/data 各文件

### Q&A

- 运行失败后弹窗：捕获异常，log 文件显示异常信息为：NoSuchElementException
  - 解决办法：检查配置信息是否有误
- 运行失败后弹窗：Bot 内部错误；或捕获异常，log 文件显示异常信息不为 NoSuchElementException
  - 解决办法：请带上提示异常时的日志文件（5分钟以内的部分）联系作者，注意在日志中抹去敏感信息（如学号、密码、家庭住址等）
- 我想要立刻执行一次打卡
  - 解决办法：运行 main.py 添加 `--once` 参数
- 我想要手动填写体温数据
  - 解决办法：打开 `data/map.xml` ，定位到 MapList->Mapping(name="report")->FunctionsList->Function(name="FillBlank" return="void" exception="log") 前两行 
    
    ~~~
    `'%.1f' % (35.5 + 0.1 * __import__('random').randint(1, 10))`
    ~~~
    
    修改为 `"体温数值"` 即可，如 `"36.2"`。
    不再希望手动填写体温数据只需改回上面的代码。

### API v3.0

- `data/map.xml`（配置文件，每次启动下载）：[map.xml](https://api.holgerbest.top/DailyReport/v3/map.xml)
- `data/configuration.xml`（用户配置文件，程序自带，如果丢失需要自行下载，需填写信息）：[configuration.xml](https://api.holgerbest.top/DailyReport/v3/configuration.xml)
- 提示信息API：[https://api.holgerbest.top/msgbox.html?msg=在这里键入提示信息](https://api.holgerbest.top/msgbox.html?msg=在这里键入提示信息)

### TODO List

- [ ] 添加 GUI
- [x] 将 bot_core 分离为独立项目

### WebBot 使用简介

#### 安装依赖

运行 `dependency_install.py` 下载并安装依赖。

#### 创建工作区

运行 `make_workspace.py 工作区文件夹` 创建新的工作区。

~~~
USAGE: 
make_workspace.py path mode=(classic | auto | empty | once)
    - mode 默认类型: classic
    - e.g.  make_workspace.py Workspaces/Demo1 mode=auto
    - e.g.  make_workspace.py Workspaces/Demo2
~~~

#### 配置数据

在新建的工作区文件夹中 data 目录下配置 map.xml 和 configuration.xml。

map.xml 为基础配置，配置方法：（详见 introduction/map_introduction.xml ）

映射定义格式（在 MapList 中）：

~~~
<Mapping name="唯一的映射名称">
    <Url>目标网址</Url>
    <ElementsList>
        元素列表
    </ElementsList>
    <FunctionsList>
        函数列表
    </FunctionsList>
    <Action>
        调用函数流程
        格式：按顺序排列调用流程，中间以空格或制表符分割，包含在<![CDATA[ ]]>中。
            <![CDATA[FunctionName1 FunctionName2 FunctionName3 ...]]>
    </Action>
</Mapping>
~~~

元素定义格式：（ElementsList 中）

~~~
<Element name="元素名称" check="true | false">
    <target></target>
    <value></value>
    <text></text>
</Element>
~~~

说明：

- name 为唯一的元素名称，用于查找该元素；check 标识是否运行时检查实际显示与text是否相同；
- target：查找方法，id | class | name
- value：要查找的值
- text：预期显示内容

函数定义格式：（FunctionsList 中）

~~~
<Function name="函数名称" return="str | void" exception="escape | log | throw"><![CDATA[
    流程控制语句
]]></Function>
~~~

说明：

- name 为唯一的函数名称，用于定位函数；
- return 为返回值类型：str 类型会返回一个字符串，void 类型无返回值（实际返回 None）；
- exception 为异常捕获声明，仅针对 NoSuchElementException，escape 不捕获；log 视为警告，仅记录不中断运行，throw 视为错误，弹窗提示并中断运行。
- 流程控制语句需包含在`<![CDATA[ ]]>`中。

流程控制语句语法：

1. 一行视作为一条语句，每条语句以预定义关键词开始；单条语句不可换行，多条语句不可合并为一行；
   每条语句有一至多个组成部分（详见以下说明），各部分用一个或多个空格或制表符分割；语句大小写敏感；
   10个预定义关键词为：
   CLICK FILL FIND-XPATH SEARCH SAVE-TEXT USE STRING-RETURN STRING-RETURN-CLEAR SLEEP AS
   ;预定义关键词全为大写；除 AS 外，每条语句必以其余9个关键词中的一个开始。
2. 字符串常量 "text" （用一对双引号 "" 包裹），解释器会在预编译阶段调用 Python 解释器（eval 函数）将其转换为
   Python 的字符串对象，若不为 str 类型则抛出异常；注意：解释器未检查 eval 安全性问题，请甄别 "" 内实际内容。
3. 
   ~~~
   可执行 Python 语句 `python_exec_stat()` （用一对反单引号 `` 包裹），解释器会在预编译阶段调用 Python 解释器
   （eval 函数）得到运行结果并转换为字符串；注意：解释器未检查 eval 安全性问题，请甄别 `` 内实际执行内容。
   ~~~
   
4. 符号定义 $symbol （以美元符号 $ 开始，仅包含字母数字和下划线，且 $ 后不为数字），用于保存字符串以及查找到的元素；
   AS 后为符号的定义，其余为符号的使用；符号有字符串类型和元素类型两种类型；
   符号有两种作用生存期类型，一种是静态符号，在预编译阶段由字符串常量和可执行 Python 语句自动生成，均为字符串类型符号，
   保存于函数对象中，生存期直至运行结束，命名规则：前缀为 $_static_0x，后接静态符号的十六进制编号；
   另一种是动态符号，由用户在语句中创建，在函数执行过程中生成，字符串类型符号的生存期为定义位置开始直至函数结尾，
   元素类型符号的生存期为定义位置开始直至首次使用的语句结束。
   未定义和生存期结束的符号被使用解释器会抛出异常，动态符号多次定义会覆盖之前的类型和内容。
   若动态符号与静态符号重名，则静态符号会覆盖动态符号的可见性（即定义符号时不应以 $_static_0x 为前缀）。
   元素名称、用户属性名称、秒数无需其他标识，但要注意避开以上的标志字符。
5. 
   ~~~
   [need] 为字符串 "text"、符号 $symbol、可执行 Python 语句 `python_exec_stat()` 的一种；加 s 表示可以有多个。
   ~~~
   
6. 双斜杠 // 后面为注释。
7. 执行过程：源码载入（将源代码载入 Mapping 对象并去除注释） -> 预编译阶段（数据准备，常量创建，可执行 Python 语句转换） -> 解释阶段（逐条解释执行）
8. 各语句使用方法说明：

~~~
FIND-XPATH "xpath-statement" AS $symbol   // 查找并定义元素类型符号 $symbol
// 无法写死在 ElementsList 中的元素可以使用 XPATH 动态查找（使用一次就失效，再次使用需重新定位）
SEARCH [need] AS $symbol      // 使用 [need] 模糊查找元素并保存到元素类型符号 $symbol
CLICK 元素名称                 // 点击指定元素，元素名称可以为符号 $symbol（元素类型）
FILL 元素名称 [need]           // 使用 [need] 填充指定元素（文本框），元素名称可以为符号 $symbol（元素类型）
SAVE-TEXT 元素名称 AS $symbol  // 使用指定元素中 HTML 文本定义字符串类型符号 $symbol
USE 用户属性名称 AS $symbol     // 使用用户配置中指定的属性定义字符串类型符号 $symbol
STRING-RETURN [need]s         // 当 return="str" 时合并各个字符串并附加到本函数调用返回值，但不会结束函数运行；
                              // 其中符号需为字符串类型，而不是元素类型；
                              // 当 return="void" 时不允许使用该语句。
STRING-RETURN-CLEAR           // 当 return="str" 时清空本函数调用返回值，但不会结束函数运行；
                              // 当 return="void" 时不允许使用该语句。
SLEEP 秒数（整数）              // 线程休眠（在执行过程中） 注意 使用 `__import__('time').sleep(秒数)`
                              // 无法达到真正休眠的目的，因为可执行 Python 语句的执行是在预编译阶段进行的,
                              // 这样做只会导致程序在预编译期休眠并产生错误
~~~

#### 开始使用

运行 `run_workspace.py 工作区文件夹` 开始使用。

~~~
run_workspace.py workspace-path [参数...]
    - workspace-path 应该为标准工作区文件夹
    - '标准工作区文件夹' 应该包含:
        + main.py
        + data/configuration.xml
        + data/map.xml

工作原理: 将 'bot' 所在文件夹添加到 PYTHONPATH, 在工作区文件夹运行 'main.py'
  您可以这样在 Python 集成开发环境（IDE）中运行工作区，例如 PyCharm、VS Code 等
~~~
