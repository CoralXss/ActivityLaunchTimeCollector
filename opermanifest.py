# encoding:utf-8
import os
import sys
sys.path.append(os.getcwd() + '/util')


import re
from lxml import etree
import fileutil
import cmdutil
import getconfigdata


# 功能：获取 xml 文件转成 XML 元素对象
def get_android_manifest_xml(manifest_file):
    content = fileutil.read_byte_file(manifest_file)
    # print(content)
    return etree.XML(content)  # 类型：<class 'lxml.etree._Element'>


# 功能：获取包名
def get_package_name(xml):
    manifest = xml.xpath('//manifest')
    package_name = manifest[0].attrib['package']
    return package_name


# 功能：获取声明的所有 activity 完整路径名
def get_activity_names(xml):
    activity_names = []

    # 获取模块包名
    module_package_name = get_package_name(xml)
    activity_elements = xml.xpath('//activity')
    # print('--act--', activity_elements)

    for element in activity_elements:
        # 3）获取 activity android:name 属性值
        name = element.attrib['{http://schemas.android.com/apk/res/android}name']
        # 4）给 activity name 声明加上完整包名
        if re.match(r'^\.', name):
            name = module_package_name + name
            element.set('{http://schemas.android.com/apk/res/android}name', name)
        # 5）收集 manifest.xml 中定义的所有 activity 名称
        activity_names.append(name)

    # # 打印收集的 activity 名称
    # for name in activity_names:
    #     print(name)
    return activity_names


# 功能：修改 manifest.xml 文件 - 给 activity 添加 exported="true" 属性
def modify_android_manifest_file(xml, new_manifest_file):
    activity_elements = xml.xpath('//activity')

    # 3）给每个 activity 插入/修改属性 android:exported="true"
    for element in activity_elements:
        # print(type(element))  # 元素类型：<class 'lxml.etree._Element'>
        # 该当前元素结点新增/修改一个属性
        element.set('{http://schemas.android.com/apk/res/android}exported', 'true')

    # 4）重新替换 或 写到新的 xml 文件中
    new_xml = etree.tostring(xml)
    fileutil.write_byte_content(new_xml, new_manifest_file)


# ------------------------todo 转成类------------------------------------

def operate_manifest(manifest_file_path):
    # 解析 manifest.xml 文件得到 xml 对象
    android_xml = get_android_manifest_xml(manifest_file_path)

    # 2）修改manifest.xml文件，可通过外部adb命令打开activity
    modify_android_manifest_file(android_xml, manifest_file_path)


def get_declared_activity(manifest_file_path):
    # 解析 manifest.xml 文件得到 xml 对象
    android_xml = get_android_manifest_xml(manifest_file_path)
    return get_activity_names(android_xml)


# 批量修改每个模块的 manifest 文件
def batch_modify_manifest():
    project_configs = getconfigdata.get_module_configs()
    for item in project_configs:
        operate_manifest(item['manifest_file'])


# 恢复到修改之前的版本
def restore_manifest():
    project_configs = getconfigdata.get_module_configs()
    for item in project_configs:
        # 直接切换到对应的目录
        os.chdir(item['project_dir'])
        cmdutil.execute_cmd('git checkout -- ' + item['manifest_file'])
    os.chdir(os.getcwd())


if __name__ == '__main__':
    # 批量修改 manifest.xml 文件
    # batch_modify_manifest()
    pass
