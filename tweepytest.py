# -*- coding: utf-8 -*-

__author__ = 'IWASA'


import tweepy as tp                 # TwitterAPI用ライブラリ
import filegetter as fg             # ファイル取得用ライブラリ
import datetime as dt               # 日付取る用ライブラリ
import random as rnd                # 乱数発生用ライブラリ
import sys                          # 残り2つはよくわからない
import codecs

# 各種キー
consumer_key = "h9MPYtJFCOFW05IzCvEQ"
consumer_secret = "3DbapHU8WGcQOT4quroKVljQd6zAuA02pvmHOLn2iJM"
access_token = "267076030-guPLUN6R04rBzCXSvSFZJYVVoDgFeidjDfr1t4cO"
access_token_secret = "HMlEFRAQNiB5QbO1VAX7g0hDrVlmsonN60Le6pgBKQY"

test_num = 0                    # post試行回数


def certificate(ck, cs, at, ats):       # OAuth認証
    auth = tp.OAuthHandler(ck, cs)
    auth.set_access_token(at, ats)
    return tp.API(
        auth_handler=auth,
        api_root='/1.1',
        secure=True
    )


def auto_certificate():                 # 直接やってもいい気もする
    return certificate(consumer_key, consumer_secret, access_token, access_token_secret)


def random_tweet(api):
    global test_num, text_list
    if test_num >= len(text_list):
        print u'postに失敗しすぎました．無念'
        api.update_status("ラッキーナンバー：" + str(rnd.randint(0,9999)))
        return

    test_num += 1
    # 乱数発生
    post_num = rnd.randint(0, len(text_list) - 1)
    try:
        api.update_status(text_list[post_num])
    except tp.error.TweepError, te:
        print u'postに失敗しました．原因は次のとおりです：'
        print te
        print u'失敗したpost内容：'
        print text_list[post_num]
        print u'乱数を再生成します...'
        random_tweet(api)
        return
    else:
        print u'postに成功しました．成功したpost内容：'
        print text_list[post_num]
        return


# これやるとこのあとのprintは全部utf8になるんだって
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

# APIに接続
api1 = auto_certificate()
# ファイルから読み込む
text_list = fg.file_getter('C:/Users/IWASA/PycharmProjects/TwitterTest/tweetdata')
# 現在時刻（OSの）
print str(dt.datetime.now()) + u'のpost:'
random_tweet(api1)
