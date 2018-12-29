# -*- coding: utf-8 -*-
import requests
import re
import time
import datetime
import threading
import codecs
import tkinter


FElist = ['GBPUSD','USDHKD','GBPHKD','EURUSD','USDCHF','CADUSD','USDJPY','EURJPY','GBPJPY','GBPCHF','CADJPY']
# FElist = ['GBPUSD','USDHKD','GBPHKD']
url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=USDHKD0&sty=MPICT&st=z&sr=&p=&ps=&cb=callback_fill&js=&token=049db06d2bc9c947062f56de8b3b5648&0"
urllist = []
printdic = {}
pricelist = []

# 定义一个函数让他能爬取网页上的信息
def GetHTMLtext(url): 
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
		return r.text
	except:
		return ""

# 获取价格
def GetPrice(text):
	html = text
	pat = re.compile(r'\d\d.\d\d\d|\d\.\d\d\d\d|\d\d\d\.\d\d') # 匹配文本中的小数
	list_price = pat.findall(html) # 获得所有小数
	price = list_price[2] # 价格是所有小数中的第3个
	return price

# 判断是否存在套汇机会
def Iftaohui(dict):
	if float(dict['GBPUSD']) * float(dict['USDHKD']) - float(dict['GBPHKD']) >= 0.0001:
		print(u"GBP、USD、HKD之间可以套汇","收益为",(float(dict['GBPUSD']) * float(dict['USDHKD']) - float(dict['GBPHKD'])))
	else:
		print(u"GBP、USD、HKD不能套汇，再等等")

	if float(dict['GBPUSD']) * float(dict['USDJPY']) - float(dict['GBPJPY']) >= 0.0001:
		print(u"GBP、USD、JPY之间可以套汇","收益为",(float(dict['GBPUSD']) * float(dict['USDJPY']) - float(dict['GBPJPY'])))
	else:
		print(u"GBP、USD、JPY不能套汇，再等等")

	if float(dict['GBPUSD']) * float(dict['USDCHF']) - float(dict['GBPCHF']) >= 0.0001:
		print(u"GBP、USD、CHF之间可以套汇","收益为",(float(dict['GBPUSD']) * float(dict['USDCHF']) - float(dict['GBPCHF'])))
	else:
		print(u"GBP、USD、CHF不能套汇，再等等")

	if float(dict['CADUSD']) * float(dict['USDJPY']) - float(dict['CADJPY']) >= 0.0001:
		print(u"CAD、USD、JPY之间可以套汇","收益为",(float(dict['CADUSD']) * float(dict['USDJPY']) - float(dict['CADJPY'])))
	else:
		print(u"CAD、USD、JPY再等等")

	if float(dict['EURUSD']) * float(dict['USDJPY']) - float(dict['EURJPY']) >= 0.0001:
		print(u"EUR、USD、JPY之间可以套汇","收益为",(float(dict['EURUSD']) * float(dict['USDJPY']) - float(dict['EURJPY'])))
	else:
		print(u"EUR、USD、JPY再等等")

# 整合信息形成字典
def Collect(url):
	# url = url
	text = GetHTMLtext(url)
	price = GetPrice(text)
	pricelist.append(float(price))
	pat = re.compile(r'[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]')
	a = pat.findall(url)
	dictoadd = {a[0]: price}
	printdic.update(dictoadd)

# 定义主函数

"""
# 根据外汇的列表来获得全部的url链接
for i in FElist:
	pat = re.compile(r'[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]')
	a = pat.findall(url)
	newurl = url.replace(a[0], i)
	urllist.append(newurl)
"""

"""
# 主要部分
if __name__ == '__main__':
	while True:
		time.sleep(0.5)
		print ("Time:",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		for i in urllist:
			main(i)
		for j in printdic:
			print(j)
		Iftaohui(pricelist)
		printdic = []
		pricelist = []
		print("————————————————-——————————————————")
"""



# 定义主函数
def main():
	global printdic
	global pricelist
	#global urllist
	# 根据外汇的列表来获得全部的url链接
	for i in FElist:
		pat = re.compile(r'[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]')
		a = pat.findall(url)
		newurl = url.replace(a[0], i)
		urllist.append(newurl)

	# 打印部分
	while True:
		time.sleep(2)
		thread = []
		print ("Time:",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

		'''
		t1 = threading.Thread(target = Collect, args = (urllist[0],))
		thread.append(t1)
		t2 = threading.Thread(target = Collect, args = (urllist[1],))
		thread.append(t2)
		t3 = threading.Thread(target = Collect, args = (urllist[2],))
		thread.append(t3)
		'''
		for i in urllist:
			t = threading.Thread(target = Collect,
				args = (i,))
			thread.append(t)

		for i in range(0,11):
			thread[i].start()

		for i in range(0,11):
			thread[i].join()

		for key, value in printdic.items():
			print('{key}:{value}'.format(key = key, value = value))

		Iftaohui(printdic)
		printdic = {}
		pricelist = []
		print("——————————————————————————————————————————————————————————")

# 启动程序，开始循环
if __name__ == "__main__":
	main()
