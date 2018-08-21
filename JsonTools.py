#!/usr/bin/python3
#-*-coding:utf-8 -*-
import json
def jsonString2Dict(jsonstr):
    return json.loads(jsonstr)
def dict2String(dict):
    return json.dumps(dict)