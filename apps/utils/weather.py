#__author__ = 'seyren'
#coding=utf-8
import json
import urllib2

class WeatherQuery(object):
    """天气查询模块"""
    def __init__(self, cityname):
        self.cityname = cityname
        self.apiurl = "http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=2f8a8f64772ea877b5a19367b05138a5" % cityname

    def queryw(self):

        # 把json格式decode成dict
        try:
            weather_json = urllib2.urlopen(self.apiurl, timeout=4).read()
            weather = json.loads(weather_json)
            s = self.parse_weather_data(weather)
        except:
            return u"系统/网络故障"
        return s

    def parse_weather_data(self, weather):
        msg = ''
        if weather['status'] == 'success':
            weatherdata = weather['results'][0]['weather_data']
            for x in weatherdata:
                msg += x['date']
                msg += x['weather']
                msg += x['temperature']
                msg += x['wind'] + '\n'
            msg = weather['results'][0]['currentCity'] + u'天气\n' + msg
            return msg
        else:
            return u'数据库中无此地名'
        weatherdata = weather['results'][0]['weather_data']
        
        for x in weatherdata:
            msg += x['date']
            msg += x['weather']
            msg += x['temperature']
            msg += x['wind'] + '\n'
        return msg
