# coding: utf-8
# 输出文件详情，函数名称
#@author 查壹壹
#@category Cha111Ng1
#@keybinding 
#@menupath Tools.查壹壹的工具箱🧰.info
#@toolbar ./logo/默认.png
import sys
import os
import subprocess
import tempfile
import ghidra
from pwn import *
from prettytable import PrettyTable
from ghidra.app.script import GhidraScript

print(u"""
++++++++++++++++++++++++++++++++++++++++++
+  微信公众号：攻有道       By:Cha111Ng1    +
++++++++++++++++++++++++++++++++++++++++++
Github：https://github.com/Cha111Ng1/ghidra_scripts_cha11
""")

# 输出保护信息
def get_elf_object():
    # 创建表格对象
    table = PrettyTable()
    # 添加表头
    table.field_names = ["属性", "值"]
    # 获取当前程序绝对路径
    current_program = getCurrentProgram()
    file_location = current_program.getExecutablePath()
    user_home = os.path.expanduser("~")
    file_location_cha11 = file_location.replace(user_home,"~")
    print("[+]文件路径为：", file_location_cha11)
    print("[+]安全保护开启情况如下：")
    elf = ELF(file_location)
    table.add_row(["架构", elf.arch])
    table.add_row(["获取是否存在栈保护（Stack Canary）", elf.canary])
    table.add_row(["获取是否存在不可执行栈（NX）", elf.nx])
    table.add_row(["获取是否启用了位置无关执行（PIE）", elf.pie])
    # 打印表格
    print(table)


# 输出基本信息
def get_info():
    current_program = getCurrentProgram()
    program_name = current_program.getDomainFile().getName()
    creation_date = current_program.getDomainFile().getMetadata()
    language_id = current_program.getLanguageID().getIdAsString()
    compiler_spec_id = current_program.getCompilerSpec().getCompilerSpecID()

    print (u"[+]Program Info程序信息-> %s: %s_%s\n" % (program_name, language_id, compiler_spec_id))
    # print (u"[+]Program Info程序信息-> %s: %s_%s (%s)\n" % (program_name, language_id, compiler_spec_id, creation_date))


# Get the current program's function names获取当前程序的函数名
def get_wxhs():
    print (u"[+]function names程序函数名称：\n**危险函数备注：[\"strcpy\", \"strcat\", \"sprintf\", \"memcpy\", \"gets\", \"system\"]**")
    function = getFirstFunction()
    while function is not None:
        print (function.getName())
        function = getFunctionAfter(function)



def addBookmarkForKeyword(keyword):
    # 获取当前程序
    currentProgram = getCurrentProgram()
    
    # 获取当前程序的内存块
    memory = currentProgram.getMemory()
    
    # 获取当前地址空间
    addressSpace = currentProgram.getAddressFactory().getDefaultAddressSpace()

    # 获取二进制文件的最小和最大地址
    minAddress = addressSpace.getMinAddress()
    maxAddress = addressSpace.getMaxAddress()

    # 将关键字转换为字节数组
    keywordBytes = keyword.encode('utf-8')

    # 遍历地址范围，查找关键字
    currentAddress = minAddress
    while currentAddress < maxAddress:
        # 从当前地址处读取字节
        currentBytes = memory.getBytes(currentAddress, len(keywordBytes))
        
        if currentBytes == keywordBytes:
            # 添加书签到包含关键字的位置
            createBookmark(currentAddress, "Keyword Found: " + keyword, "Description")

        # 移动到下一个地址
        currentAddress = currentAddress.add(1)


# 命令选择
def comd():
    choices = ["输出保护信息", "输出基本信息", "输出函数名称", "将敏感字符添加书签"]
    selected_option = askChoices("info By：Cha111Ng1", "选择一个或多个功能:", choices)
    print("[+]选择的功能为：" + str(selected_option))
    # print(selected_option)
    return selected_option


# 在需要的地方调用 get_elf_object() 函数
try:
    selected_option = comd()
    if "输出保护信息" in selected_option:
        get_elf_object()
    if "输出基本信息" in selected_option:
        get_info()
    if "输出函数名称" in selected_option:
        get_wxhs()
    if "将敏感字符添加书签" in selected_option:
        # 调用函数以运行脚本并查找指定关键字
        addBookmarkForKeyword("/bin/sh")
except Exception as e:
    print("An error occurred:", e)