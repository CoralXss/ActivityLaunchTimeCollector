# encoding:utf-8
# 如何引入第三方库？- 在红色波浪线处，alt+enter，进行install .
import getconfigdata
import opermanifest
import executecmd
import findinvalidstartpage
from util import fileutil

import sys
import os

sys.path.append(os.getcwd() + '/util')

'''
步骤：
方式一：相当于读取 xml 文件，可以使用 xpath 进行查找
1）读取 manifest.xml 文件内容；
2）读取包名，package="com.coral.aop"；
3）读取<activity 下 android:name="" 空格之间的内容 
   或者 读取所有的 android:name="" 得到引号之间的内容，然后按 Activity 删选;
4) 在<activity 下插入新属性：android:export="true" ；
5）将最终得到的 xml 内容重新写到 AndroidManifest.xml 文件中；
6）使用命令运行项目 并 安装 apk 到手机中（新的apk是添加了exported="true"属性的包）；
   - cd 到对应模块根目录；
   - 执行 gradle assembleDebug/Release;
   - 执行 adb install apk文件，安装到手机（这里必须受到 build successful 的通知才能执行安装）；
7）批量执行 adb shell am start -W packageName/ActivityName 启动 Activity；
   - 命令：adb shell am start -n 包名/包名＋类名
   - 这里必须知道 apk 安装成功才能批量执行统计命令；
   - 还需要知道当前应用是否处于前台；手机是否处于锁屏状态，不然命令执行一直处于堵塞状态。
   
   adb shell am start -W 命令返回参数说明：
   Starting - 表示启动的 Activity 意图；
   Activity - 表示执行这条命令成功后打开的页面（如果执行了命令，但是目标Activity一直没有打开，则代表打开的下一个Activity）
   
   参考：http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2016/0105/3830.html
   
8）手机 adb 执行命令得到的输出结果 并将统计结果写到一个文件中。


TODO-1：有的页面需要传值，如果拿不到上个页面的值，就会 crash 或者 直接 finish 掉，这样通过 adb am start 就无法统计页面启动时间。
解决：这里可以使用 lancet 插入的方式，执行登录，给需要传值的页面传值，
     如此，运行本命令，既可以收集 adb am start 的时间，也可以收集通过 lancet hook 方式获取的启动时间。
     
TODO-2：针对整个项目执行脚本，则需要对每个模块进行 读取&插入 exported="true" 属性，
   然后对整个项目执行 adb am start 命令进行统计，
   同时需要打开 lancet & 统计通过 AOP 形式得到的启动时间。    
     


小工具：写一个 python 脚本实现打包某个模块的 apk，然后安装到对应的手机。打包成功提示，打包成功后进行安装；安装成功后提示。

方式二：纯正则表达式查找、替换和插入
'''

'''
脚本的三种使用情形：
1）仅执行打包 & 安装到手机；
2）仅执行 启动页面 & 收集启动时间；
3）打包 -> 安装到手机 -> 启动页面 & 收集。

对于手机整个项目中的模块页面启动：
1）对每个模块，先修改对应的 manifest.xml 文件；（单独运行 python 脚本）
  - python execute.py 0
  - python execute.py 1
  
2）以项目形式依赖到主工程；
3）针对不同模块，批量执行启动 对应模块声明的 Activity & 得到文件数据。

python opermanifest.py



'''


def get_input_arg():
    # 输入参数结构：python argv[0] argv[1]，如 python execute.py 1
    build_index = 0
    if len(sys.argv) > 1:
        build_index = int(sys.argv[1])

    print(build_index)
    return build_index


# 第一次针对所有业务模块执行 am start 命令（仅执行一次）
def first_execute_cmd(**root_project):
    project_configs = getconfigdata.get_module_configs()
    activity_name_list = []

    for index in range(len(project_configs)):
        manifest_file_path = project_configs[index]['manifest_file']

        # 获取模块中完整activity名称
        complete_activity_names = opermanifest.get_declared_activity(manifest_file_path)
        # 获取主业务模块中的 activity 列表
        for item in complete_activity_names:
            activity_name_list.append(item)
    # 批量执行 am start 命令
    executecmd.batch_execute_adb_start_cmd_for_devices(root_project['package_name'], 
      activity_name_list, root_project['collect_file'])


NEED_FILTER_INVALID_ACTIVITY = False


# 运行程序
if __name__ == '__main__':

    root_project = getconfigdata.get_module_configs()[0]

    app_valid_act_file = root_project['valid_file']
    app_collect_file = root_project['collect_file']

    # todo 如何用全局变量控制？
    if not NEED_FILTER_INVALID_ACTIVITY:
      first_execute_cmd(**root_project)
    else:  
      # 筛选能正常启动的页面
      findinvalidstartpage.process_valid_page(**root_project)
    
      # 针对 invalid_file.txt 文件中收集的 activity 执行 am start 命令(可选)
      valid_activity_names = fileutil.read_file_by_line(app_valid_act_file)
      executecmd.batch_execute_adb_start_cmd_for_devices('', valid_activity_names, app_collect_file)
    








