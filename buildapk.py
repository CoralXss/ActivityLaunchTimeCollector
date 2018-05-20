from util import cmdutil
from util import dateutil
import os

'''
    小工具：
    1. 写一个 python 脚本实现打包某个模块的 apk，然后安装到对应的手机。打包成功提示，打包成功后进行安装；安装成功后提示。
    2. 用脚本操作 抓包步骤：获取PC IP地址；设置当前手机连接 wifi 代理。
    3. 
'''


# variant Debug包 Release包
def execute_build_apk(is_release):
    print('-------build task begin-------')
    start_time = dateutil.get_current_time()
    # 执行打包命令
    cmd = 'gradle assembleDebug'
    if is_release:
        cmd = 'gradle assembleRelease'
    build_results = cmdutil.get_execute_cmd_result(cmd)
    # print(build_results)
    end_time = dateutil.get_current_time()
    print('-------build task end-------')
    for data in build_results:
        if 'BUILD SUCCESSFUL' in data:
            print('EXEC BUILD SUCCESSFUL, TIME = %s' % dateutil.get_time_span_string(end_time, start_time))
            return True
        elif 'FAILED' in data or 'FAILURE' in data:
            print('EXEC BUILD FAILURE, TIME = %s' % dateutil.get_time_span_string(end_time, start_time))
            return False


def execute_install_apk(project_dir, package_name, is_release):
    print('-------install task begin-------')
    start_time = dateutil.get_current_time()
    apk_file = project_dir + '/app/build/outputs/apk/app-debug.apk'
    if is_release:
        # todo 通过 assembleRelease 若没有配置签名文件，得到的安装包是 app-release-unsigned
        apk_file = project_dir + '/app/build/outputs/apk/app-release-unsigned.apk'

    # 安装之前检测有多少设备，若存在多台则提示并且程序不继续往下执行
    device_results = cmdutil.get_execute_cmd_result('adb devices')
    # 按行读取一台设备，list中会有三条数据
    print('len =', len(device_results))
    if len(device_results) > 3:
        print('Multi devices! Please keep one device online.')
        # raise ValueError('Multi devices! Please keep one device online.')

    install_results = cmdutil.get_execute_cmd_result('adb install ' + apk_file)
    print('----')
    print(install_results)
    # 如果安装失败，命令返回值为空字串或者空列表
    if len(install_results) == 0:
        # 先卸载然后重新安装
        print('Has installed apk. Then uninstall the pre one and install new .')
        cmdutil.execute_cmd('adb uninstall ' + package_name)
        cmdutil.get_execute_cmd_result('adb install ' + apk_file)
    end_time = dateutil.get_current_time()
    print('-------build task end-------')
    print('EXEC INSTALL TASK, TIME = %s' % dateutil.get_time_span_string(end_time, start_time))


def execute_build_assemble_task(project_dir, package_name, is_release, origin_dir):
    # # 以下 cd 命令执行成功后又立刻返回到当前的工作目录
    cmdutil.execute_cmd('cd ' + project_dir)
    # 直接切换到对应的目录
    os.chdir(project_dir)

    if execute_build_apk(is_release):
        execute_install_apk(project_dir, package_name, is_release)
    else:
        raise ValueError('Build task failed, install task is stopped ! Please try again later.')

    # 切换到之前的目录
    os.chdir(origin_dir)


def start_build_and_install_task(project_model, origin_path):
    execute_build_assemble_task(project_model['project_dir'], project_model['package_name'],
                                project_model['is_release'], origin_path)


# if __name__ == '__main__':

#     # build_path = sys.argv[1]  # /Users/xss/me_ele/NaposPromotion
#
#     device_results = cmdutil.get_execute_cmd_result('adb devices')

    # start_build_and_install_task()

