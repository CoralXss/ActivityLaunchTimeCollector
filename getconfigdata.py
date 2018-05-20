# encoding:utf-8
import os
import sys
# 不通包路径下库的引入方式
sys.path.append(os.getcwd() + '/util')
import fileutil  # 这里添加了系统路径可以不用from
import re
import json
import os


# 读取项目配置文件列表
def get_module_configs():
    return fileutil.read_json_file('./file/moduleconfig.json')


def get_collect_json_data_by_index(index):
    project_configs = get_module_configs()
    return get_collect_json_data(project_configs[index]['collect_file'])


# 获取收集到的 js对象数据 列表
def get_collect_json_data(collect_file):
    new_datas = []
    try:
        # 存储时是写json字符串到文件中，所以在构造列表时需要重新转化为 dict，不然得前端自己转换
        datas = fileutil.read_file_by_line(collect_file)
        # for data, i in enumerate(datas):
        for data in datas:
            # 将字符串反序列化为 js 对象
            new_datas.append(json.loads(data))

        return new_datas
    except FileNotFoundError as e:
        print('catch error:', e)
    raise ValueError('Unfortunately, catch error !')


# 有些页面缺少上个页面传递的参数，会在 onCreate 直接 finish，所以无法收集数据，视为 invalid
def get_collect_page_valid(datas):
    new_datas = []
    for data in datas:
        # 如果启动出错，则不执行
        if 'Error' in data or 'timeout' in data:
            continue

        # 启动的 Activity 意图
        starting = data['Starting']
        # 将字符串反序列化为 js 对象

        act = data['Activity']
        m = re.search(r'(.*cmp=)(.*)( }$)', starting)
        if m:
            data['Component'] = m.group(2).split('/')[1]
            if m.group(2) == act:
                data['Valid'] = True
                new_datas.append(data)
            else:
                data['Valid'] = False
            # 去掉前面的包名
            data['Activity'] = act.split('/')[1]

    return new_datas


# ---------------------------------------------


# 获取配置
def get_module_config_by_type(build_index):
    # 当前文件根目录
    root_dir = os.getcwd()
    # 0）读取本地项目配置文件
    project_configs = get_module_configs()  # 返回 <class 'list'>
    # print(project_configs, type(project_configs))
    config_len = len(project_configs)

    if build_index >= config_len:
        raise ValueError('Out of index bounds of project config list . '
                         'Please keep the arg two less than %d' % config_len)

    # todo 将 json 字符串转成 ProjectModel 对象，从外部接收传入的 index，进行打包成功后安装
    project_model = project_configs[build_index]  # 得到 <class 'dict'>
    manifest_file_path = project_model['manifest_file']
    app_package_name = project_model['package_name']
    collect_file = project_model['collect_file']
    # 是否需要收集启动时间，若不需要则直接打包并安装apk
    need_collect = project_model['need_collect']
    # 分开 构建安装 和 收集 两种操作
    need_build = project_model['need_build']

    return app_package_name, collect_file, manifest_file_path, need_build, need_collect, project_model, root_dir
