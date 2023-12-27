# coding: utf-8
# BUUCTF刷题脚本
#@author 查壹壹
#@category Cha111Ng1
#@keybinding 
#@menupath Tools.查壹壹的工具箱🧰.BUUCTF下一题
#@toolbar ./logo/buuctf.png

import requests
import pyperclip
import json
import os
import webbrowser
import subprocess
import configparser
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 「info」初始化插件配置-获取seesion
def loginbuuctf():
    session = requests.Session()

    paramsGet = {"next":"https://buuoj.cn/"}
    paramsPost = {"name":user,"nonce":"710d973dc84f1ec7a5c6f94afe98a1594dc3c8cfe926f253d9df4af365451c9a","password":password}
    headers = {"Origin":"https://buuoj.cn","Sec-Ch-Ua":"\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"","Upgrade-Insecure-Requests":"1","Sec-Ch-Ua-Platform":"\"macOS\"","Sec-Fetch-Site":"same-origin","Sec-Fetch-Dest":"document","Sec-Fetch-User":"?1","Dnt":"1","Sec-Ch-Ua-Mobile":"?0","Sec-Fetch-Mode":"navigate","Content-Type":"application/x-www-form-urlencoded"}
    cookies = {"next":"https://buuoj.cn/","session":"15589683-83d2-4419-9609-b2a8c1fd5497.LYKidWpSY2aRbFEGbjtDRN7MHAI"}
    response = session.post("https://buuoj.cn/login", data=paramsPost, params=paramsGet, headers=headers, cookies=cookies, verify=False, allow_redirects=False)

    # 提取 Set-Cookie 头部信息
    set_cookie_headers = response.headers.get('Set-Cookie', '').split(',')
    session_value = None

    for cookie_header in set_cookie_headers:
        # 寻找包含 'session=' 的头部
        if 'session=' in cookie_header:
            # 使用分号拆分头部并找到包含 'session=' 的部分
            parts = cookie_header.split(';')
            for part in parts:
                if 'session=' in part:
                    # 提取 'session=' 后面的值
                    session_value = part.split('session=')[1].strip()
                    break

    print("[+]Session值获取成功: %s" % session_value)
    buucsrf_nonce = csrfbuuctf(session_value)
    return session_value, buucsrf_nonce

# 「info」初始化插件配置-获取csrf_noncez
def csrfbuuctf(buusession):
    session = requests.Session()

    headers = {"Sec-Ch-Ua":"\"Chromium\";v=\"118\", \"Google Chrome\";v=\"118\", \"Not=A?Brand\";v=\"99\"","Upgrade-Insecure-Requests":"1","Sec-Ch-Ua-Platform":"\"macOS\"","Sec-Fetch-Site":"same-origin","Sec-Fetch-Dest":"document","Sec-Fetch-User":"?1","Pragma":"no-cache","Dnt":"1","Sec-Ch-Ua-Mobile":"?0","Sec-Fetch-Mode":"navigate"}
    cookies = {"next":"/challenges?","session":buusession}
    response = session.get("https://buuoj.cn/challenges", headers=headers, cookies=cookies, verify=False)

    response_text = response.text

    # 使用正则表达式提取 csrf_nonce 的值
    csrf_nonce_match = re.search(r'var csrf_nonce = "(.*?)";', response_text)
    if csrf_nonce_match:
        csrf_nonce_value = csrf_nonce_match.group(1)
        print("[+]csrf_noncez值获取成功:", csrf_nonce_value)
        return csrf_nonce_value
    else:
        print("csrf_nonce not found in the response text")


# 「获取」BUUCTF新题的名字和ID
def getbuuctfid(cookies):
    response = session.get("https://buuoj.cn/api/v1/challenges.cache?category=Pwn&size=1&page=1&show=4&version=b4e165bd-6507-44ed-a2bd-03fba1073047", cookies=cookies)


    data = json.loads(response.text)
    id_value = data['data'][0]['id']
    name_value = data['data'][0]['name']

    # print(f'id: {id_value}, name: {name_value}')
    return id_value,name_value

# 查询获取的新题的二进制下载路径
def getbuuctffile(cookies,id_value):
    response = session.get("https://buuoj.cn/api/v1/challenges/%s"%id_value, cookies=cookies)

    data = json.loads(response.text)
    # 提取"files"字段对应的内容
    files_content = data['data']['files']
    return files_content[0]

# 「获取」BUUCTF新题，下载二进制题目至buuctf工作目录
def dowbuuctffile(cookies,buuctffile,name_value,root_path):
    response = session.get("https://buuoj.cn%s"%buuctffile,cookies=cookies)
    parts = buuctffile.rsplit('/', 1)
    if len(parts) == 2:
        last_part = parts[1]
    # 构建文件夹路径
    folder_path = root_path + name_value
    save_path = os.path.join(folder_path, last_part)
    # 创建文件夹（如果不存在）
    os.makedirs(folder_path, exist_ok=True)
    # 以二进制模式打开文件并保存响应内容
    with open(save_path, "wb") as file:
        file.write(response.content)
    # print("")
    return save_path

# 根据当前题目名称查询靶机题目ID
def namebuuctfid(cookies,name_value):
    response = session.get("https://buuoj.cn/api/v1/challenges.cache?page=1&size=1&q=%s&field=name&version="%name_value,cookies=cookies)
    data = json.loads(response.text)
    id_value = data['data'][0]['id']
    return id_value

# 「编写」WriteUp
def codewp(name_value):
    pyperclip.copy("""# BUUCTF %s
> 飞书链接：https://li2h5rwaaaa.feishu.cn/wiki/Jqyaw6kI5i8I5xkHd72c3Nk9nfe   密码：WwR]4r|7
> 自动化脚本项目地址：https://github.com/Cha111Ng1/ghidra_scripts_cha11
> 微信公众号：攻有道
> 题目地址：https://buuoj.cn/challenges#%s
> 题目名称：%s
## 保护信息

## 程序运行效果

## 关键函数
```C

```
> GPT说：
> 

### **思路：**

# exp.py
```Python

```
**成果：**

---
# 拓展资料
"""%(name_value,name_value,name_value))
    command_to_execute = "open -a '/Applications/Lark.app' 'https://li2h5rwaaaa.feishu.cn/wiki/DwLTwjFMtiSpihktdzPciOkxnph'"
    subprocess.Popen(command_to_execute, shell=True)

# 「开启」BUUCTF远程靶场
def startbuuctf(cookies,id_value,headers):
    response = session.post("https://buuoj.cn/plugins/ctfd-whale/challenge/%s/container"%id_value, headers=headers, cookies=cookies)
    # 解析JSON数据
    json_data = json.loads(response.text)
    # 提取"ip"和"port"字段对应的值
    success_value = json_data['success']
    if success_value == True:
        startbuuctfinfo(cookies,id_value,headers)
        
    else:
        print("Status code:   %i" % response.status_code)
        print("Response body: %s" % response.content)
        print("[x]靶场开启失败")

# 获取远程靶场开启状态
def startbuuctfinfo(cookies,id_value,headers):
    # headers = {"Csrf-Token":"9ff5091b21ac326dfc5bc756960cb282a184d85a0db47942e8bd0ae2a9829a7e"}
    response = session.get("https://buuoj.cn/plugins/ctfd-whale/challenge/%s/container"%id_value, headers=headers, cookies=cookies)
    try:
        # 解析JSON数据
        json_data = json.loads(response.text)
        # 提取"ip"和"port"字段对应的值
        ip_value = json_data['ip']
        port_value = json_data['port']
        print(f"[+]远程连接：nc {ip_value} {port_value}")
        cpcode = f"cha11 = remote('{ip_value}', '{port_value}')"
        pyperclip.copy(cpcode)
        print(f"[+]复制代码：{cpcode}")
        print("[+]靶场开启成功")
        return "[+]靶场开启成功"
    except Exception as e:
        print("Status code:   %i" % response.status_code)
        print("Response body: %s" % response.content)
        print("[*]当前状态为未开启，开启中...")
        return "[x]靶场开启失败"

# 「提交」flag至BUUCTF
def upflagbuuctf(cookies,id_value,flag,headers):
    rawBody = {"challenge_id":id_value,"submission":flag}
    response = session.post("https://buuoj.cn/api/v1/challenges/attempt", data=json.dumps(rawBody), headers=headers, cookies=cookies)

    print("Status code:   %i" % response.status_code)
    print("Response body: %s" % response.content)
    # 解析JSON数据
    json_data = json.loads(response.text)
    # 提取status字段
    status_value = json_data['data']['status']
    if status_value == "incorrect":
        print("[x]提交的flag错误")
    else:
        print("[+]你太牛了，又做对一题")

# 「关闭」BUUCTF远程靶场
def stopbuuctfinfo(cookies,id_value,headers):
    response = session.delete("https://buuoj.cn/plugins/ctfd-whale/challenge/%s/container"%id_value, headers=headers, cookies=cookies)
    json_data = json.loads(response.text)
    # 提取"ip"和"port"字段对应的值
    success_value = json_data['success']
    if success_value == True:
        print("[+]靶场关闭成功")
    else:
        print("[x]靶场关闭失败，状态如下")
        print("Status code:   %i" % response.status_code)
        print("Response body: %s" % response.content)

# Ghidra中获取当前程序绝对路径，从而获取题目名称
def findfilename():
        current_program = getCurrentProgram()
        file_location = current_program.getExecutablePath()
        parts = file_location.split("/")
        name_value = parts[-2]
        return name_value

# Ghidra弹出选择窗体
def comd():
    # return "「提交」flag至BUUCTF"
    choices = ["「info」初始化插件配置","「获取」BUUCTF新题", "「编写」WriteUp", "「开启」BUUCTF远程靶场", "「提交」flag至BUUCTF", "「关闭」BUUCTF远程靶场","「查询」该题目资料"]
    selected_option = askChoice("BUUCTF刷题神器 By：Cha111Ng1", "选择一个功能:", choices, "")
    print("[+]选择的功能为：" + selected_option)
    return selected_option
    



print(u"""
++++++++++++++++++++++++++++++++++++++++++
+  微信公众号：攻有道       By:Cha111Ng1    +
++++++++++++++++++++++++++++++++++++++++++
Github：https://github.com/Cha111Ng1/ghidra_scripts_cha11
""")


# 获取用户主目录的完整路径
user_home = os.path.expanduser("~")
# 从配置文件读取值
config = configparser.ConfigParser()
configcha11 = '%s/.config/ghidra_scripts_cha11/config.ini'%user_home
config.read(configcha11,encoding='utf-8')

# buuctf登录信息
# 获取 用户名密码 的值
user = config.get('buuctf', 'user')
password = config.get('buuctf', 'password')

# 获取buuctf登录配置项的值
buucsrf_nonce = config.get('buuctf', 'buucsrf_nonce')
buusession = config.get('buuctf', 'buusession')
# BUUCTF插件根目录配置信息
root_path = config.get('benji', 'root_path')

session = requests.Session()
# BUUCTF登录配置信息
headers = {"Accept":"application/json","Csrf-Token":buucsrf_nonce,"Content-Type":"application/json"}
cookies = {"session":buusession}



try:
    buuf = comd()
    ## 「info」初始化插件配置
    if buuf=="「info」初始化插件配置":
        buusession, buucsrf_nonce = loginbuuctf()
        # 修改配置项的值
        config.set('buuctf', 'buusession', buusession)
        config.set('buuctf', 'buucsrf_nonce', buucsrf_nonce)

        # 保存修改后的配置文件
        with open(configcha11, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

    ## 获取一道新的PWN题
    # 获取一道未解答的PWN题
    elif buuf == "「获取」BUUCTF新题":
        id_value,name_value = getbuuctfid(cookies)
        print(f'[+]题目ID为: {id_value}\n[+]题目名称为: {name_value}')
        # 获取PWN二进制文件下载地址
        buuctffile = getbuuctffile(cookies,id_value)
        # 下载PWN二进制文件到本地，还需要传入一个路径
        bdfile = dowbuuctffile(cookies,buuctffile,name_value,root_path)
        pyperclip.copy(bdfile)
        print("[+]下载完成保存路径为："+bdfile)

    ## 开启靶机,查询当前题目靶机启动id
    elif buuf=="「开启」BUUCTF远程靶场":
        
        name_value = findfilename()

        # name_value = "wn1_sctf_201"

        # 获取题目ID
        id_value = namebuuctfid(cookies,name_value)
        print("[*]当前二进制题目ID为：" + str(id_value))
        # 先获取靶场开启情况
        if startbuuctfinfo(cookies,id_value,headers) == "[x]靶场开启失败":
            # 查询未开启，进入「开启」BUUCTF远程靶场发包请求
            print(startbuuctf(cookies,id_value,headers))

    ## 「提交」flag至BUUCTF
    elif buuf=="「提交」flag至BUUCTF":
        name_value = findfilename()

        # name_value = "wn1_sctf_201"

        # flag = "flag\{1fdfd\}"
        flag = askString("「提交」flag至BUUCTF", "请输入你的flag")
        print("[+]输入的flag为：" + flag)
        id_value = namebuuctfid(cookies,name_value)
        upflagbuuctf(cookies,id_value,flag,headers)

    ## 「关闭」BUUCTF远程靶场
    elif buuf=="「关闭」BUUCTF远程靶场":
        name_value = findfilename()

        id_value = namebuuctfid(cookies,name_value)
        stopbuuctfinfo(cookies,id_value,headers)
        # print("[+]「关闭」BUUCTF远程靶场")

    ## 「查询」该题目资料
    elif buuf=="「查询」该题目资料":
        name_value = findfilename()

        url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=ubuntuu_cb&wd=ctf+%s"%name_value
        url2 = "https://search.bilibili.com/all?from_source=web_search&keyword=ctf+%s"%name_value
        webbrowser.open(url)
        webbrowser.open(url2)
        # print("[+]「关闭」BUUCTF远程靶场")
    ## 「编写」WriteUp
    elif buuf=="「编写」WriteUp":
        name_value = findfilename()
        codewp(name_value)

except Exception as e:
    print("An error occurred:", e)