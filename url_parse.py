#-*- coding:utf-8 -*-
import PyV8
import re
import time
import requests
from bs4 import BeautifulSoup
import ipdata_output

class UrlParse(object):
	def __init__(self):
		self.ipdataoutput = ipdata_output.IpdataOutput()
		self.__ipurl = ""
		self.__cookies = {}
		self.__headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
		#self.__proxies = {"http":"http://211.151.94.156:80","https":"http://220.248.229.45:3128"}

	def set_ipurl(self,ipurl):
		self.__ipurl = ipurl

	def ipdataparse(self,logobj):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
		requesturl = "http://ipblock.chacuo.net/cdn-cgi/l/chk_jschl"
		#访问首页时，接受服务器发送来的set-cookie中的__cfduif的cookie
		s = requests.session()
		try:
			r = s.get(self.__ipurl,headers = headers,timeout = None)
		except requests.RequestException,e:
			#print e
			logobj.error("first get request is failure!catch exception: %s" % e)
			return -2
		#print r.status_code
		#logobj.debug("first get request statuscode = %d" % r.status_code)	
		#presetcookie = r.headers['set-cookie']
		#sentcookie1st = dict(__cfduid = presetcookie.split(";")[0].split("=")[1])
		sentcookie1st = dict(__cfduid = r.cookies['__cfduid'])
		###########解析页面中的js代码，放到v8中执行##################################
		soup = BeautifulSoup(r.text,'lxml')
		pass_value = soup.find(attrs={'name': 'pass'}).get('value')
		jschl_vc_value = soup.find(attrs={'name': 'jschl_vc'}).get('value')
		#tempstr 存储以下形式的字符串
		#rkJsjKz.KvWrlLpzwg-=!+[]+!![]+!![]+!![]+!![]+!![]+!![];rkJsjKz.KvWrlLpzwg*=+((!+[]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]));rkJsjKz.KvWrlLpzwg+=+((!+[]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]));rkJsjKz.KvWrlLpzwg-=+((!+[]+!![]+!![]+[])+(+!![]))
		tempstr =''
		a = re.search('var s,t,o,p,b,r,e,a,k,i,n,g,f, (\w+)={"(\w+)":(.*)};',r.text)
		dictname, key, value  = a.group(1), a.group(2), a.group(3)
		a = re.search(';(.*;)a\.value',r.text)
		tempstr = dictname +'.'+key + '=' + value +";"+ a.group(1)
		#进入v8
		ctxt = PyV8.JSContext()
		ctxt.enter()
		#拼凑js代码
		oo = "(function(){var "+ dictname + "={'"+ key +"':''};"+tempstr+"return "+dictname+"."+key+";})"
		func = ctxt.eval(str(oo))
		#对应a.value = parseInt(rkJsjKz.KvWrlLpzwg, 10) + t.length中的t.lendth也就是域名的长度
		jschl_answer_value = str(func()+len("ipblock.chacuo.net"))
		payload = {
		    'pass':pass_value,
		    'jschl_vc':jschl_vc_value,
		    'jschl_answer':jschl_answer_value,

		}
		#很关键，需要进行5秒钟休眠
		time.sleep(5)
		#allow_redirects ＝ False不要让requests来自动处理302的跳转
		try:
			r = requests.get(requesturl,allow_redirects=False,cookies = sentcookie1st, headers= headers, params = payload ,timeout = None)
		except requests.RequestException,e:
			logobj.error("second get request is failure!catch exception: %s" % e)
			return -2
		#logobj.debug("second get request statuscode = %d" % r.status_code)
		#print (r.status_code) #log记录状态码
		#获取cf_clearance这个cookie
		presetcookie = r.headers['set-cookie']
		sentcookie2nd = {'cf_clearance':presetcookie.split(";")[0].split("=")[1]}
		#请务必带上Referer header，因为url又会重定向为/view.C_XX
		headers['Referer'] = 'http://ipblock.chacuo.net/view/'+self.__ipurl[-4:]
		#print headers['Referer']
		try:
			r = requests.get(self.__ipurl,cookies = sentcookie2nd, headers = headers)
		except requests.RequestException,e:
			logobj.error("three get request is failure!catch exception: %s" % e)
			return -2	
		#logobj.debug("three get request statuscode = %d" % r.status_code)
		self.__cookies ={'__cfduid':sentcookie1st['__cfduid'],'cf_clearance':sentcookie2nd['cf_clearance']}
		#print (r.status_code) log记录状态码
		status = self.ipdataoutput.ipdatasave(r.content,self.__ipurl,logobj)
		return status
	def ipdatarecevie(self,logobj):
		#请务必带上Referer header，因为url又会重定向为/view.C_XX
		self.__headers['Referer'] = 'http://ipblock.chacuo.net/view/'+self.__ipurl[-4:]
		try:
			r = requests.get(self.__ipurl,cookies = self.__cookies, headers = self.__headers)
		except requests.RequestException,e:
			logobj.error("three get request is failure!catch exception: %s" % e)
			return -1	
		#logobj.debug("some get request statuscode = %d" % r.status_code)
		status = self.ipdataoutput.ipdatasave(r.content,self.__ipurl,logobj)
		return status	