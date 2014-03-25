#coding=utf-8
import os
import urllib
import urllib2
import cookielib





def violation_query():
    """交通违规查询"""

    cookie = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))














def check_code(urlopener):
    """下载验证码"""
    isOk = False


    try:
        imgfile = open('code.jpg', 'w')
        imgfile.write(urlopener.open(urllib2.Request('http://wf.nbjj.gov.cn/image.jsp?')).read())
        imgfile.close()

        isOk = True

    except:
        isOk = False

    return isOk






cookie = cookielib.CookieJar()

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

imgfile = open('code.jpg', 'w')

imgfile.write(opener.open(urllib2.Request('http://wf.nbjj.gov.cn/image.jsp?')).read())

imgfile.close()

authcode = raw_input(r'请输入验证码')

postdata = urllib.urlencode(
    {
        'cheHaoMa': '浙B·061X6',
        'clsbdm': '029131',
        'cheClass': '02',
        'yzm': authcode
    }
)


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    'Referer': 'http://wf.nbjj.gov.cn/',
    'Content-Type': 'application/x-www-form-urlencoded'
}




req = urllib2.Request(
    url='http://wf.nbjj.gov.cn/wzquery.jsp?time=1395723767390',
    data=postdata,
    headers=headers

)

result = opener.open(req)

print result.read()