#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @ 2014-12-26 18:37:24
# author:zhangxian01@baidu.com

from __future__ import division
import sys
from optparse import OptionParser 
from pymongo import MongoClient
import json
from pandas import DataFrame,Series
import ipdb
import time

import json
from pandas import DataFrame , Series
import pandas as pd; import numpy as np
import numpy as np
#注意顺序
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import plot,savefig
import ipdb


def str2sec(s):
    #按照 2914-12-1这种格式组织
    s = s+' 00:00:00'
    sec = time.mktime(time.strptime(s,'%Y-%m-%d %H:%M:%S'))
    return sec 

def Now():
    lt = time.localtime(time.time())
    format_str = '%Y-%m-%d'
    dt = time.strftime(format_str,lt)
    return dt

def sec2str(sec):
    lt = time.localtime(sec)
    format_str = '%Y-%m-%d %H:%M:%S'
    dt = time.strftime(format_str,lt)
    return dt

def compareDateStr(a,b):
    s1 = str2sec(a)
    s2 = str2sec(b)
    if s1 < s2:
        return -1
    elif s1 == s2:
        return 0
    else:
        return 1

if __name__ == "__main__":

    client = MongoClient('10.99.40.33', 27017)
    #维修
    f = open ('weixiu_data.txt','w')
    rec_iter =client.meta_data.yp.find({'__meta.dataid':'3993'})
    buf = list()
    for rec in rec_iter:
        buf.append(rec)
    #print "len",len(buf)
    unknown_brand = 0 
    known_brand = 0
    for rec in buf:
        loc = rec['loc']
        brandlist = list() 
        category = rec['category']
        if  "item" in rec['products']:
            items = rec['products']['item']
            if isinstance(items,dict): 
                t = items
                items=list()
                items.append(t)
            for item in items: 
                if 'brand' in item:
                    r = dict()
                    r['loc'] = loc 
                    r['category'] = category
                    r['name']= item['name']
                    r['brand'] = item['brand']
                    print >>f,json.dumps(r,ensure_ascii=False).encode("UTF-8")
                    #print 'NO', item['titleUrl'],item['title'],item['brand'],item['name'] 
                    if item['brand'] == '':
                        #print 'NO', item['titleUrl'],item['title'],item['brand'],item['name'] 
                        unknown_brand += 1
                    else :
                        #print rec['category'],item['titleUrl'],item['title'],item['brand'],item['name'] 
                        known_brand +=1
                        brandlist.append(item['brand'])
                else:
                    #print "Error:NO brand ",loc
                    pass
        else:
            #print "Error:NO ITEM ",loc
            pass
        #output
        #brand = "$$".join(brandlist)
        #print >>f,loc,json.dumps(category,ensure_ascii=False).encode("UTF-8"),json.dumps(brandlist,ensure_ascii=False).encode("UTF-8") 
    #print 'unknown brand ratio', known_brand,unknown_brand,unknown_brand/(unknown_brand+known_brand)
    f.close()
