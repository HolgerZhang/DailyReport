#!/usr/bin/python3
"""
file: run_workspace.py
coding: utf-8
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-External
"""
import os
import sys

usage_str = """USAGE:
run_workspace.py workspace-path [args...]
    - workspace-path should be the path to a standard workspace folder
    - 'a standard workspace' should contains:
        + main.py
        + data/configuration.xml
        + data/map.xml

Working principle: Add the folder where the module 'bot' is located into PYTHONPATH,
                   and run 'main.py' in workspace folder.
You can use like this to run the workspace in the Python integrated development 
  environment (IDE), such as PyCharm, VS Code, etc.
"""

if len(sys.argv) < 2:
    print('Error Usage')
    print(usage_str)
    exit(1)


def check_path(path, dir_=False):
    if dir_:
        if not os.path.isdir(path):
            print('NOT a standard workspace folder:', path)
            print(usage_str)
            exit(2)
    else:
        if not os.path.isfile(path):
            print('NOT a standard workspace folder:', path, 'not found')
            print(usage_str)
            exit(3)


bot_path = os.path.split(__import__('bot').__file__)[0].rstrip('bot')
workspace = sys.argv[1]
check_path(workspace, True)
data_path = os.path.join(workspace, 'data')
check_path(data_path, True)
check_path(os.path.join(workspace, 'main.py'))
check_path(os.path.join(data_path, 'configuration.xml'))
check_path(os.path.join(data_path, 'map.xml'))

os.chdir(workspace)
py_path = 'set PYTHONPATH=%PYTHONPATH%;' if sys.platform.lower().startswith('win32') \
    else 'export PYTHONPATH=$PYTHONPATH:' + bot_path
exec_stat = 'python' if sys.platform.lower().startswith('win32') else 'python3' + ' main.py'
for arg in sys.argv[2:]:
    exec_stat += ' ' + arg
os.system(py_path + ' && ' + exec_stat)
