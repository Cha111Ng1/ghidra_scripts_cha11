# coding: utf-8
# 使用IDA打开当前文件，自动选择63位和32位
#@author 查壹壹
#@category Cha111Ng1
#@keybinding 
#@menupath Tools.查壹壹的工具箱🧰.使用IDA打开当前文件
#@toolbar ./logo/ida.png

import subprocess
import configparser
import os


print(u"""
++++++++++++++++++++++++++++++++++++++++++
+  微信公众号：攻有道       By:Cha111Ng1    +
++++++++++++++++++++++++++++++++++++++++++
Github：https://github.com/Cha111Ng1/ghidra_scripts_cha11
""")


# 使用合适的IDA打开文件
def idastart(ida):
    # 获取当前程序绝对路径
    current_program = getCurrentProgram()
    file_location = current_program.getExecutablePath()
    command_to_execute = idahome + ida + " " + file_location
    print("[+]执行命令：" + command_to_execute)
    subprocess.Popen(command_to_execute, shell=True)
    return "[+]执行成功\n"

def idaserver_vps(vpsip,vpsport,vpsrootpath):
    # 定义要执行的命令
    current_program = getCurrentProgram()
    program_name = current_program.getDomainFile().getName()
    file_location = current_program.getExecutablePath()
    command_to_execute = "scp -P "+vpsport+" " + file_location + " root@"+vpsip+":"+vpsrootpath+" " + "&& ssh -t -p "+vpsport+" root@"+vpsip+" \'cd "+vpsrootpath+"&&chmod +x "+program_name+" && /root/tools/tool/gdbserver/linux_server64 ./"+program_name+";/bin/bash\'\n"
    print("[+]远程IDAserver地址："+vpsip+" 23946")
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

def file_x86():
    current_program = getCurrentProgram()
    language_id = current_program.getLanguageID().getIdAsString()
    print("[+]架构：" + language_id)
    if ":32:" in language_id:
        print("[+]执行32位IDA...")
        return "ida"
    elif ":64:" in language_id:
        print("[+]执行64位IDA...")
        return "ida64"
    else:
        print("[*]未识别多少位执行程序无法打开对应版本IDA")
        # return ""


def comd():
    choices = ["使用32/64位IDA打开当前二进制程序进行静态分析", "将当前二进制文件上传VPS使用IDA进行动态调试"]
    # 使用 askChoice 显示选项`askChoices("test","test",choices)`设置多选
    selected_option = askChoice("IDA插件 By：Cha111Ng1", "选择一个功能:", choices, "")
    print("[+]选择的功能为：" + selected_option)
    return selected_option




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
idahome = config.get('ida', 'idahome')

# 在需要的地方调用 get_elf_object() 函数
try:
    ida_cha11 = comd()
    # 使用IDA进行静态分析
    if ida_cha11 == "使用32/64位IDA打开当前二进制程序进行静态分析":
        idastart(file_x86())
    # 打开远程VPS调试
    elif ida_cha11 == "将当前二进制文件上传VPS使用IDA进行动态调试":
        idaserver_vps(vpsip,vpsport,vpsrootpath)
        ida = file_x86()
        command_to_execute = idahome + ida
        print("[+]执行命令：" + command_to_execute)
        subprocess.Popen(command_to_execute, shell=True)
except Exception as e:
    print("An error occurred:", e)