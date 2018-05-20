# encoding:utf-8
import re
import os

# python 调用 shell 脚本的两种方式：
# os.system(cmd)
# os.popen(cmd)
# 区别：前者返回值仅为0(成功)，1，2；后者会将执行的 cmd 的输出作为返回值，所以如果需要手机返回值则使用第二种执行方式。


# 功能：执行一般shell命令
def execute_cmd(cmd):
    os.system(cmd)


# 功能：获取 cmd 命令执行后的结果列表
def get_execute_cmd_result(cmd):
    return os.popen(cmd).readlines()


# 功能：获取adb启动activity命令结果列表
def execute_adb_start_cmd(cmd):
    outputs = get_execute_cmd_result(cmd)
    items = {}
    for line in outputs:
        m = re.search(r'(.*)(: )(.*)', line.strip())
        if m:
            # print('---')
            # print(m.group(0))  # 完整输出
            # print(m.group(1))  # : 前面部分/key
            # print(m.group(2))  # :
            # print(m.group(3))  # : 后面部分/value
            items[m.group(1)] = m.group(3)

    return items


# 测试执行 cmd 命令
# CMD_ADB_START = 'adb shell am start -W ' \
#                 'me.ele.napospromotion/me.ele.napos.promotion.module.home.PromotionHomeTabActivity'
# execute_adb_start_cmd(CMD_ADB_START)



