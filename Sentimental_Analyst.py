# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 16:50:53 2018

@author: June
"""
import json

with open('realDonaldTrump/timeline.json', 'r') as f:
    data = json.loads(f.read())