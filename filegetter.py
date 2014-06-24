# -*- coding: utf-8 -*-

__author__ = 'IWASA'

import os
import codecs

file_list = []
text_list = []


def file_getter(path):
    global file_list
    file_list = os.listdir(path)
    for file_name in file_list:
        #print file_name
        f = codecs.open(os.path.join(path, file_name), 'r', 'utf8', 'ignore')
        text_list.append(f.read())
        f.close()

    return text_list



