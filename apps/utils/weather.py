#__author__ = 'seyren'
#coding=utf-8
import json
import urllib2

class WeatherQuery(object):
    """天气查询模块"""
    def __init__(self, cityname):
        self.cityname = cityname
        self.apiurl = "http://api2.sinaapp.com/search/weather/?appkey=0020130430&appsecert=fa6095e113cd28fd&reqtype=text&keyword=%s" % cityname

    def queryw(self):

        # 把json格式decode成dict
        try:
            weather_json = urllib2.urlopen(self.apiurl).read()
            weather = json.loads(weather_json)
        except:
            return "系统故障"
        return weather['text']['content']




