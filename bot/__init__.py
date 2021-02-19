# coding = utf-8
"""
file: bot/__init__.py
author: holger
version: 3.0
license: AGPL-3.0
belongs: WebBot-Module
"""

from bot import default
from bot import error
from bot import util
from bot import version
from bot.core import WebBot
from bot.default import job_maker
from bot.default import run
from bot.default import run_once
from bot.task import TaskScheduler
