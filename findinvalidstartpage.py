from util import fileutil, cmdutil
import getconfigdata
import re
import json


# FoodHomeActivity 通过 adb shell am start -W 无法启动并统计数据问题

def process_valid_page_by_index(index):
    project_configs = getconfigdata.get_module_configs()
    process_valid_page(**project_configs[index])


def process_valid_page(**kwargs):
    valid_file = kwargs['valid_file']
    invalid_file = kwargs['invalid_file']
    collect_file = kwargs['collect_file']

    # 收集之后才能执行筛选操作
    datas = fileutil.read_file_by_line(collect_file)
    new_datas = []
    for data in datas:
        # 将字符串反序列化为 js 对象
        new_datas.append(json.loads(data))

    invalid_items = []
    valid_items = []
    for data in new_datas:
        starting = data['Starting']
        act = data['Activity']
        # print('start = ' + starting + ', act = ' + act)

        m = re.search(r'(.*cmp=)(.*)( }$)', starting)
        if m:
            # print('---')
            # print(m.group(0))  # 完整输出
            # print(m.group(1))  # : 前面部分/key
            # print(m.group(2))  # :
            # print(m.group(3))  # : 后面部分/value

            if m.group(2) == act:
                valid_items.append(m.group(2))   # 去掉包名 .split('/')[1])
            else:
                invalid_items.append(m.group(2))

    print('---------VALID-----------------')
    output = open(valid_file, 'w')
    for item in valid_items:
        # json_string = json.dumps(item, ensure_ascii=False) + '\n'
        output.write(item + '\n')
        print(item)
    output.close()

    print('---------INVALID-----------------')
    output = open(invalid_file, 'w')
    for item in invalid_items:
        # json_string = json.dumps(item, ensure_ascii=False) + '\n'
        output.write(item + '\n')
        print(item)
    output.close()


# 启动不合理的 Activity（无法统计是因为启动时 缺少参数 闪退 或者没有参数直接 finish 了页面导致无法统计）
