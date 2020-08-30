from bs4 import BeautifulSoup
import re
from  urllib.parse import urlparse
from  urllib.parse import parse_qs
from queue import Queue
from time import sleep
import requests
import string
from urllib.request import urlretrieve
import time
import urllib
import sys
from urllib import request
import wget

#得到该链接的对应的源码
def link2content(link):
    for i in range(4):
        try:
            res = requests.get(url=link, headers=headers)
            res.encoding = 'utf-8'
            #print(res.text)
            return res.text
        except Exception:
            sleep(0.1)
    return ""

#根据源码结构特征进行解析
def parse_link(url):
    soup = BeautifulSoup(link2content(url), 'html.parser')
    for bt in soup.find_all("a",class_=re.compile('dbtn')):
        try:
            parse=urlparse(bt['href'])
            if parse.path!='/':
                path=parse_qs(parse.path)
                #print(path['url'][0])
                queue_link.put(path['url'][0])
        except:
            continue
    print("parse link complete")

if __name__ == '__main__':
    queue_link = Queue() # apk下载链接队列
    headers= {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        }
    cid=['11','12','14','15','16','17','18','102228','102230','102231','102232','102139','102239']

    for c in cid:
        for page in range(1,51):
            #link = 'http://zhushou.360.cn/list/index/cid/11/'
            link ='http://zhushou.360.cn/list/index/cid/'+c+'/?page='+str(page)
            parse_link(link)
            num=1
            while not queue_link.empty():
                try:
                    u = queue_link.get()
                    print(u)
                    #urlretrieve(u,'./apk/'+str(num)+'.apk',Schedule)

                    wget.download(u,'./apk/'+str(num)+'.apk')
                    print('第',num,'个apk下载完成')
                    sleep(1)
                    num = num+1
                    sleep(1)
                except:
                    print('出现错误，直接跳过，当前页面为： ', link)
                    continue

