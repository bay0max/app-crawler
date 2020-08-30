from bs4 import BeautifulSoup
import re
from queue import Queue
from time import sleep
import requests
import string
from  urllib.parse import urlparse
from  urllib.parse import parse_qs
from urllib.request import urlretrieve
import time
import urllib
import sys
from urllib import request
import wget

#得到该链接的对应的源码
def link2content(link):
    try:
        res = requests.get(url=link, headers=headers)
        res.encoding = 'utf-8'
        return res.text
    except Exception:
        sleep(0.1)
    return ""

#根据源码结构特征进行解析
def parse_link(url):
    soup = BeautifulSoup(link2content(url), 'html.parser')
    for bt in soup.find_all("a",class_='Mbtn'):
        try:
            soup1=BeautifulSoup(link2content(bt['href']), 'html.parser')
            dl= soup1.find('a',class_='btn_down_to_pc')
            queue_link.put(dl['href'])

            #parse =urlparse(bt.attrs['onclick'])
            #s=str(bt.attrs['onclick']).split('\'',13)
        except:
            continue


    print("parse link complete")


if __name__ == '__main__':
    queue_link = Queue() # 每个应用的详情页面对应链接队列
    headers= {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        } #报文头部
    cid = ['1002', '1003', '1001', '1007', '1012', '1008', '1005', '1016', '1006', '1015', '1004', '1011', '1010','1014','1013','1009']
    num = 1
    for c in cid:
        for page in range(1,11):
            link='http://zhushou.2345.com/sort/cid_'+c+'/down_'+str(page)+'.html'
            parse_link(link)
            while not queue_link.empty():
                try:
                    u = queue_link.get() #从队列中得到链接
                    print(u)
                    wget.download(u , './apk/'+str(num)+'.apk')#下载apk,参数为下载链接和路径
                    print('第',num,'个apk下载完成')
                    num = num+1
                    sleep(2)
                except:
                     print('出现错误，直接跳过，当前页面为： ',link)
                     continue

#有反爬虫机制下载速度较慢