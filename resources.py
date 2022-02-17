# coding = utf-8
# author: holger version: 2.5
# license: AGPL-3.0
# belong: DailyReport-Predefined

CONFIG_NEED_UPDATE_F2 = "{}配置需要更新<br />请打开相应的json文件，按照_notes提示更新配置文件<br />" \
                        "若启动参数为 '--disable-monitor' 更新后需重启程序；若{}秒后没有修改则程序可能会异常退出。"
CONFIG_UP_TO_DATE = '配置已是最新'
ERR_WRONG_VER_F2 = "Error: 版本号有误，请手动下载{}替换，详见： {}"
PROGRAM_SETUP = '程序初始化'
RUN_F1 = "执行 {}"
SRC_NEED_UPDATE = "软件需要更新<br />请访问：https://github.com/HolgerZhang/DailyReport/releases/tag/v{} <br />更新后请重启程序。"
SRC_UP_TO_DATE = '程序版本已是最新'
START_INTRODUCTION = '<p><strong>程序初始化完成.</strong></p>' \
                     '<p>运行 python3 main.py 开始打卡</p>' \
                     '<p></p>' \
                     '<p> - 首次运行请预先配置 data 目录下 json 文件 </p>' \
                     '<p> - 具体用法请参考：https://github.com/HolgerZhang/DailyReport 或 README 文件</p>' \
                     '<p></p>' \
                     '<h1>免责声明</h1>' \
                     '<p> - 每日打卡自动化程序 DailyReport（下简称“此软件”）仅供自动化测试使用，' \
                     '使用时不应该带有扰乱正常秩序的目的，不得作为商业目的使用；</p>' \
                     '<p> - 此软件基于 AGPL-3.0 开源协议，引用此项目请保留开源协议并开放源代码，不得恶意修改（包括但不限于源代码、配置文件等）；</p>' \
                     '<p> - 此软件使用时需要保持开机并联网，且需保证网络通畅，能够访问目标网站。' \
                     '使用此软件时需留意日志文件信息以及自行查询是否打卡成功。' \
                     '由于网络问题、目标页面更新等导致的打卡失败、不能连续打卡等问题，此软件以及作者不承担任何责任；</p>' \
                     '<p> - 其余未尽事宜，此软件以及作者保留解释权利；</p>' \
                     '<p> - 使用此软件，默认接受以上声明；如不接受，请删除本软件。</p>'
# API V2.0
API_V2 = "https://api.holgerbest.top/DailyReport/v2/"
VERSION_API_V2 = "https://api.holgerbest.top/DailyReport/v2/version/"
