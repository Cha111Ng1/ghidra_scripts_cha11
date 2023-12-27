# coding: utf-8
# 将二进制文件，上传至远程服务器，开启调试、执行、创建题目
#@author 查壹壹
#@category Cha111Ng1
#@keybinding 
#@menupath Tools.查壹壹的工具箱🧰.上传二进制至VPS
#@toolbar ./logo/update_vps.png

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
    choices = ["连接远程服务器至工作目录", "将当前二进制文件上传至服务器「并打开shell」", "将当前二进制文件上传至服务器「并启动GDB调试」", "将当前二进制文件上传至服务器「并使用socat开启题目」"]
    # 使用 askChoice 显示选项`askChoices("test","test",choices)`设置多选
    selected_option = askChoice("远端调试插件 By：Cha111Ng1", "选择一个功能:", choices, "")
    print("[+]选择的功能为：" + selected_option)
    return selected_option

def updata_vps(comd,vpsip,vpsport,vpsrootpath):
    # 定义要执行的命令
    current_program = getCurrentProgram()
    program_name = current_program.getDomainFile().getName()
    file_location = current_program.getExecutablePath()
    if comd == "连接远程服务器至工作目录":
        command_to_execute = "ssh -t -p "+vpsport+" root@"+vpsip+" \'cd "+vpsrootpath+";/bin/bash\'\n"
    elif comd == "将当前二进制文件上传至服务器「并打开shell」":
        command_to_execute = "scp -P "+vpsport+" " + file_location + " root@"+vpsip+":"+vpsrootpath+" " + "&& ssh -t -p "+vpsport+" root@"+vpsip+" \'cd "+vpsrootpath+"&&chmod +x "+program_name+";/bin/bash\'\n"
    elif comd == "将当前二进制文件上传至服务器「并启动GDB调试」":
        command_to_execute = "scp -P "+vpsport+" " + file_location + " root@"+vpsip+":"+vpsrootpath+" " + "&& ssh -t -p "+vpsport+" root@"+vpsip+" \'cd "+vpsrootpath+"&&chmod +x "+program_name+"&&gdb "+program_name+";/bin/bash\'\n"
    elif comd == "将当前二进制文件上传至服务器「并使用socat开启题目」":
        command_to_execute = "scp -P "+vpsport+" " + file_location + " root@"+vpsip+":"+vpsrootpath+" " + "&& ssh -t -p "+vpsport+" root@"+vpsip+" \'cd "+vpsrootpath+"&&chmod +x "+program_name+"&&socat TCP-LISTEN:1337,reuseaddr,fork EXEC:./"+program_name+";/bin/bash\'\n"
        print("[+]远程题目地址：nc "+vpsip+" 1337")
        print("[+]exp.py：cha11 = remote('%s', '1337')"%vpsip)
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

# 获取用户主目录的完整路径
user_home = os.path.expanduser("~")
# 从配置文件读取值
config = configparser.ConfigParser()
configcha11 = '%s/.config/ghidra_scripts_cha11/config.ini'%user_home
config.read(configcha11,encoding='utf-8')

# 配置服务器修改值
vpsip = config.get('vps', 'vpsip')
vpsport = config.get('vps', 'vpsport')
vpsrootpath = config.get('vps', 'vpsrootpath')

try:
    print("[+]启动远端调试插件...")
    updata_vps(comd(),vpsip,vpsport,vpsrootpath)
except Exception as e:
    print("[x]请检查网络连接情况")
    print("An error occurred:", e)