#-*- coding:utf-8 -*-
import logging
import sys
class IpUrlManager(object):
	def __init__(self):
		self.newipurls = set()
		self.urlfile = None
		#self.oldipurls = set()

	def Is_has_ipurl(self):
		return len(self.newipurls)!=0

	def get_ipurl(self):
		if len(self.newipurls)!=0:
			new_ipurl = self.newipurls.pop()
			#self.oldipurls.add(new_ipurl)
			return new_ipurl
		else:
			return None

	def download_ipurl(self,destpath,logobj):
		try:
			self.urlfile = open(destpath,'r')
			iter_f = iter(self.urlfile)
			lines = 0
			for ipurl in iter_f:
				lines = lines + 1
				self.newipurls.add((ipurl.rstrip('\r\n')).lstrip('\xef\xbb\xbf'))
			#print self.newipurls
			#log记录读取了多少行IP url
			#print lines
		except IOError,e:
			logobj.error("download ipurl is failed!catch exception: %s" % e)
		finally:
			if self.urlfile:
				self.urlfile.close()	