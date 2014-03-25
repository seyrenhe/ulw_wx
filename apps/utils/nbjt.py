#coding=utf-8

import urllib
import urllib2
import cookielib




cookie = cookielib.CookieJar()


opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))


postdata = urllib.urlencode(
    {
        'cheHaoMa': '浙B·061X6',
        'clsbdm': '029131',
        'cheClass': '02',
        'yzm': ''
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