# coding = utf-8
# author: holger version: 1.4
# license: AGPL-3.0

# use `--miss-feature` to disable file monitor feature and file auto update feature

import sys
import main

if '--miss-feature' in sys.argv:
    import scheduler as monitor
else:
    import monitor

if __name__ == '__main__':
    main.更新()
    monitor.调度(main.作业)
