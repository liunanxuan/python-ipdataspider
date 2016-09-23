#-*- coding:utf-8 -*-
import sys
import spiders_main
spidersmain = spiders_main.SpidersMain()
urlpath = sys.path[0]+'/'+"ip_url.txt"
spidersmain.spidersipdata(urlpath)