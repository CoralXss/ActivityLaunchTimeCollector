# ActivityLaunchTimeCollector
This is a python script for Android Activity launch time . 

一、功能说明（仅适用于本地启动时间统计，如果要收集线上各个用户收集启动时间，可通过 AOP 实现）

统计项目/模块中所有的Activity，批量执行命令 adb shell am start -W packageName/ActivityName 启动并获取输出数据写到文件中。

未完成功能：将文件中收集到的数据以表格形式展示 & 标识每个字段的名称 & 计算每个页面启动时长 & 分析启动时长，得出本地启动页面的简单性能报告。
具体实现：使用 python 实现 web 服务器 & vue.js 前端展示收集到的数据。

使用的第三方python库：lxml（修改xml文件），flask（python后台）

其他技术要求：1）Python Web服务器搭建； 2）vue.js前端展示。


二、技术点说明

1. 使用adb命令打开一个项目中所有的Activity，必须对每个Activity配置 exported="true" 属性，否则是不允许外部直接访问 Activity 的。
（这里很想知道 Appium 是怎样实现 拿到页面上的某个点击的 view ？同样式通过 xpath 查找，对于现在高系统的真机，已经是没有权限去获取点击事件了。）

2. 执行 adb start 命令得A到的时间字段含义说明：
   - ThisTime 表示一连串启动 Activity 的最后一个 Activity 的启动耗时；
   - WaitTime 返回 Activity 到应用第一帧完全展示的这段时间，也即是总耗时，包括前一个应用 Activity pause 的时间和新应用启动的时间；
   - TotalTime 表示新应用启动的耗时，包括 新进程的启动 和 Activity 的启动，但不包括前一个应用 Activity pause 的耗时。

   图示标识如下：
   Activity1               Activity2                   Activity2
   onPause(T1)             startActivity(T2)           onWindowFocused(T3)

   字段计算：
   ThisTime  = T3 - T2
   TotalTime = T3 - T2
   WaitTime  = T3 - T1

   结论：1）一次只启动一个 Activity 时，ThisTime 和 TotalTime 是一样的；
        2）WaitTime 是一直大于 TotalTime 的，因为 WaitTime 包含了上一个 Activity 执行 onPause 的时间；
        3）由此可得知，开发者只需要关心 TotalTime 即可，这段时间是页面真正的启动耗时。


三、技术网站

xpath - http://www.w3school.com.cn/xpath/index.asp

xpath 原理：使用路径表达式选取 XML 文档中的节点或者节点集。


四、文件目录说明

1. 脚本收集相关：
/file/moduleconfig.json  -- 配置文件（配置整个工程中模块的路径名-主要用于批量修改 manifest 文件 & 获取每个模块中的 Activity）
/getconfigdata.py  -- 读取配置文件

/util
   /cmdutil.py  -- 执行命令工具脚本
   /dateutil.py -- 日期相关
   /fileutil.py -- 文件读写操作

/batch_modify_manifest.py -- 批量修改项目模块 manifest 文件
/opermanifest.py -- 读取、修改 manifest 工具脚本

/executecmd.py   -- 批量执行 am start -W 工具脚本   
/findvalidstartpage.py  -- 获取能正常启动的 Activity 脚本（执行一次批量 am start 后才可执行该脚本，主要用于过滤）
/executeall.py   -- 程序主入口，1）修改manifset文件（若在gradle中实现则此步可省略）；2）批量执行am start命令

2. 后台服务器实现：
/getcollectdata.py  -- flask 实现


五、执行步骤

1）单独执行 python batch_modify_manifest.py true 批量修改 moduleconfig.json中配置的工程模块中的 AndroidManifest.xml 文件，
主要是插入 android:exported="true" 属性（这一步可以写一个 gradle task 实现）；
2）运行 & 安装 apk；
3）执行 executeall.py 对获取到的所有 Activity 执行 am start -W 命令，最终的收集到的命令执行结果数据会写到 配置的 collect_file 文件中。


六、说明
1. 若项目仅存在一个 app 主模块，则直接配置工程路径到配置文件中即可；
2. 若项目分模块，模块与模块以 library 形式存在，则将各模块以及主模块路径配置到文件中；若子模块以 AAR 形式依赖则无法通过脚本修改 manifest 文件，只能忽略该模块中的 Activity 。
