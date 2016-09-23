#-*- coding:utf-8 -*-
#!/usr/bin/env python2.7
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import url_manager
import url_parse
import log_record
class SpidersMain(object):
	def __init__(self):
		self.urlmangerobj = url_manager.IpUrlManager()
		self.urlparseobj = url_parse.UrlParse()
		self.logrecordobj = log_record.LogRecord()
		self.failurllst = []

	def spidersipdata(self,urlpath):
		logrecord = self.logrecordobj.GetLogObj()
		self.urlmangerobj.download_ipurl(urlpath,logrecord)
		count = 1
		parseflag = 0
		while self.urlmangerobj.Is_has_ipurl():
		 	new_ipurl = self.urlmangerobj.get_ipurl()
		 	#得到一个ipurl，接下来进行下载并解析
		 	print new_ipurl
		 	self.urlparseobj.set_ipurl(new_ipurl)
		 	if count == 1 or parseflag == 1:
		 		status_first = self.urlparseobj.ipdataparse(logrecord)#第一次获得cookies即可
		 		if status_first == -2:
		 			parseflag = 1
		 		else:
		 			parseflag = 0
		 	else:
		 		status_first = self.urlparseobj.ipdatarecevie(logrecord)#直接请求ip url
		 	count = 2
		 	if status_first == -1 or status_first == -2:
		 		logrecord.error("new_ipurl = %s,first download is failed!fail url save." % new_ipurl)
		 		self.failurllst.append(new_ipurl)
		 	else:
		 		logrecord.debug("new_ipurl = %s,download is success!" % new_ipurl)
		 	#	return None
		 		#log 记录 url 下载成功
		#对于失败的list重新request get 
		count = 1		
		while len(self.failurllst)!=0:
			fail_ipurl = self.failurllst.pop()
			print 'fail_ipurl=%s'% fail_ipurl
			self.urlparseobj.set_ipurl(fail_ipurl)
			status_second = self.urlparseobj.ipdataparse(logrecord)
			if status_second == -1 or status_second == -2:
				logrecord.error("for failipurl = %s,count %d download is failed!fail url save." % (fail_ipurl,count))
				count = count + 1
				if count < 235:#total 235 ip data
					self.failurllst.append(fail_ipurl)#循环抓取失败的list

				 		
		logrecord.warning('download ip data is success!')	
'''if __name__ == "__main__":
	import sys
	print sys.path
	spidersmain = SpidersMain()
	print 'hello world'
	urlpath = "ip_url.txt"
	spidersmain.spidersipdata(urlpath)'''
