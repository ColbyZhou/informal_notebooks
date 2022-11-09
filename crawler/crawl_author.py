#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
#
# Copyright (c) 2021 www.tencent.com, Inc. All Rights Reserved
#
################################################################################

"""
This module provide service.

Author: zhouqiang
Date:   2021/08/29 20:02:41
"""

from bs4 import BeautifulSoup
import requests
import sys
import time

reload(sys)
sys.setdefaultencoding('utf-8')


host = "https://so.gushiwen.cn/"

home_page_list = []
for index in range(1, 11):
    cur = "https://so.gushiwen.cn/shiwens/default.aspx?page=" + str(index) + "&tstr=&astr=%E5%88%98%E7%A6%B9%E9%94%A1&cstr=&xstr="
    home_page_list.append((index, cur))

def fetch_shiwen(page_url, file_name):
    file = open("author_one_line/" + file_name + "txt", 'w')
    p_file = open("author_normal/" + file_name + "txt", 'w')
    h_file = open("author_html/" + file_name + "html", 'w')
    res = requests.post(page_url)
    #print(res)
    #print(dir(res))
    #print(res.content)

    soup = BeautifulSoup(res.content)
    #print(soup)
    typecont_list = soup.find_all('div',class_='cont')
    #print(typecont)
    #print(len(typecont))

    for typecont in typecont_list:
        links = typecont.find_all('a')
        #print(len(links))
        for idx, link in enumerate(links):
            #print(link)
            url = link.get('href')
            style = link.get("style")
            if style != "font-size:18px; line-height:22px; height:22px;":
                continue
            title = link.get_text()
            title = title.decode('utf-8').encode('utf-8')
            title = title.replace("\n", "")
            file.write(title + "\t")
            title = "    " + title
            print >> p_file, title
            print >> h_file, "<p>" + title + "<br>"
            if url is None:
                #print "title error:" + title
                continue
            if "http" not in url:
                url = host + url
            #print(url)

            cur_res = None
            for _ in range(5):
                cur_res = requests.post(url)
                if cur_res.status_code != 200:
                    time.sleep(0.5)
                else:
                    break
                #print(cur_res.content)
            if cur_res is None:
                continue
            #print(cur_res.content)

            page_shiwen = cur_res.content
            soup_shiwen = BeautifulSoup(page_shiwen)
            shiwen_list = soup_shiwen.find_all('div', class_ = 'contson')
            if len(shiwen_list) == 0:
                continue
            shiwen = shiwen_list[0]
            #print(shiwen)
            for cont in shiwen.contents:
                #print(dir(cont))
                shiwen_text = str(cont).decode('utf-8').encode('utf-8')
                print >> h_file, shiwen_text
                #if 'br' in shiwen_text:
                #    continue
                shiwen_text = shiwen_text.replace("\n", "").replace("<p>", "").replace("</p>", "").replace("<br/>", "").replace("<br>", "").replace("</br>", "")
                if len(shiwen_text) == 0:
                    continue
                file.write(shiwen_text)
                print >> p_file, shiwen_text
            file.write("\n")
            print >> p_file, "\n"
            print >> h_file, "<br></p><br><br>"

            #print(dir(shiwen))
            #print(len(shiwen))

            #if idx > 3:
            #    break
    file.close()


author = "liuyuxi"
print(home_page_list)
for idx, home_page in home_page_list:
    fetch_shiwen(home_page, author + "_" + str(idx) + ".")


