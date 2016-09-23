#-*- coding:utf-8 -*-
import logging
import sys
class LogRecord(object):
	def __init__(self):
		self.mylogger = logging.getLogger('iplog')
		self.mylogger.setLevel(logging.WARNING)
		#创建一个handler,用于写入日志文件
		self.fn = logging.FileHandler(sys.path[0]+'/iplog.log','a')
		#定义handler的输出格式formatter
		self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s')
		#定义handler的输出格式
		self.fn.setFormatter(self.formatter)
		#给mylogger添加handler
		self.mylogger.addHandler(self.fn)

	def GetLogObj(self):
		return self.mylogger