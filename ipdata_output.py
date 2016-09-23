#-*- coding:utf-8 -*-
import time
import platform
import datetime
import os
import codecs
from bs4 import BeautifulSoup
class IpdataOutput(object):
	def __init__(self):
		self.path = 'F:/OnlineIpDA/download/'
		self.savefile = None
	def ipdatasave(self,data_content,ipurl,logobj):
		if data_content is None:
			#log 记录解析失败
			logobj.error("save ipdata is failed!catch exception: %s" % e)
			return -1
		soup = BeautifulSoup(data_content,'html.parser',from_encoding='utf-8')
		datavalue = soup.find_all('pre')
		if len(datavalue) == 0:
			#print datavalue
			logobj.error("ipurl=%s,parse pre tag failure,data_content[0:5]=%s." % (ipurl,data_content[0:5]))
			return -1
		#获取当前日期，创建文件夹
		now = datetime.datetime.now()
		strdate = now.strftime("%Y%m%d")
		if os.path.exists(self.path+strdate) == False:
			try:
				os.mkdir(self.path+strdate)
			except WindowsError,e:
				logobj.error("catch exception: %s" % e)
				return -1
		#将IP数据写入磁盘
		for data in datavalue:
			try:
				self.savefile = codecs.open(self.path+strdate+'/'+ipurl[-4:]+'.txt','wb','utf-8')
				#print 'file open save'
				if platform.system() == "Windows":
					self.savefile.write((data.get_text().strip('\r\n')))
				elif platform.system() == "Linux":
					self.savefile.write((data.get_text().strip('\n')))
				else:#for mac os
					self.savefile.write((data.get_text().strip('\r')))
			except IOError,e:
				logobj.error("save ipdata is failed!catch exception: %s" % e)		
			finally:
				if self.savefile:
					self.savefile.close()
		return 0
