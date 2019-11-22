'''
@Descripttion: 
@version: Dev
@Author: CHEN
@Date: 2019-11-21 21:56:14
@LastEditors: CHEN
@LastEditTime: 2019-11-22 19:47:25
'''
import requests
import time
from lxml import etree
import random
import os
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}


def get_files(url, header=None):

    try:
        if header is not None:
            re = requests.get(url, headers=header)
        else:
            re = requests.get(url, headers=headers)
        print(re.status_code)
        # return etree.HTML(re.text)
        return re
    except:
        print(re.status_code)
        return ""


def get_list(url, header):
    print(url)
    dic = dict()
    js = json.loads(get_files(url, header).text)
    # 拿到Json数据，封装
    for i in range(len(js["data"])):
        print(js["data"][i]
              ["subject_title"], js["data"][i]["file_lists"][0]["file_url"])

        dic[js["data"][i]["subject_id"]] = [js["data"][i]
                                            ["subject_title"], js["data"][i]["file_lists"][0]["file_url"]]
    
    return dic


def get_dowm_flie_list(dic=dict(), file_address=""):

    subject_id = dict()
    header = dict()
    header["User-Agent"] = headers["User-Agent"]
    # 从dict中取出数据
    for key, value in dic.items():
        now = round((time.time()*1000))
        header["referer"] = "https://wenku.sanhao.com/ziliao-subject-{}.html".format(
            key)
        url = "https://wenku.sanhao.com//api.php?act=file_subject&method=detail&subject_id={}&_={}".format(
            key, now)
        print(url)
        # print(header)
        js = json.loads(get_files(url, header).text)

        # 如果拿到文件列表，新建文件夹，开始下载
        try:
            file_list = js["data"]["file_lists"]

            tf_address = file_address+value[0]
            print(tf_address)
            if not os.path.exists(tf_address):
                os.mkdir(tf_address)
                print("新建了个文件")
            # file_list = 文件URL
            down_flie(key, value[1], file_list, tf_address)
        except:
            # 拿不到，记录subject_id
            print("拿不到")
            subject_id[key] = value
        time.sleep(random.uniform(2, 10))

    return subject_id


def down_flie(subject_id, url_jud, file_list, file_addres):
    # http://ziliao.sanhao.com/file_subject/6328/
    base_url = "http://"
    try:
        for each in file_list:
            tf_url_list = url_jud.split("/")
            # file_url: "http://ziliao.sanhao.com/ftp/资料库资料/高中化学/2017-2018学年人教版化学必修1热点专题高分特训/2017-2018学年人教版化学必修1热点专题高分特训钠及其化合物.doc"
            url = base_url
            for i in range(2, len(tf_url_list)-1):
                url += tf_url_list[i]+"/"
            print("--------------{}".format(url))

            url += each["file_name"]+"." + each["file_ext"]
            print("--------------{}".format(url))
            # print("url = {}".format(url))
            save_files(url, file_addres+"/")
            time.sleep(random.uniform(0, 1))

    except:
        print("url获取失败")


def save_files(url, file_address):
    try:
        time.sleep(random.uniform(0, 1))
        res = get_files(url)
        if res == "":
            return "访问不到数据"
        else:
            print("成功访问")
        print(file_address)
        print(url.split("/")[-1])
        with open(file_address+url.split("/")[-1], "wb") as f:
            f.write(res.content)
    except:
        print("存储有误")


if __name__ == '__main__':

    # file_address = "D:\\workspace\\VSCode\\HighSchoolSpider\\三好网\\"
    file_address = os.getcwd()+"/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "referer": "https://wenku.sanhao.com/index.php?u=p2"
    }
    for i in range(0, 90):
        url = "https://wenku.sanhao.com//api.php?act=file_subject&method=lists&subject_cat=1&subject_tag=0&subject_type=0&subject_category=0&subject_cat_id=0&sort=1&limit={}&count=15".format(
            str(i*15))
        # print(url)
        header["referer"] = "https://wenku.sanhao.com/index.php?u=p{}".format(
            str(i+1))
        # print(header)
        dic = get_list(url, header)
        # url = https://wenku.sanhao.com/ziliao-subject-dic.key.html
        subj_id = get_dowm_flie_list(dic, file_address)
        with open(file_address+"sub_id.txt", "a") as f:
            for key, value in subj_id.items():
                f.write("{}:{}\n".format(key, value))
