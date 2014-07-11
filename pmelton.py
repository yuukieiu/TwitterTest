# -*- coding: utf-8 -*-

__author__ = 'IWASA'

import tweepy as tp                 # TwitterAPI用ライブラリ
import datetime as dt               # 日付取る用ライブラリ
import wx                           # wxPython
import webbrowser                   # 認証ページ開く
import os
import threading                    # マルチスレッド


class MeltonMain(tp.StreamListener, threading.Thread):
    def __init__(self):
        self.frame = MeltonFrame()
        self.twitter = MeltonAPI()
        # イベントハンドラバインド
        self.frame.top_ctrl.tweet_btn.Bind(wx.EVT_BUTTON, self.tweet_post)
        #threading.Thread.__init__(self)
        #self.start()
        self.frame.MainLoop()

    def run(self):
        stream = tp.Stream(self.twitter.auth, MeltonMain(), secure=True)
        stream.userstream()

    def on_status(self, status):
        # TLにツイートを追加
        pass

    def tweet_post(self, event):
        text = self.frame.top_ctrl.text.GetValue()
        self.twitter.melton_tweet(text)
        self.frame.top_ctrl.text.SetValue("")


class MeltonFrame(wx.App):
    def OnInit(self):
        self.frame = wx.Frame(None, wx.ID_ANY, 'Melton for Python ver.Garland', size=(600, 400))
        self.top_ctrl = TopCtrl(self.frame)
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.layout.Add(self.top_ctrl, flag=wx.GROW)
        self.frame.Show()
        return True


class TopCtrl(wx.Panel):
    def __init__(self, frame):
        wx.Panel.__init__(self, frame, wx.ID_ANY)

        self.layout = wx.BoxSizer(wx.HORIZONTAL)

        # アイコンセット
        self.image = wx.Bitmap('Meltonicon.png')
        self.icon = wx.StaticBitmap(self, -1, self.image, (0, 0))
        self.layout.Add(self.icon, flag=wx.GROW)
        # テキストボックスセット
        self.text = wx.TextCtrl(self, wx.ID_ANY)
        self.layout.Add(self.text, flag=wx.GROW)
        # ツイートボタンセット
        self.tweet_btn = wx.Button(self, wx.ID_ANY)
        self.tweet_btn.SetLabel('Tweet!')
        self.tweet_btn.SetToolTipString(u'ツイートします')
        self.layout.Add(self.tweet_btn, flag=wx.GROW)

        self.SetSizer(self.layout)


class TLCtrl(wx.Panel):
    # タイムライン用クラス
    pass


class ToolsCtrl(wx.Panel):
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
    melton = MeltonMain()