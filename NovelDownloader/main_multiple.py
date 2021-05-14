# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
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
        self.server = 'https://www.xsbiquge.com/'  # 小说网站链接
        self.target = 'https://www.vbiquge.com/15_15338/'  # 目录链接
        self.novel_name = '未找到名称.txt'  # 保存位置及名称
        self.names = []  # 存放章节名
        self.urls = []  # 存放章节链接
        self.nums = []  # 章节数

    def get_download_url(self):
        req = requests.get(url=self.target)
        req.encoding = req.apparent_encoding  # 防止中文乱码
        html = req.text
        div_bf = BeautifulSoup(html)

        info = div_bf.find_all('div', id='info')
        info_bf = BeautifulSoup(str(info[0]))
        novel_name = info_bf.find_all('h1')
        self.novel_name = novel_name[0].text + '.txt'

        div = div_bf.find_all('div', id='list')

        a_bf = BeautifulSoup(str(div[0]))
        a = a_bf.find_all('a')
        self.nums = len(a)  # 剔除不必要的章节,并统计章节数

        for each in a:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))

    def get_contents(self, target):
        req = requests.get(url=target)
        req.encoding = req.apparent_encoding  # 防止中文乱码
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('div', id='content')
        texts = texts[0].text.replace('\xa0' * 4, '\n\n')
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

    for i in trange(dl.nums):
        dl.writer(dl.names[i], dl.novel_name, dl.get_contents(dl.urls[i]))

    print(dl.novel_name + '下载完成')
