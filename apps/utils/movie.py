# coding=utf-8
import urllib2
from bs4 import BeautifulSoup as bs
import hashlib, time, json


def moviespider():
    url1 = 'http://theater.mtime.com/China_Zhejiang_Province_Fenghua/3869/'
    url2 = 'http://theater.mtime.com/China_Zhejiang_Province_Fenghua_yuelinjiedao/2834/'

    page = urllib2.urlopen(url1)
    soup = bs(page)

    original = soup.find_all(class_='table')
    m_count = len(original)
    movie_list = []
    for i in range(0, m_count):
        # movie_time = ''
        # movie_price = ''
        movie_dict = {}
        movie_dict_time = {}
        movie_name = original[i].find(class_='c_000').text
        movie_dict['name'] = movie_name
        for t in original[i].find_all('b'):
            p = t.previousSibling
            #print "======>", p, t.contents[0]
            movie_dict_time[t.contents[0].text] = p.text
        movie_dict['time-price'] = movie_dict_time
        movie_dict['pic'] = original[i].find(class_='i_img')['src']
        # for t in original[i].find_all('strong'):
        #     movie_time += t.text + ' '
        # movie_dict['time'] = movie_time
        # for p in original[i].find_all('em'):
        #     movie_price += p.text + ' '
        # movie_dict['price'] = movie_price
        movie_list.append(movie_dict)
    return movie_list

s = moviespider()
print s

def parse_move_list(movie_list):
    for x in xrange(len(movie_list[0])):
        for y in xrange(len(movie_list[1][x])):
            return movie_list[0][x] + '\n' + movie_list[1][x][y] + movie_list[2][x][y]

# def moviespider():
#     url1 = 'http://theater.mtime.com/China_Zhejiang_Province_Fenghua/3869/'
#     url2 = 'http://theater.mtime.com/China_Zhejiang_Province_Fenghua_yuelinjiedao/2834/'
#
#     page = urllib2.urlopen(url1)
#     soup = bs(page)
#
#     original = soup.find_all(class_='table')
#     m_count = len(original)
#     movie_list = []
#     for i in range(0, m_count):
#         movie_time = ''
#         movie_price = ''
#         movie_dict = {}
#         movie_dict_time = {}
#         movie_name = original[i].find(class_='c_000').text
#         movie_dict['name'] = movie_name
#         for t in original[i].find_all('strong'):
#             for p in original[i].find_all('em'):
#                 movie_dict_time[t.text] = p.text
#         movie_dict['time-price'] = movie_dict_time
#         # for t in original[i].find_all('strong'):
#         #     movie_time += t.text + ' '
#         # movie_dict['time'] = movie_time
#         # for p in original[i].find_all('em'):
#         #     movie_price += p.text + ' '
#         # movie_dict['price'] = movie_price
#         movie_list.append(movie_dict)
#     return movie_list


    # movie_list = []
    # movie_name = []
    # movie_time = []
    # movie_price = []
    #
    # for i in range(0, m_count):
    #     name_temp = []
    #     time_temp = []
    #     price_temp = []
    #
    #     name_temp.append(original[i].find(class_='c_000').text)
    #
    #     for t in original[i].find_all('strong'):
    #         time_temp.append(t.text)
    #     #time_temp=qc(time_temp)
    #     for p in original[i].find_all('em'):
    #         price_temp.append(p.text)
    #
    #     movie_name.extend(name_temp)
    #     movie_time.append(time_temp)
    #     movie_price.append(price_temp)
    #
    # movie_list.append(movie_name)
    # movie_list.append(movie_time)
    # movie_list.append(movie_price)
    #
    # return movie_list



