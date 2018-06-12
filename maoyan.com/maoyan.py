#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/6/11 15:14 
# @Author : Liang shu xian 
# @Site :  maoyan.com
# @File : maoyan.py
# @Software: Visual Studio


import json #标准库模块

#导入模块
import requests  # pip install requests
from lxml import etree
from requests.exceptions import RequestException

import headers


def get_html_text(url):
    '''得到一个页面的信息'''
    try:
        user_agent = {'user-agent': headers.headers()}
        r = requests.get(url, headers=user_agent, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  # utf-8
        return r.text
    except RequestException:
        return ''


def parse_one_page(text):
    html = etree.HTML(text)
    # 电影名
    name = html.xpath('//p[@class="name"]//text()')
    #主演名字
    star = html.xpath('//p[@class="star"]//text()')
    #上映时间
    releaseTime = html.xpath('//p[@class="releasetime"]//text()')

    for item in range(len(name)):
        yield{
            "index":item,
            "name":name[item],
            "star":star[item].strip(),
            "releaseTime":releaseTime[item]
        }


def write_to_file(content):
    with open(r'./maoyan.com/maoyan.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')


def main():
    for offset in range(10):
        url = 'http://maoyan.com/board/4?offset={}'.format(offset)
        text = get_html_text(url)
        for item in parse_one_page(text):
            write_to_file(item)


if __name__ == '__main__':
    f = open('./maoyan.com/maoyan.txt', 'w')
    f.close()
    main()
