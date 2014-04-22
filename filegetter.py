# -*- coding: utf-8 -*-

__author__ = 'IWASA'

import os
import codecs

file_list = []
text_list = []
file_list = os.listdir("C:/Users/IWASA/PycharmProjects/TwitterTest/tweetdata")


def file_getter():
    for file_name in file_list:
        #print file_name
        f = codecs.open(os.path.join('C:/Users/IWASA/PycharmProjects/TwitterTest/tweetdata', file_name), 'r', 'utf8', 'ignore')
        text_list.append(f.read())
        f.close()

    return text_list



