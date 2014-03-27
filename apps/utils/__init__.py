# coding=utf-8
import urllib2
from bs4 import BeautifulSoup as bs
import hashlib, time, json
import weather

_time = time.strftime('%Y%m%d',time.localtime(time.time())) # 当前时间 格式为yearmonthday


def moviespider():
    url = 'http://theater.mtime.com/China_Zhejiang_Province_Fenghua/3869/'

    page = urllib2.urlopen(url)
    soup = bs(page)

    original = soup.find_all(class_='table')
    m_count = len(original)
    movie_list = []
    movie_name = []
    movie_time = []
    movie_price = []

    for i in range(0, m_count):
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


def verification(request):
    """
    接入和消息推送校验
    """
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')

    token = 'seyren'
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()

    if hashstr == signature:
        return True
    return False


def parse_movie_list(movie_list):
    s = ''
    for x in xrange(len(movie_list[0])):
        for y in xrange(len(movie_list[1][x])):
            s += movie_list[0][x] + movie_list[1][x][y] + movie_list[2][x][y] + '\n'
    return s
