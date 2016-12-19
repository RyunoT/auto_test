#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
test kivy
"""
# Date: 2016/12/17
# Filename: QP3_kivy

from kivy.app import App
from kivy.uix.button import Label
from kivy.config import Config

#Window sizeの設定
Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')

class TestApp(App):
    def build(self):
         self.title = 'Window Sample'
         return Label(text='Hello World')

TestApp().run()


__author__ = 'RyunosukeT'
__date__ = '2016/12/17'
__version__ = '0.1'

