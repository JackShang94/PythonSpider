# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
from tqdm import trange


"""
类说明:下载网络小说
Parameters:
    无
Returns:
    无
Modify:
    2021-05-13
"""


class novel_downloader(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com/'  # 小说网站链接
        self.target = 'https://www.bqkan8.com/2_2760/'  # 目录链接
        self.novel_name = '未找到名称.txt'  # 保存位置及名称
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = []  # 章节数

    def get_download_url(self):
        req = requests.get(url=self.target)
        req.encoding = req.apparent_encoding  # 防止中文乱码
        html = req.text
        div_bf = BeautifulSoup(html)

        info = div_bf.find_all('div', class_='info')
        info_bf = BeautifulSoup(str(info[0]))
        novel_name = info_bf.find_all('h2')
        self.novel_name = novel_name[0].text + '.txt'

        div = div_bf.find_all('div', class_='listmain')
        # print(div[0])  # Check div menu contents

        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a[13:])  # 剔除不必要的章节,并统计章节数

        for each in a[13:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    def get_contents(self, target):
        req = requests.get(url=target)
        req.encoding = req.apparent_encoding  # 防止中文乱码
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0' * 8, '\n\n')
        return texts

    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')


if __name__ == "__main__":
    dl = novel_downloader()
    dl.get_download_url()
    print(dl.novel_name + '开始下载：')

    # for i in range(dl.nums):
    #     dl.writer(dl.names[i], dl.novel_name, dl.get_contents(dl.urls[i]))
    #     print('已下载:' + '{:f}'.format(i / dl.nums) + '%\r')

    for i in trange(dl.nums):
        dl.writer(dl.names[i], dl.novel_name, dl.get_contents(dl.urls[i]))

    print(dl.novel_name + '下载完成')

