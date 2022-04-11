# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup

user = {"no": "2019xxx", "password": "xxx"}  # 学号  # 密码

data = {
    "myvs_1": "否",  # 1是否有发热 是/否
    "myvs_2": "否",  # 2是否有咳嗽  是/否
    "myvs_3": "否",  # 3是否有乏力症状  是/否
    "myvs_4": "否",  # 4是否有鼻塞  是/否
    "myvs_5": "否",  # 5是否被确诊  是/否
    "myvs_6": "否",  # 6是否是疑似  是/否
    "myvs_7": "否",  # 7是否是密切接触者  是/否
    "myvs_8": "否",  # 8是否在医疗机构隔离  是/否
    "myvs_9": "否",  # 9是否在集中点隔离   是/否
    "myvs_10": "否",  # 10是否在居家隔离  是/否
    "myvs_11": "否",  # 11小区/村是否有确诊  是/否
    "myvs_12": "否",  # 12是否有共同具状人确诊  是/否
    "myvs_13a": "41",  # 13a 所在省的身份证区划代码(前两位)如河南省=41
    "myvs_13b": "4101",  # 13b所在省的身份证区划代码(前四位)如河南郑州=4101
    "myvs_13c": "河南省郑州市高新区科学大道100号",  # 13c具体所在地
    "myvs_24": "否",  # 是否为当日返郑人员
    "myvs_25": "5",  # 应该是和疫苗有关，5是三针
    # 以下内容无需更改
    "did": "2",
    "door": "",
    "day6": "b",
    "men6": "a",
    "sheng6": "",
    "shi6": "",
    "fun18": "819",
    "fun3": "",
    "jingdu": "113.535807",  # 主校区经度
    "weidu": "34.81732",  # 主校区纬度
    "ptopid": "",
    "sid": "",
}
# 以下内容无需改动
user_agent = "Mozilla/5.0 (Linux; U; Android 2.3.6; zh-cn; GT-S5660 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1 MicroMessenger/4.5.255"
host = "jksb.v.zzu.edu.cn"
origin = "https://jksb.v.zzu.edu.cn"
session = requests.session()
info = {}


# 登录函数
def login(account, password):
    header = {
        "Origin": origin,
        "Referer": "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0",
        "User-Agent": user_agent,
        "Host": host,
    }
    post_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login"
    post_data = {
        "uid": account,
        "upw": password,
        "smbtn": "进入健康状况上报平台",
        "hh28": "722",
    }
    response = session.post(post_url, data=post_data, headers=header)
    response.encoding = "utf-8"
    return response.text


# 选择填报人和填报类型
def enter(html):
    url = get_url(html)
    response = session.get(url)
    response.encoding = "utf-8"
    new_html = response.text
    post_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb"
    refer = url + "&fun2="
    header = {
        "Origin": origin,
        "Referer": refer,
        "User-Agent": user_agent,
        "Host": host,
    }
    post_data = get_session_data(new_html)
    # print(info)
    response = session.post(post_url, data=post_data, headers=header)
    response.encoding = "utf-8"
    return response.text


# 获取选择填报人和填报类型界面的超链接
def get_url(html):
    p = re.compile(r'parent.window.location="(.*?)"')
    s = str(p.findall(html)[0]).replace("first6", "jksb")
    return s


# 获取登录的session信息
def get_session_data(html):
    keys = ["did", "door", "men6", "ptopid", "sid"]
    values = []
    soup = BeautifulSoup(html, "html.parser")
    for key in keys:
        values.append(soup.find("input", {"name": key})["value"])
    global info
    info = dict(zip(keys, values))
    return info


# 填写上报表格
def submit(data):
    url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb"
    headers = {
        "User-Agent": user_agent,
        "Host": host,
        "Origin": origin,
        "Referer": "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb",
    }
    data["ptopid"] = info.get("ptopid")
    data["sid"] = info.get("sid")
    r = requests.post(url, headers=headers, data=data)
    r.encoding = "utf-8"
    str = r.text
    if str.find("感谢你今日上报健康状况") == -1:
        print(str)
        print("填报失败")
    else:
        print(return_message(str))
        print("填报成功！")


def return_message(s):
    p = re.compile(r">　　(.*?)同学")
    return p.findall(s).pop()


# 三个主要功能函数聚集
def jksb(user: dict, data: dict):
    html = login(user.get("no"), user.get("password"))
    enter(html)
    submit(data)


# main方法
if __name__ == "__main__":
    try:
        jksb(user, data)
    except Exception as e:
        print(e)
    finally:
        input("Press Any Key")
