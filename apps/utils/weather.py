#__author__ = 'seyren'
#coding=utf-8
import json
import urllib2

class WeatherQuery(object):
    """天气查询模块"""
    def __init__(self, cityname):
        self.cityname = cityname
        self.apiurl = "http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=5slgyqGDENN7Sy7pw29IUvrZ" % cityname

    def queryw(self):

        # 把json格式decode成dict
        try:
            print self.apiurl
            weather_json = urllib2.urlopen(self.apiurl).read()
            weather = json.loads(weather_json)
        except:
            return "系统故障"
        return self.parse_weather_data(weather)

    def parse_weather_data(self, weatherdata):
        msg = ''
        weatherdata = weatherdata['results'][0]['weather_data']
        for x in weatherdata:
            msg += x['date']
            msg += x['weather']
            msg += x['temperature']
            msg += x['wind'] + '\n'
        return msg

