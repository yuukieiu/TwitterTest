# -*- coding: utf-8 -*-

__author__ = 'IWASA'


import tweepy as tp
import filegetter as fg
import datetime as dt
import random as rnd


consumer_key = "h9MPYtJFCOFW05IzCvEQ"
consumer_secret = "3DbapHU8WGcQOT4quroKVljQd6zAuA02pvmHOLn2iJM"
access_token = "267076030-guPLUN6R04rBzCXSvSFZJYVVoDgFeidjDfr1t4cO"
access_token_secret = "HMlEFRAQNiB5QbO1VAX7g0hDrVlmsonN60Le6pgBKQY"


def certificate(ck, cs, at, ats):
    auth = tp.OAuthHandler(ck, cs)
    auth.set_access_token(at, ats)
    return tp.API(auth_handler=auth, api_root='/1.1', secure=True)


def auto_certificate():
    return certificate(consumer_key, consumer_secret, access_token, access_token_secret)


api = auto_certificate()
text_list = fg.file_getter()
post_id = rnd.randint(0, 9999)

print str(dt.datetime.today()) + "のポスト:"
for text in text_list:
    result = api.update_status(text + "post_id:" + post_id)
    print text.encode('utf-8')