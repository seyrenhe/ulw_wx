#coding=utf-8
#__author__ = 'seyren'

import urllib2
from bs4 import BeautifulSoup as bs
import time
import hashlib


_time = time.strftime('%Y%m%d',time.localtime(time.time())) # 当前时间 格式为yearmonthday






def moviespider(_time=_time):
    url = 'http://theater.mtime.com/China_Zhejiang_Province_Fenghua/3869/?d=%s' % _time

    page = urllib2.urlopen(url)
    soup = bs(page)

    original = soup.find_all(class_='table')
    m_count = len(original)
    movie_list = []
    movie_name = []
    movie_time = []
    movie_price = []

    for i in range(0,m_count):
        name_temp = []
        time_temp = []
        price_temp = []

        name_temp.append(original[i].find(class_='c_000').text)

        for t in original[i].find_all('strong'):
            time_temp.append(t.text)
        #time_temp=qc(time_temp)
        for p in original[i].find_all('em'):
            price_temp.append(p.text)

        movie_name.extend(name_temp)
        movie_time.append(time_temp)
        movie_price.append(price_temp)

    movie_list.append(movie_name)
    movie_list.append(movie_time)
    movie_list.append(movie_price)

    return movie_list

