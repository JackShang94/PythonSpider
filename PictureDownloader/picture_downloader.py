# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup
if __name__ == '__main__':
    target = 'https://www.dmzj.com/info/yaoshenji.html'
    req = requests.get(url=target)
    bs = BeautifulSoup(req.text)
    list_con_li = bs.find('ul', class_='list_con_li')
    comic_list = list_con_li.find_all('a')
    chapter_names = []
    chapter_urls = []
    for comic in comic_list:
        href = comic.get('href')
        name = comic.text
        chapter_urls.append(href)
        chapter_names.append(name)

print(chapter_names)
print(chapter_urls)