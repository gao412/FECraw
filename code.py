# -*- coding: utf-8 -*-
import requests
import re
import time
import datetime

FElist = ['GBPUSD','USDHKD','GBPHKD','EURUSD','USDCHF','CADUSD','USDJPY','NZDUSD','GBPJPY','GBPCHF','CADJPY']
#FElist = ['GBPUSD','USDHKD','GBPHKD']
url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=USDHKD0&sty=MPICT&st=z&sr=&p=&ps=&cb=callback_fill&js=&token=049db06d2bc9c947062f56de8b3b5648&0"
urllist = []
printdic = []
pricelist = []
t = time.time()
nowTime = lambda:int(round(t * 1000))

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
def Iftaohui(list):
	if list[0] * list[1] - list[2] >= 0.01:
		print(u"可以套汇","收益为",(list[0] * list[1] - list[2]))
	else:
		print(u"再等等")

# 整合信息形成外汇：价格的格式
def Collect(url):
	url = url
	text = GetHTMLtext(url)
	price = GetPrice(text)
	pricelist.append(float(price))
	pat = re.compile(r'[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]')
	a = pat.findall(url)
	printprice = a[0] + ":" + price
	printdic.append(printprice)

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

	# 根据外汇的列表来获得全部的url链接
	for i in FElist:
		pat = re.compile(r'[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]')
		a = pat.findall(url)
		newurl = url.replace(a[0], i)
		urllist.append(newurl)

	# 打印部分
	while True:
		time.sleep(0.5)
		print ("Time:",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		for i in urllist:
			Collect(i)
		for j in printdic:
			print(j)
		Iftaohui(pricelist)
		printdic = []
		pricelist = []
		print("————————————————-——————————————————")

# 启动程序，开始循环
if __name__ == "__main__":
	main()
