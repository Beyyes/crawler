# -*- coding:utf8 -*-
__author__ = 'cgf1993'

import requests
import sys
import threading
from bs4 import BeautifulSoup,BeautifulStoneSoup
import os
from datetime import time, datetime
import time
from threading import Timer
# reload(sys)
reload(__import__('sys')).setdefaultencoding('utf-8')



class crawer:

    sohu_html = None
    sohu_bf = None
    url = None
    DIR = None
    interval = None

    def __init__(self, _url, _time, _dir):
        self.url = _url
        self.interval = _time
        self.DIR = _dir

    def fun(self):
        now = datetime.now()
        dir_pre = '/tmp/backup/'
        str_now = now.strftime('%Y%m%d%H%M%S')
        cur_dir = dir_pre + str(str_now)
        os.makedirs(cur_dir)
        os.makedirs(cur_dir + '/images')
        os.makedirs(cur_dir + '/js')
        os.makedirs(cur_dir + '/css')
        sohu_html = requests.get(url)
        content = BeautifulSoup(sohu_html.content, "lxml")
        # print content
        try:
            f = open(cur_dir + '/index.html', 'wb')
            f.write(sohu_html.content)

            images = content.findAll('img')
            image_urls = []
            for temp in images:
                image_urls.append(temp["src"])
            cnt = 1
            print image_urls
            for temp in image_urls:
                image_data = requests.get(temp).content
                print temp, cnt
                post = str(temp).split('.')[-1]
                image_file = open(cur_dir + '/images/' + str(cnt) + '.' + post, 'wb')
                image_file.write(image_data)
                cnt += 1
                image_file.flush()
                image_file.close()
            # get js
            js = content.findAll('script')
            print js
            cnt = 1
            for temp in js:
                js_file = open(cur_dir + '/js/' + str(cnt) + '.js', 'wb')
                js_content = requests.get(temp["src"]).content
                js_file.write(js_content)
                cnt += 1
            # get css
            css = content.findAll('link')
            print css
        except Exception, e:
            print e


if __name__ == "__main__":

    d = sys.argv[1]   # 参数的输入未判别是否合法
    interval = sys.argv[2]
    u = sys.argv[3]
    url = sys.argv[4]
    o = sys.argv[5]
    DIR = sys.argv[6]
    # print d == '-d'
    if d != '-d' or u != '-u':
        print 'main.py -d 60 -u http://m.sohu.com -o \\tmp\\backup'
    test = crawer(url, interval, DIR)
    test.fun()
    # while 1:
    #     test.fun()
    #     time.sleep(60)
