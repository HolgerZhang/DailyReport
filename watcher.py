# coding = utf-8
# author: holger
# version: 4.0.0
# license: AGPL-3.0
# belong: DailyReport-Watcher
import argparse
import os
import sys
import time
import traceback
from sys import exit

import psutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from BotCore import logger
from BotCore.version import VERSION, INSIDER_VERSION

parser = argparse.ArgumentParser(description="Daily health report Watcher. 每日打卡自动化程序监控程序",
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-v", "--version", action="version",
                    version='Daily health report Watcher. 每日打卡自动化程序监控程序\n'
                            'v{}.{}.{} (BUILD.{ins})\n'
                            '  By @HolgerZhang.\n'
                            '  GitHub: https://github.com/HolgerZhang/DailyReport/v4/\n'.format(*VERSION,
                                                                                                ins=INSIDER_VERSION))
parser.add_argument('-c', '--config', type=str, default="configurations/general.json",
                    help="path to the general configuration file, default is 'configurations/general.json'")
parser.add_argument('-e', '--exe', type=str,
                    default=r".\DailyReport.exe" if sys.platform.startswith('win32') else "./DailyReport",
                    help="path to the executable file, default is './DailyReport' in the current directory")
args = parser.parse_args()

config_file = os.path.abspath(args.config)
watch_path, _ = os.path.split(config_file)
pwd, exec_file = os.path.split(os.path.abspath(args.exe))
os.chdir(pwd)
logger.info(f"使用配置文件：{config_file}")
logger.info(f"监控目录：{watch_path}")
logger.info(f"工作目录：{pwd}")


def kill_all():
    for pid in psutil.pids():
        proc = psutil.Process(pid)
        if proc.name() == 'DailyReport' or proc.name() == 'DailyReport.exe':
            logger.info(f'{proc.name()}(pid={pid}) Killed')
            proc.kill()


def startup():
    cmd = f'./{exec_file} -c {config_file}'
    if sys.platform.startswith('win32'):
        os.system(f'powershell -c "Start-Process -WindowStyle hidden -FilePath \"{cmd}\""')
    else:
        os.system(f'nohup {cmd} > /dev/null 2>&1 &')
    logger.info('DailyReport Started')


def check():
    time.sleep(1)
    count = 0
    for pid in psutil.pids():
        proc = psutil.Process(pid)
        if proc.name() == 'DailyReport' or proc.name() == 'DailyReport.exe':
            logger.info(f'{proc.name()}(pid={pid}) Found')
            count += 1
            if count > 1:
                proc.kill()
    return count != 0


class FileEventHandler(FileSystemEventHandler):
    def on_moved(self, event):
        global config_file
        if os.path.abspath(event.src_path) != config_file:
            return
        logger.info(f"{config_file}文件移动 -> {event.dest_path}，重载DailyReport")
        logger.warn("移动文件存在风险！文件离开监控目录时自动重载会失效且无法恢复！")
        config_file = os.path.abspath(event.dest_path)
        kill_all()
        startup()
        if not check():
            logger.error("Error: DailyReport未能成功载入")
            exit(1)

    def on_deleted(self, event):
        global config_file
        if os.path.abspath(event.src_path) != config_file:
            return
        logger.error(f"Error: {event.src_path}文件被删除")
        kill_all()
        exit(1)

    def on_modified(self, event):
        global config_file
        if os.path.abspath(event.src_path) != config_file:
            return
        logger.info(f"{config_file}文件编辑，重载DailyReport")
        kill_all()
        startup()
        if not check():
            logger.error("Error: DailyReport未能成功载入")
            exit(1)


def main():
    kill_all()
    logger.info(f"即将载入DailyReport...")
    startup()
    if not check():
        logger.error("Error: DailyReport未能成功载入")
        exit(1)
    observer = Observer()  # 创建观察者对象
    file_handler = FileEventHandler()  # 创建事件处理对象
    observer.schedule(file_handler, watch_path, False)  # 向观察者对象绑定事件和目录
    observer.start()  # 启动
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        kill_all()
        logger.info('Bye <3')
    observer.join()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.debug("Unexpected Exception: " + traceback.format_exc())
        exit(2)
