# coding = utf-8
# author: holger
# version: 4.0.0
# license: AGPL-3.0
# belong: DailyReport-Main
import argparse
import json
import traceback

from easydict import EasyDict

import daemon
from BotCore import logger, version
from BotCore.file import get_driver
from BotCore.version import VERSION
from mail import Mail

parser = argparse.ArgumentParser(description="Daily health report automated program. 每日打卡自动化程序",
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-v", "--version", action="version",
                    version='Daily health report automated program. 每日打卡自动化程序\n'
                            'v{}.{}.{}  By @HolgerZhang, thanks @ygLance, @TTL2000.\n'
                            '    Together with SUMSC/email-sender v0.1.2\n'
                            'GitHub: https://github.com/HolgerZhang/DailyReport/v4/\n'.format(*VERSION))
parser.add_argument('-i', '--initialize', action='store_true',
                    help="initialize program")
parser.add_argument('-o', '--once', action='store_true',
                    help="run only once")
parser.add_argument('-l', '--local', action='store_true',
                    help="enable 'local run'(turn off automatic update), default disabled(automatic update)")
parser.add_argument('-c', '--config', type=str, default="configurations/general.json",
                    help="path to the general configuration file, default is 'configurations/general.json'")
parser.add_argument('-u', '--user', type=str,
                    help="create an user configuration named `user.${USER}.json` in 'configurations/'")
args = parser.parse_args()

with open(args.config, 'r', encoding='utf-8') as _file:
    config = EasyDict(json.loads(_file.read()))
    assert version.check_version(version.GENERAL_MIN_VERSION, config['VERSION']), '版本号不匹配'

mail = Mail(config.mail)


def init():
    logger.info("程序初始化")
    daemon.update()
    get_driver(config.webdriver.browser, config.webdriver.driver_path)
    logger.info("程序初始化完成.")


@daemon.virtual_display(turn_on=config.virtual_display)
@daemon.schedule(hour=config.scheduler.hour, minute=config.scheduler.minute, enable=not args.once)
def main():
    daemon.wakeup(user_config_path=config.user_config_folder,
                  users=config.user_list,
                  bot_config=config.webdriver,
                  mail=mail,
                  update_=args.local)


if __name__ == '__main__':
    logger.debug('执行配置："{}"\n'.format(args.config) + json.dumps(config, indent=2, ensure_ascii=False))
    try:
        if args.user is not None:
            daemon.new_user(config.user_config_folder, args.user)
        elif args.initialize:
            init()
        else:
            main()
    except Exception as e:
        mail.fail_mail(to=[], stu_id='ALL',
                       detail={'<strong>未知错误</strong>': Mail.html('{} - {}'.format(e.__class__, e)),
                               'Stack': Mail.html(traceback.format_exc())})
        logger.error('主线程异常 {} {}'.format(e.__class__, e.args), exc_info=True)
