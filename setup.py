# -*- coding: utf-8 -*-

__author__ = 'IWASA'

from distutils.core import setup
import py2exe

option = {
    "compressed": 1,
    "optimize": 2,
    "bundle_files": 3,
    "includes": ["tweepy"]
}

setup(options={"py2exe": option},
      console=[{"script": "timelineviewer.py"}],
      zipfile=None
      )