#!/usr/bin/env python
# coding: utf-8
from webPageParser.constant.base_const import Const


class __NodeConst(Const):
    
    def raise_const_error(self, name):
        raise self.ConstError("Can't change NodeConst property '%s'" % name)

    def __init__(self):
        self._ROOT = "root"
        self._FIELD = "field"
        self._ATTR = "attr"
        self._EVENTS = "events"
        self._EVENT = "event"
        self._PAGING = "paging"
        self._URL = "url"
        
    @property
    def ROOT(self):
        return self._ROOT

    @property
    def FIELD(self):
        return self._FIELD

    @property
    def ATTR(self):
        return self._ATTR

    @property
    def EVENTS(self):
        return self._EVENTS

    @property
    def EVENT(self):
        return self._EVENT

    @property
    def PAGING(self):
        return self._PAGING

    @property
    def URL(self):
        return self._URL
    

NodeConst = __NodeConst()




