import requests
import os
# 持久存贮
import json
import datetime
import re


def review_time(today):
    delta_list = [1, 1, 2, 2, 3, 4, 5, 5]  # 每两天复习的间隔
    review_day = []
    new_day = datetime.datetime.strptime(today, '%m-%d')
    for day in delta_list:
        new_day = datetime.datetime.strptime(new_day.strftime('%m-%d'), '%m-%d') + datetime.timedelta(days=day)
        review_day.append(new_day.strftime('%m-%d'))
    return review_day


def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename, 'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存成功")


def all_files_path(rootDir):
    txt_path = []
    for root, dirs, files in os.walk(rootDir):  # 分别代表根目录、文件夹、文件
        for file in files:  # 遍历文件
            file_path = os.path.join(root, file)  # 获取文件绝对路径
            if file_path.endswith(".txt"):
                if not txt_path.__contains__(file_path):
                    txt_path.append(file_path)
        for dir in dirs:  # 遍历目录下的子目录
            dir_path = os.path.join(root, dir)  # 获取子目录路径
            all_files_path(dir_path)  # 递归调用
    return txt_path


def ifNeed_V():
    rev_text = all_files_path('./')
    for i in rev_text:
        f = open(i, encoding='gbk')
        txt = []
        for line in f:
            if line.strip() == datetime.datetime.now().strftime('%m-%d'):
                li = re.findall(r'./(.+)\\', i)
                if li:
                    print("今天需要复习" + str(li))


if __name__ == '__main__':
    ifNeed_V()
    while True:
        q = input("输入翻译单词\n")
        if q == 'q':
            break;
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/110.0.0.0 Safari/537.36 "
        }
        posurl = "https://fanyi.baidu.com/sug"
        data = {
            "kw": q
        }
        # 请求发送
        res = requests.post(url=posurl, data=data, headers=header)
        print(res.status_code)
        # 读取返回值
        print(res.json())
        dict_a = res.json()
        # 持久保存
        f_p = r"./" + str(datetime.date.today()) + "history"
        if not os.path.exists(f_p):
            os.mkdir(f_p)
            rev = review_time(datetime.datetime.now().strftime('%m-%d'))
            text_save(f_p + '/revtime.txt', rev)
        file_name = f_p + "/" + q + ".json"
        if not dict_a["data"]:
            print("单词不存在")
            continue
        fp = open(file_name, 'w', encoding='utf-8')
        json.dump(dict_a, fp=fp, ensure_ascii=False)
        fp.close()
        print('完成')
