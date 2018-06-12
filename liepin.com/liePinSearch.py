#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/5/22 9:42 
# @Author : joey
# @content : 
# @File : liePinSearch.py 
# @Software: PyCharm


import csv
import time
from multiprocessing import Pool

import bs4
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

import fenxi
import headers


def get_html_text(url):
    try:
        user_agent = {'user-agent': headers.headers()}
        r = requests.get(url, headers=user_agent, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  # utf-8
        return r.text
    except RequestException:
        return ' '


def parse_page_list(uList, html):
    soup = BeautifulSoup(html, "html.parser")
    try:
        for li in soup.find(class_="sojob-list").children:
            if isinstance(li, bs4.element.Tag):
                if li.h3.a['href']:
                    uList.append(li.h3.a['href'])
            else:
                uList
        return uList
    except AttributeError:
        return []


def parse_des_page(html, isVip):
    data = []
    soup = BeautifulSoup(html, "html.parser")
    if not soup.find('h1') is None:
        title = soup.find('h1').text
    else:
        return data
    salary = ''
    if not soup.find(class_='job-item-title') is None:
        parTag = soup.find(class_='job-item-title')
        if not soup.find(class_='job-item-title').find('span')is None:
            tag = parTag.span.extract()
            salary = parTag.text
        elif not soup.find(class_='job-item-title').find('strong')is None:
            tag = parTag.strong.extract()
            salary = parTag.text

    elif not soup.find(class_='job-main-title') is None:
        parTag = soup.find(class_='job-main-title')
        if not soup.find(class_='job-main-title').find('span')is None:
            tag = parTag.span.extract()
            salary = parTag.text
        elif not soup.find(class_='job-main-title').find('strong')is None:
            tag = parTag.strong.extract()
            salary = parTag.text
        else:
            salary = parTag.text
    location = ''
    if not soup.find(class_='basic-infor') is None:
        if not soup.find(class_='basic-infor').find('span') is None:
            location = soup.find(class_='basic-infor').find('span').text
    elif not soup.find(class_='job-main-tip') is None:
        if not soup.find(class_='job-main-tip').find('span') is None:
            location = soup.find(class_='job-main-tip').find('span').text

    education = ''
    workingLife = ''
    language = ''
    age = ''
    i = 0
    try:
        for span in soup.find(class_='job-qualifications').children:
            if isinstance(span, bs4.element.Tag):
                if i == 0:
                    education = span.text
                elif i == 1:
                    workingLife = span.text
                elif i == 2:
                    language = span.text
                else:
                    age = span.text
                i = i + 1
    except AttributeError:
        ''
    try:
        for span in soup.find(class_='job-title-left').find(class_='resume').children:
            if isinstance(span, bs4.element.Tag):
                if i == 0:
                    education = span.text
                elif i == 1:
                    workingLife = span.text
                elif i == 2:
                    language = span.text
                else:
                    age = span.text
                i = i + 1
    except AttributeError:
        ''
    walefair = ''
    try:
        for span in soup.find(class_='tag-list').children:
            if isinstance(span, bs4.element.Tag):
                walefair = walefair + span.text + ','
    except AttributeError:
        ''
    postDuties = ''
    tenureRequirements = ''
    if not soup.find(class_='job-description') is None:
        jobTag = soup.find(class_='job-description').find(class_='content')
    else:
        jobTag = soup.find(class_='job-info-content')
    if not jobTag is None:
        content = jobTag.text
        splitContent = content.split('职位要求')
        splitContent = content.split('任职')
        for i in range(len(splitContent)):
            if i == 0:
                postDuties = splitContent[i]
            if i == 1:
                tenureRequirements = splitContent[i]
    department = ''
    if not soup.find_all("span", text="所属部门：") is None:
        for tag in soup.find_all("span", text="所属部门："):
            if not tag.parent.find('label') is None:
                department = tag.parent.find('label').text
            else:
                parTag = tag.parent
                if not parTag.find('span') is None:
                    tag = parTag.span.extract()
                department = parTag.text
    proRequirement = ''
    if not soup.find_all("span", text="专业要求：") is None:
        for tag in soup.find_all("span", text="专业要求："):
            if not tag.parent.find('label') is None:
                proRequirement = tag.parent.find('label').text
            else:
                parTag = tag.parent
                if not parTag.find('span') is None:
                    tag = parTag.span.extract()
                proRequirement = parTag.text
    reportTO = ''
    if not soup.find_all("span", text="汇报对象：") is None:
        for tag in soup.find_all("span", text="汇报对象："):
            if not tag.parent.find('label') is None:
                reportTO = tag.parent.find('label').text
            else:
                parTag = tag.parent
                if not parTag.find('span') is None:
                    tag = parTag.span.extract()
                reportTO = parTag.text
    reportBy = ''
    if not soup.find_all("span", text="下属人数：") is None:
        for tag in soup.find_all("span", text="下属人数："):
            if not tag.parent.find('label') is None:
                reportBy = tag.parent.find('label').text
            else:
                parTag = tag.parent
                if not parTag.find('span') is None:
                    tag = parTag.span.extract()
                reportBy = parTag.text
    industry = ''
    scale = ''
    i = 0
    try:
        if not soup.find(class_='new-compintro') is None:
            for li in soup.find(class_='new-compintro').children:
                if isinstance(li, bs4.element.Tag):
                    if i == 0:
                        if not li.find("a") is None:
                            industry = li.find("a").text
                    elif i == 1:
                        scale = li.text[5:]
                        break
                    i = i + 1
    except AttributeError:
        ''
    viewRate = ''
    i = 0
    try:
        if not soup.find(class_='apply-check') is None:
            for span in soup.find(class_='apply-check').children:
                if isinstance(span, bs4.element.Tag):
                    if not span.find('em') is None:
                        if i == 0:
                            viewRate = span.find("em").text + "%"
                            break
    except AttributeError:
        ''
    i = 0
    try:
        if not soup.find(class_='view-rate') is None:
            for span in soup.find(class_='view-rate').children:
                if isinstance(span, bs4.element.Tag):
                        if i == 0:
                            viewRate = span.text
                            break
    except AttributeError:
        ''
    write_into_xls('lieping', postDuties+tenureRequirements)
    write_into_xls('fuli', walefair.replace(",", ""))
    write_into_xls('liepingrenzhi', tenureRequirements)
    write_into_xls('liepingzhiwei', postDuties)
    data = [title, salary, location, education, workingLife,
            language, age, walefair, postDuties, tenureRequirements,
            department, proRequirement, reportTO, reportBy, industry,
            scale, viewRate, isVip]
    print(data)
    return data


def write_into_excel(dataList):
    print(dataList)
    with open('lieping.csv', 'a', newline='', errors='ignore')as f:
        writer = csv.writer(f)
        writer.writerows(dataList)

def write_into_xls(name, data):
    with open(name + '.txt', 'a', newline='', errors='ignore')as f:
        f.write(data)

def main(page):
    print("第{0}页".format(page))
    key = '猎头'
    url = 'https://www.liepin.com/zhaopin/?' \
          + 'fromSearchBtn=' + str(page) \
          + '&key=' + key \
          + '&curPage='+str(page)
    uList = []
    html = get_html_text(url)
    uList = parse_page_list(uList, html)
    i = 0
    datas = []
    for href in uList or []:
        i = i+1
        isVip =''
        if '/a/' in href:
            href = 'https://www.liepin.com' + href
            isVip = '1'
        print(href)
        html = get_html_text(href)
        data = parse_des_page(html, isVip)
        if len(data) > 0 or data != []:
            datas.append(data)
    write_into_excel(datas)


if __name__ == '__main__':
    start = time.clock()
    # 初始化文件
    fieldnames = ['职位', "薪金范围", "所在地", "学历", "工作年限", "语言", "年龄", "员工福利",
                  "岗位职责", "任职要求", "所属部门", "专业要求", "汇报对象", "下属人数",
                  "行业", "公司规模", "应聘查看率", "是否仅限VIP查看"]
    f = open('lieping.csv', 'w', newline="")
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    zf = open('liepingzhiwei.txt', 'w')
    rf = open('liepingrenzhi.txt', 'w')
    lf = open('lieping.txt', 'w')
    lf = open('fuli.txt', 'w')
    pool = Pool(processes=100)
    pool.map_async(main, range(1, 100))
    f.close()
    zf.close()
    rf.close()
    lf.close()
    pool.close()
    pool.join()
    fenxi.analyse('lieping', '职位描述')
    fenxi.analyse('liepingrenzhi', '任职要求')
    fenxi.analyse('liepingzhiwei', '岗位职责')
    fenxi.analyse('fuli', '员工福利')
    elapsed = (time.clock() - start)
    print("Time used:", elapsed)
