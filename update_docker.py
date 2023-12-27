# coding: utf-8
# 进入本地Docker分析二进制文件，开启调试、执行、创建题目
#@author 查壹壹
#@category Cha111Ng1
#@keybinding 
#@menupath Tools.查壹壹的工具箱🧰.进入本地Docker分析二进制文件
#@toolbar ./logo/update_docker.png

import subprocess
import configparser
import os

print(u"""
++++++++++++++++++++++++++++++++++++++++++
+  微信公众号：攻有道       By:Cha111Ng1    +
++++++++++++++++++++++++++++++++++++++++++
Github：https://github.com/Cha111Ng1/ghidra_scripts_cha11
""")

def comd():
    # choices = ["连接本机Docker工作目录", "进入本机Docker工作目录「并启动GDB调试」", "进入本机Docker工作目录「并使用socat开启题目」"]
    choices = ["连接本机Docker工作目录", "进入本机Docker工作目录「并运行二进制程序」", "进入本机Docker工作目录「并启动GDB调试」", "进入本机Docker工作目录「并使用socat开启题目」"]
    # 使用 askChoice 显示选项`askChoices("test","test",choices)`设置多选
    selected_option = askChoice("远端调试插件 By：Cha111Ng1", "选择一个功能:", choices, "")
    print("[+]选择的功能为：" + selected_option)
    return selected_option

def updata_docker(comd,dockerid):
    # 定义要执行的命令
    current_program = getCurrentProgram()
    program_name = current_program.getDomainFile().getName()
    file_location = current_program.getExecutablePath()
    docker_file = file_location.replace(dockerlj, "/home/pwntools/")
    # 匹配最后一个program_name
    last_match_index = docker_file.rfind(program_name)
    # 替换program_name为空
    docker_mkdir = docker_file[:last_match_index] + "" + docker_file[last_match_index + len(program_name):]
    # docker_mkdir = docker_file.replace(program_name, "",1)
    if comd == "连接本机Docker工作目录":
        command_to_execute = "docker exec -it "+dockerid+" bash -c 'cd "+docker_mkdir+"&&bash'"
    elif comd == "进入本机Docker工作目录「并运行二进制程序」":
        command_to_execute = "docker exec -it "+dockerid+" bash -c 'chmod +x "+docker_file+"&&"+docker_file+"&&cd "+docker_mkdir+"&&bash'"
    elif comd == "进入本机Docker工作目录「并启动GDB调试」":
        command_to_execute = "docker exec -it "+dockerid+" bash -c 'chmod +x "+docker_file+"&&gdb "+docker_file+"'"
    elif comd == "进入本机Docker工作目录「并使用socat开启题目」":
        command_to_execute = "docker exec -it "+dockerid+" bash -c 'chmod +x "+docker_file+"&&socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"+docker_file+"'"
        print("[+]Docker题目地址：nc 127.0.0.1 1337")
        print("[+]exp.py：cha11 = remote('127.0.0.1', '1337')")
    print("[+]执行的命令为：" + command_to_execute)
    # 创建一个包含AppleScript命令的字符串
    applescript = f"""
    tell application "Terminal"
        activate
        do script "{command_to_execute}"
    end tell
    """
    # 执行AppleScript以创建新终端窗口并执行命令
    subprocess.call(['osascript', '-e', applescript])
    print("[+]执行完毕\n")

## docker配置信息
# 获取用户主目录的完整路径
user_home = os.path.expanduser("~")
# 从配置文件读取值
config = configparser.ConfigParser()
configcha11 = '%s/.config/ghidra_scripts_cha11/config.ini'%user_home
config.read(configcha11,encoding='utf-8')

# 获取docker的id
dockerid = config.get('docker', 'dockerid')
dockerlj = config.get('docker', 'dockerlj')

try:
    print("[+]启动本地Docker调试插件...")
    updata_docker(comd(),dockerid)
except Exception as e:
    print("[x]请检查本地Docker启用情况")
    print("An error occurred:", e)