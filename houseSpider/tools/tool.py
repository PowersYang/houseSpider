# -*- coding: utf-8 -*-
from xpinyin import Pinyin


class tools:
    p = Pinyin()

    @classmethod
    def get_pinyin_ajk(self, city):
        if city == u"重庆":
            return 'chongqing'
        elif city == u"厦门":
            return 'xm'
        else:
            return self.p.get_pinyin(city, u'')

    @classmethod
    def get_pinyin_ftx(self, city):
        if city == u"北京":
            return ''
        elif city == u"苏州":
            return 'suzhou.'
        elif city == u"太原":
            return 'taiyuan.'
        elif city == u"哈尔滨":
            return 'hrb.'
        elif city == u"西安":
            return 'xian.'
        elif city == u"无锡":
            return 'wuxi.'
        elif city == u"武汉":
            return 'wuhan.'
        elif city == u"南京":
            return 'nanjing.'
        elif city == u"重庆":
            return 'cq.'
        elif city == u"厦门":
            return 'xm.'
        else:
            return self.p.get_initials(city, u'').lower()  + '.'

    @classmethod
    def get_pinyin_lj(self, city):
        if city == u"苏州":
            return 'su'
        elif city == u"重庆":
            return 'cq'
        elif city == u"厦门":
            return 'xm'
        else:
            return self.p.get_initials(city, u'').lower()
