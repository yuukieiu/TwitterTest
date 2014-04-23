# -*- coding: utf-8 -*-

__author__ = 'IWASA'


import tweepy as tp                 # TwitterAPI用ライブラリ
import filegetter as fg             # ファイル取得用ライブラリ
import datetime as dt               # 日付取る用ライブラリ
import random as rnd                # 乱数発生用ライブラリ
import sys                          # 残り2つはよくわからない
import codecs

# 各種キー
consumer_key = "KFpixxIYa2SkBs5wv5FcEGxMr"
consumer_secret = "7dEnd3b4XQEzWx3ZfPkxszGWHYuBn0Vo90YcgTNn81oWj9rqrR"
access_token = "1466483934-OVtVEvIwHI7zlLmbd0mr0ZWk9n9XzndvGjCdUWT"
access_token_secret = "FHoLHBVNDu7DUp6WAoPl1HzqKEcMtvPNaTy1vCVB7uasb"


def certificate(ck, cs, at, ats):       # OAuth認証
    auth = tp.OAuthHandler(ck, cs)
    auth.set_access_token(at, ats)
    return tp.API(auth_handler=auth, api_root='/1.1', secure=True)


def auto_certificate():                 # 直接やってもいい気もする
    return certificate(consumer_key, consumer_secret, access_token, access_token_secret)

# これやるとこのあとのprintは全部utf8になるんだって
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

# APIに接続
api = auto_certificate()
# ファイルから読み込む
text_list = fg.file_getter()

post_num = rnd.randint(0,len(text_list) - 1)

print str(dt.datetime.now()) + u'のポスト:'
try:
    api.update_status(text_list[post_num])
except tp.error.TweepError, te:
    print u'postに失敗しました．原因は次のとおりです：'
    print te
    print u'失敗したpost内容：'

print text_list[post_num]