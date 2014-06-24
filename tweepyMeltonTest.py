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


def get_differ(new, old):
    """new にあってold にないものを返す関数"""
    if not isinstance(new, set):
        new = set(new)
    if not isinstance(old, set):
        old = set(old)
    return new.difference(old)


def thanks_follow(new, api):
    """新たにフォローしてくれた人をフォロー"""
    for user in new:
        api.create_friendship(user)
        print(u"新たにフォローしてくれた人：" + str(api.get_user(user).screen_name))
        api.update_status('@' + api.get_user(user).screen_name + u' フォローありがとう！')


def remove(gone, api):
    """リムーブする"""
    for user in gone:
        #pass
        api.destroy_friendship(user)
        print(str(api.get_user(user).screen_name) + u"をリムーブ")


def auto_follow(api):
    friends = api.friends_ids("Dev_Melton")
    followers = api.followers_ids("Dev_Melton")
    print(friends)
    print(followers)
    #old_friends, old_followers = get_friend_ship(FOLLOW)

    # removeされたフォロワー
    gone_followers = get_differ(friends, followers)
    # 新たにフォローしてくれた人
    new_followers = get_differ(followers, friends)

    thanks_follow(new_followers, api)
    remove(gone_followers, api)


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
text_list = fg.file_getter('C:/Users/IWASA/PycharmProjects/TwitterTest/testdata')
# 現在時刻（OSの）
print str(dt.datetime.now()) + u'のpost:'
random_tweet(api1)
print u"フォロー状況："
auto_follow(api1)
