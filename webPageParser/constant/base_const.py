#!/usr/bin/env python
# coding: utf-8
import abc
"""常量类，属性不能被修改"""


class Const(object):
    __metaclass__ = abc.ABCMeta

    class ConstError(TypeError):
        pass

    @abc.abstractmethod
    def raise_const_error(self, name):
        """
        this method must be override by subclass
        :return like this:
        raise self.ConstError("Can't change *Const property '%s'" % name)
        """

    def __setattr__(self, name, value):
        saved_name = name
        if not str(name).startswith("_"):
            saved_name = "_" + name
        if saved_name in self.__dict__:
            self.raise_const_error(name)
        self.__dict__[saved_name] = value





