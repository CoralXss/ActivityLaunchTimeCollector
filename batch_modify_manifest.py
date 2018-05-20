# encoding:utf-8
import os
import sys

sys.path.append(os.getcwd() + '/util')
sys.path.append(os.getcwd() + '/opermanifest.py')

import opermanifest


# 说明：主要在 Android 主工程 中在 assembleDebug 之前运行
if __name__ == '__main__':
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
