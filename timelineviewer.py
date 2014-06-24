# -*- coding: utf-8 -*-

__author__ = 'IWASA'

import tweepy as tp                 # TwitterAPI用ライブラリ
import datetime as dt               # 日付取る用ライブラリ
import wx                           # wxPython
import webbrowser
import os


def get_oauth():
    consumer_key = "h9MPYtJFCOFW05IzCvEQ"
    consumer_secret = "3DbapHU8WGcQOT4quroKVljQd6zAuA02pvmHOLn2iJM"
    #access_token = "267076030-guPLUN6R04rBzCXSvSFZJYVVoDgFeidjDfr1t4cO"
    #access_token_secret = "HMlEFRAQNiB5QbO1VAX7g0hDrVlmsonN60Le6pgBKQY"

    if os.path.exists('accesstoken.bat'):                   # accesstoken保存済みなら読み込み
        f = open('accesstoken.bat', 'r')
        access_token = f.readline().replace('\n', '')
        access_token_secret = f.readline().replace('\n', '')
        f.close()
        auth = tp.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
    else:                                                   # accesstoken未保存ならaccesstoken取ってきて保存
        auth = tp.OAuthHandler(consumer_key, consumer_secret)
        auth.secure = True
        auth_url = auth.get_authorization_url().replace( "authorize", "authenticate")
        webbrowser.open(auth_url)
        verifier = raw_input("PIN:")
        auth.get_access_token(verifier)
        f = open('accesstoken.bat', 'w')
        f.write(auth.access_token.key + '\n')
        f.write(auth.access_token.secret + '\n')
        f.close()
    return auth


class AbstractedlyListener(tp.StreamListener):
    def on_status(self, status):
        status.created_at += dt.timedelta(hours=9)
        print(u"{text}".format(text=status.text))
        print(u"{name}({screen}) {created} via {src}\n".format(
            name=status.author.name, screen=status.author.screen_name,
            created=status.created_at, src=status.source))


class WindowSample(wx.App):
    def OnInit(self):
        self.auth = get_oauth()
        self.twitter = tp.API(
            auth_handler=self.auth,
            api_root='/1.1',
            secure=True
        )
        self.init_frame()
        return True

    def init_frame(self):
        self.frm_main = wx.Frame(None)
        self.icon =wx.Icon("Meltonicon.png", wx.BITMAP_TYPE_PNG)
        self.frm_main.SetIcon(self.icon)
        self.sizer = wx.BoxSizer()
        self.frm_main.SetSizer(self.sizer)
        self.txt_title = wx.TextCtrl(self.frm_main)
        self.sizer.Add(self.txt_title, 1, wx.TOP)
        self.btn_tweet = wx.Button(self.frm_main)
        self.btn_tweet.SetLabel("Tweet!")
        self.btn_tweet.SetToolTipString(u"ツイートします")
        self.btn_tweet.Bind(wx.EVT_BUTTON, self.click_btn_tweet)
        self.sizer.Add(self.btn_tweet, 0, wx.TOP)
        element_array = ("element_1", "element_2", "element_4", "element_3", "element_5")
        self.listbox = wx.ListBox(self.frm_main, wx.ID_ANY, choices=element_array, style=wx.LB_SINGLE | wx.LB_HSCROLL)
        self.sizer.Add(self.listbox, 0, wx.BOTTOM)
        self.frm_main.SetTitle("Melton for Python version Garland")
        self.frm_main.SetSize((400, 200))
        self.frm_main.Show()

    def click_btn_tweet(self, event):
        self.twitter.update_status(self.txt_title.GetValue())
        self.txt_title.SetValue("")
        pass


if __name__ == '__main__':
    app = WindowSample(False)
    #stream = tp.Stream(auth, AbstractedlyListener(), secure=True)
    #stream.userstream()
    app.MainLoop()
