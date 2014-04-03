#coding=utf-8

import hashlib, time, json
from uliweb import expose, functions
import xml.etree.ElementTree as ET  #解析xml
import utils


# uliweb cache
@expose('/')
def index():
    cache = functions.get_cache()
    print cache.get('test', default='ss', creator=my_creator)
    print cache['test']
    return '<h1>Hello, Uliweb</h1>'


def my_creator():
    return 'test'


@expose('/weixin', methods=['GET'])
def access_verify():
    echostr = request.args.get('echostr')
    if utils.verification(request) and echostr is not None:
        return echostr
    return 'verification fail'


# @expose('/weixin', methods=['POST'])
# def customer_msg():
#     if utils.verification(request):
#         data = request.data
#         msg = parse_msg(data)
#         if user_subscribe_event(msg):
#             return help_info(msg)
#         elif is_text_msg(msg):  # 如果是文字消息就先返回帮助信息
#             s1 = msg['Content'].strip()
#             content = ''.join(s1.split(' '))
#             if content == u'今日电影':
#                 cache = functions.get_cache()
#
#                 def tmovie():
#                     """动态构建函数，供cache对像使用"""
#                     movie_list = utils.moviespider()
#                     return response_news_msg(msg, movie_list)
#
#                 cache.get('tmovie', default='error', creator=tmovie)
#                 recontent = cache['tmovie']
#                 return recontent
#             elif content == u'违规查询':
#
#                 pass
#             # 有天气两个字就调用天气模块
#             elif content.find(u'天气')  > 0:
#                 cityname = content[0:-2].encode('UTF-8')
#                 weatherq = utils.weather.WeatherQuery(cityname)
#                 recontent = weatherq.queryw()
#                 return response_text_msg(msg, recontent)
#
#             return help_info(msg)
#
#     return 'message processing fail'

@expose('/weixin', methods=['POST'])
def customer_msg():
    data = request.data
    msg = parse_msg(data)
    if user_subscribe_event(msg):
        return help_info(msg)
    elif is_text_msg(msg):  # 如果是文字消息就先返回帮助信息
        content = msg['Content']
        if content == u'今日电影':
            cache = functions.get_cache()

            def tmovie():
                """动态构建函数，供cache对像使用"""
                movie_list = utils.moviespider()
                return response_news_msg(msg, movie_list)

            cache.get('tmovie', default='error', creator=tmovie)
            recontent = cache['tmovie']
            # recontent = utils.parse_movie_list(my_movie_list)
            # return response_text_msg(msg, recontent)
            return recontent
        elif content == u'违规查询':
            return for_single_item(msg)
        elif content == u'测试':
            return response_news_msg(msg)
        # 有天气两个字就调用天气模块
        elif content.find(u'天气') != -1:
            cityname = content[0:-2].encode('UTF-8')
            weatherq = utils.weather.WeatherQuery(cityname)
            recontent = weatherq.queryw()
            return response_text_msg(msg, recontent)

        return help_info(msg)
    return 'message processing fail'



def parse_msg(rawmsgstr):
    """
    将xml消息解析为dict字典
    """
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def is_text_msg(msg):
    """判断是否是文字消息"""
    return msg['MsgType'] == 'text'

def user_subscribe_event(msg):
    """"""
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'


def help_info(msg):
    return response_text_msg(msg, HELP_INFO)


def response_text_msg(msg, content):
    s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'],
        str(int(time.time())), content)
    return s


def response_news_msg(msg, movie_list):
    msg_header = NEWS_MSG_HEADER_TPL % (msg['FromUserName'], msg['ToUserName'],
                                        str(int(time.time())), len(movie_list))  # 括号里的内容不用反斜杠\就能换行
    msg = ''
    msg += msg_header
    msg += make_articles(movie_list)
    msg += NEWS_MSG_TAIL
    return msg


def make_articles(movie_list):
    msg = ''
    for i, item in enumerate(movie_list):
        msg += make_items(item, i+1)
    return msg


def make_items(item, itemindex):
    time_price = ''
    for i in sorted(item['time-price'].keys()):
        time_price += u'%s-%s' % (i, item['time-price'][i]) + ' '
    title = u'%s' % item['name'] + time_price
    description = ''
    pic_url = item['pic']
    url = item['url']
    item = NEWS_MSG_ITEM_TPL % (title, description, pic_url, url)
    return item

def for_single_item(msg):
    msg_header = NEWS_MSG_HEADER_TPL % (msg['FromUserName'], msg['ToUserName'],
                                        str(int(time.time())), 1)  # 括号里的内容不用反斜杠\就能换行
    msg = ''
    msg += msg_header
    title = u'宁波交通局官方查询网站'
    description = u'安全，放心'
    picUrl = 'http://imgt2.bdstatic.com/it/u=1024854720,2703624734&fm=21&gp=0.jpg'
    url = 'http://wf.nbjj.gov.cn'
    item = NEWS_MSG_ITEM_TPL % (title, description, picUrl, url)
    msg += item
    msg += NEWS_MSG_TAIL
    return msg







HELP_INFO = \
u"""欢迎关注奉化生活^_^各种功能还在开发中,输入'今日电影'可以查博纳电影放映详情，输入'地名天气'，比如'奉化天气'可以查询奉化的天气。如果好用的话请别忘了推荐给你的小伙伴哦  by Seyren
"""


NEWS_MSG_ITEM_TPL = \
u"""
<item>
    <Title><![CDATA[%s]]></Title>
    <Description><![CDATA[%s]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
</item>
"""

TEXT_MSG_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""

NEWS_MSG_HEADER_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<Content><![CDATA[]]></Content>
<ArticleCount>%d</ArticleCount>
<Articles>
"""

NEWS_MSG_TAIL = \
u"""
</Articles>
<FuncFlag>1</FuncFlag>
</xml>
"""
