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


@expose('/weixin', methods=['POST'])
def customer_msg():
    if verification(request):
        data = request.data
        msg = parse_msg(data)
        if user_subscribe_event(msg):
            return help_info(msg)
        elif is_text_msg(msg):  # 如果是文字消息就先返回帮助信息
            content = msg['Content']
            if content == u'今日电影':
                cache = functions.get_cache()

                def tmovie():
                    return utils.moviespider()

                cache.get('tmovie', default='error', creator=tmovie)
                my_movie_list = cache['tmovie']
                recontent = utils.parse_list(my_movie_list)
                return response_text_msg(msg, recontent)


            return help_info(msg)

    return 'message processing fail'


def verification(request):
    """
    接入和消息推送校验
    """
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')

    token = 'seyren'
    tmplist = [signature, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()

    if hashstr == signature:
        return True
    return False

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


HELP_INFO = \
u"""
欢迎关注奉化生活^_^各种功能还在开发中
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

