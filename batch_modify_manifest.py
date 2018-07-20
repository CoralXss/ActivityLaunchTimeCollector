# encoding:utf-8
import os
import sys

sys.path.append(os.getcwd() + '/util')
sys.path.append(os.getcwd() + '/opermanifest.py')

import opermanifest


# 说明：主要在 Android 主工程 中在 assembleDebug 之前运行
# 本地运行：python batch_modify_manifest.py true
if __name__ == '__main__':
    # 输入参数为 true 则表示修改清单文件，false 表示恢复
    modifyEnabled = sys.argv[1]

    tip = 'restore'
    if 'true' == modifyEnabled:
        tip = 'modify'
    print('----------begin to ' + tip + ' to activity----------')
    if 'true' == modifyEnabled:
        opermanifest.batch_modify_manifest()
    else:
        opermanifest.restore_manifest()
    print('----------' + tip + ' activity end-------------------')
