#-*- coding:utf-8 -*-
class statistic(object):
    def __init__(self,*args,**kw):
        self._totalNum = 0
        self._totalNumBad = 0
        self._totalNumGood = 0
        self._totalQueueNum = 0
        self._totalMW200HNum = 0
        self._totalTestNum = 0

    @property
    def totalTestNum(self):
        return self._totalTestNum
    @totalTestNum.setter
    def totalTestNum(self,value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        else:
            self._totalTestNum = value
    @property
    def totalMW200HNum(self):
        return self._totalMW200HNum
    @totalMW200HNum.setter
    def totalMW200HNum(self,value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        else:
            self._totalMW200HNum = value
    @property
    def totalNum(self):
        return self._totalNum
    @totalNum.setter
    def totalNum(self,value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        else:
            self._totalNum = value

    @property
    def totalNumBad(self):
        return self._totalNumBad
    @totalNumBad.setter

    def totalNumBad(self,value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        else:
            self._totalNumBad = value
    @property
    def totalNumGood(self):
        return self._totalNumGood
    @totalNumGood.setter
    def totalNumGood(self,value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        else:
            self._totalNumGood = value
    @property
    def totalQueueNum(self):
        return self._totalQueueNum
    @totalQueueNum.setter

    def totalQueueNum(self,value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        else:
            self._totalQueueNum = value

exception = ['make','by','joyotime','tec','rom','team','!']

