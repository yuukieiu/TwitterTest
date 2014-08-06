# -*- coding: utf-8 -*-

__author__ = 'IWASA'

import tweepy as tp                 # TwitterAPI用ライブラリ
import datetime as dt               # 日付取る用ライブラリ
#import wx                           # wxPython
import Tkinter as tk                # Tkinter
import ScrolledText as st
from PIL import Image, ImageTk
import webbrowser                   # 認証ページ開く
import os
import threading                    # マルチスレッド


class MeltonMain(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.frame = MeltonFrame(self)
        self.master.title('Melton for Python ver.Garland')
        self.frame.pack()
        self.twitter = MeltonAPI()
        # イベントハンドラバインド

        self.stream = tp.Stream(self.twitter.auth, MyStreamListener(), secure=True)
        #self.stream.userstream()
"""
    def tweet_post(self, event):
        text = self.frame.top_ctrl.text.GetValue()
        self.twitter.melton_tweet(text)
        self.frame.top_ctrl.text.SetValue("")
"""

class MyStreamListener(tp.StreamListener):
    def on_status(self, status):
        # TLにツイートを追加
        status.created_at += dt.timedelta(hours=9)
        print(u"{text}".format(text=status.text))
        print(u"{name}({screen}) {created} via {src}\n".format(
            name=status.author.name, screen=status.author.screen_name,
            created=status.created_at, src=status.source))


class MeltonFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        #self.top_ctrl = TopCtrl(None)
        # topを配置する


class TopCtrl(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # アイコンセット
        self.image = Image.open('Meltonicon.png')
        self.image = ImageTk.PhotoImage(self.image)
        self.icon = tk.Label(self, image=self.image)
        self.icon.pack(side=tk.LEFT)
        # テキストボックスセット
        self.text = st.ScrolledText(self)
        self.text.pack(fill=tk.BOTH, expand=1)
        # ツイートボタンセット
        self.tweet_btn = tk.Button(self, text='Tweet!')
        self.tweet_btn.pack()


class TLCtrl(tk.Frame):
    # タイムライン表示用クラス
    pass


class ToolsCtrl(tk.Frame):
    # 各種ボタン＋ステータス表示
    pass


class MeltonAPI():
    _consumer_key = "h9MPYtJFCOFW05IzCvEQ"
    _consumer_secret = "3DbapHU8WGcQOT4quroKVljQd6zAuA02pvmHOLn2iJM"

    def __init__(self):
        self.auth = self.get_oauth()
        self.api = tp.API(
            auth_handler=self.auth,
            api_root='/1.1',
            secure=True
        )

    def get_oauth(self):
        if os.path.exists('accesstoken.melton'):                   # accesstoken保存済みなら読み込み
            f = open('accesstoken.melton', 'r')
            access_token = f.readline().replace('\n', '')
            access_token_secret = f.readline().replace('\n', '')
            f.close()
            auth = tp.OAuthHandler(self._consumer_key, self._consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
        else:                                                   # accesstoken未保存ならaccesstoken取ってきて保存
            auth = tp.OAuthHandler(self._consumer_key, self._consumer_secret)
            auth.secure = True
            auth_url = auth.get_authorization_url().replace("authorize", "authenticate")
            webbrowser.open(auth_url)
            verifier = raw_input("PIN:")
            auth.get_access_token(verifier)
            f = open('accesstoken.melton', 'w')
            f.write(auth.access_token.key + '\n')
            f.write(auth.access_token.secret + '\n')
            f.close()
        return auth

    def melton_tweet(self, text):
        self.api.update_status(text)

    def melton_retweet(self, status):
        status.retweet()

    def melton_favorite(self, status):
        status.favorite()


if __name__ == '__main__':
    m = MeltonMain()
    m.pack()
    m.stream.userstream()
    m.mainloop()