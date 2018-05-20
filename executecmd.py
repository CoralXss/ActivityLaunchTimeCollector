# encoding:utf-8
import json
import re
import threading
import os
import sys

sys.path.append(os.getcwd() + '/util')

from util import cmdutil


# 获取所有链接的设备
def get_devices():
    devices = []
    results = cmdutil.get_execute_cmd_result('adb devices')
    for item in results:
        m = re.match(r'(.*)device$', item)
        if m:
            devices.append(m.group(1).strip())
    return devices


# 功能：批量执行启动 activity 命令
def batch_execute_adb_start_cmd(app_package_name, activity_names, collect_file, device):
    print(threading.currentThread().name)
    output = open(collect_file, 'w')  #  + '_' + device
    cmd_prefix = 'adb -s ' + device + ' shell am start -W ' + app_package_name + '/'
    if app_package_name == '':
        cmd_prefix = 'adb -s ' + device + ' shell am start -W '
    for name in activity_names:
        cmd = cmd_prefix + name
        print(cmd)
        item_dict = cmdutil.execute_adb_start_cmd(cmd)
        # 转成 json串写入到文件中
        json_string = json.dumps(item_dict, ensure_ascii=False) + '\n'
        print('--------')
        print(json_string)
        output.write(json_string)
    output.close()


# 针对多设备批量执行am start 命令
def batch_execute_adb_start_cmd_for_devices(app_package_name, activity_names, collect_file):
    devices = get_devices()
    for device in devices:
        # 在线程中执行批量操作
        batch_execute_adb_start_cmd(app_package_name, activity_names, collect_file, device)
        # print(device)
    #     try:
    #         _thread.start_new_thread(batch_execute_adb_start_cmd,
    #                       (app_package_name, activity_names, collect_file, device, ))
    #     except:
    #         print('Error')
    #
    # # 如果主线程先于子线程结束，会出现Unhandled exception in thread started，所有需要让主线程休眠足够长
    # time.sleep(100)
