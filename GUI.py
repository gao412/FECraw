# -*- coding: utf-8 -*-
import requests
import re
import time
import datetime
import threading
import tkinter
import pandas as pd

root = tkinter.Tk()
root.title('外汇小工具————James.Gao')
root.resizable(1,1)
vartext_time = tkinter.StringVar()
vartext_GBPUSD = tkinter.StringVar()
vartext_USDHKD = tkinter.StringVar()
vartext_GBPHKD = tkinter.StringVar()
vartext_EURUSD = tkinter.StringVar()
vartext_USDCHF = tkinter.StringVar()
vartext_CADUSD = tkinter.StringVar()
vartext_USDJPY = tkinter.StringVar()
vartext_EURJPY = tkinter.StringVar()
vartext_GBPJPY = tkinter.StringVar()
vartext_GBPCHF = tkinter.StringVar()
vartext_CADJPY = tkinter.StringVar()
vartext_taohui1 = tkinter.StringVar()
vartext_taohui2 = tkinter.StringVar()
vartext_taohui3 = tkinter.StringVar()
vartext_taohui4 = tkinter.StringVar()
vartext_taohui5 = tkinter.StringVar()
vartext_foreGBPUSD = tkinter.StringVar()
vartext_foreUSDHKD = tkinter.StringVar()
vartext_foreGBPHKD = tkinter.StringVar()
vartext_foreEURUSD = tkinter.StringVar()
vartext_foreUSDCHF = tkinter.StringVar()
vartext_foreCADUSD = tkinter.StringVar()
vartext_foreUSDJPY = tkinter.StringVar()
vartext_foreEURJPY = tkinter.StringVar()
vartext_foreGBPJPY = tkinter.StringVar()
vartext_foreGBPCHF = tkinter.StringVar()
vartext_foreCADJPY = tkinter.StringVar()

GBPUSDlist = []
USDHKDlist = []
GBPHKDlist = []
EURUSDlist = []
USDCHFlist = []
CADUSDlist = []
USDJPYlist = []
EURJPYlist = []
GBPJPYlist = []
GBPCHFlist = []
CADJPYlist = []

FElist = ['GBPUSD','USDHKD','GBPHKD','EURUSD','USDCHF','CADUSD','USDJPY','EURJPY','GBPJPY','GBPCHF','CADJPY']
url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=USDHKD0&sty=MPICT&st=z&sr=&p=&ps=&cb=callback_fill&js=&token=049db06d2bc9c947062f56de8b3b5648&0"
urllist = []
printdic = {}
pricelist = []
taohui = []
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
	# global taohui
	if float(dict['GBPUSD']) * float(dict['USDHKD']) - float(dict['GBPHKD']) >= 0.0001:
		vartext_taohui1.set((u"GBP、USD、HKD可以套汇","收益为",round((float(dict['GBPUSD']) * float(dict['USDHKD']) - float(dict['GBPHKD'])), 5)))
	else:
		vartext_taohui1.set((u"GBP、USD、HKD不能套汇，再等等"))

	if float(dict['GBPUSD']) * float(dict['USDJPY']) - float(dict['GBPJPY']) >= 0.0001:
		vartext_taohui2.set((u"GBP、USD、JPY可以套汇","收益为",round((float(dict['GBPUSD']) * float(dict['USDJPY']) - float(dict['GBPJPY'])), 5)))
	else:
		vartext_taohui2.set((u"GBP、USD、JPY不能套汇，再等等"))

	if float(dict['GBPUSD']) * float(dict['USDCHF']) - float(dict['GBPCHF']) >= 0.0001:
		vartext_taohui3.set((u"GBP、USD、CHF可以套汇","收益为",round((float(dict['GBPUSD']) * float(dict['USDCHF']) - float(dict['GBPCHF'])), 5)))
	else:
		vartext_taohui3.set((u"GBP、USD、CHF不能套汇，再等等"))

	if float(dict['CADUSD']) * float(dict['USDJPY']) - float(dict['CADJPY']) >= 0.0001:
		vartext_taohui4.set((u"CAD、USD、JPY可以套汇","收益为",round((float(dict['CADUSD']) * float(dict['USDJPY']) - float(dict['CADJPY'])), 5)))
	else:
		vartext_taohui4.set((u"CAD、USD、JPY不能套汇，再等等"))

	if float(dict['EURUSD']) * float(dict['USDJPY']) - float(dict['EURJPY']) >= 0.0001:
		vartext_taohui5.set((u"EUR、USD、JPY可以套汇","收益为",round((float(dict['EURUSD']) * float(dict['USDJPY']) - float(dict['EURJPY'])), 5)))
	else:
		vartext_taohui5.set((u"EUR、USD、JPY不能套汇，再等等"))

# 整合信息形成外汇：价格的格式
def Collect(url1):
	url = url1
	text = GetHTMLtext(url)
	price = GetPrice(text)
	# pricelist.append(float(price))
	pat = re.compile(r'[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]')
	a = pat.findall(url)
	dictoadd = {a[0]: price}
	printdic.update(dictoadd)


# 采用差分指数平滑法进行预测
def forecast(list):
	n = len(list)
	if n == 1:
		return list[0]
	else:
		dyhat = [0] * (n + 1) # 先产生一个0列表
		yhat = [0] * (n + 1) # 先产生一个0列表
		alpha = 0.4 # 设置阿尔法值
		yt = pd.Series(list) # 将列表里的数存储为序列
		dyt = yt.diff(1) # 求序列的一阶差分
		dyt[0] = 0 # 差分序列加零补位
		dyhat[1] = dyt[1] # 指数平滑值得初始值
		yhat[0] = list[0]
		for i in range(1, n):
			dyhat[i + 1] = alpha * dyt[i] + (1 - alpha) * dyhat[i]

		for i in range(0, n):
			yhat[i + 1] = dyhat[i + 1] + yt[i]

		return round(yhat[n], 4)

# 定义主函数：参数是可以设置计时器
def start():
	# 全局化变量
	global printdic
	global pricelist
	global urllist
	# 根据外汇的列表来获得全部的url链接
	for i in FElist:
		pat = re.compile(r'[A-Z][A-Z][A-Z][A-Z][A-Z][A-Z]')
		a = pat.findall(url)
		newurl = url.replace(a[0], i)
		urllist.append(newurl)

	# 多线程快速下载外汇数据并存储在字典中
#while True:
	thread = []
		# print ("Time:",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	
	for i in urllist:
		t = threading.Thread(target = Collect, args = (i,))
		thread.append(t)

	for i in range(0,11):
		thread[i].start()

	for i in range(0,11):
		thread[i].join()
	
	GBPUSDlist.append(float(printdic['GBPUSD']))
	USDHKDlist.append(float(printdic['USDHKD']))
	GBPHKDlist.append(float(printdic['GBPHKD']))
	EURUSDlist.append(float(printdic['EURUSD']))
	USDCHFlist.append(float(printdic['USDCHF']))
	CADUSDlist.append(float(printdic['CADUSD']))
	USDJPYlist.append(float(printdic['USDJPY']))
	EURJPYlist.append(float(printdic['EURJPY']))
	GBPJPYlist.append(float(printdic['GBPJPY']))
	GBPCHFlist.append(float(printdic['GBPCHF']))
	CADJPYlist.append(float(printdic['CADJPY']))
	#print(GBPUSDlist)
	#print(type(GBPUSDlist))

	vartext_foreGBPUSD.set(str(forecast(GBPUSDlist)))
	vartext_foreUSDHKD.set(str(forecast(USDHKDlist)))
	vartext_foreGBPHKD.set(str(forecast(GBPHKDlist)))
	vartext_foreEURUSD.set(str(forecast(EURUSDlist)))
	vartext_foreUSDCHF.set(str(forecast(USDCHFlist)))
	vartext_foreCADUSD.set(str(forecast(CADUSDlist)))
	vartext_foreUSDJPY.set(str(forecast(USDJPYlist)))
	vartext_foreEURJPY.set(str(forecast(EURJPYlist)))
	vartext_foreGBPJPY.set(str(forecast(GBPJPYlist)))
	vartext_foreGBPCHF.set(str(forecast(GBPCHFlist)))
	vartext_foreCADJPY.set(str(forecast(CADJPYlist)))

	#for i in urllist:
	#	Collect(i)
	# 将字典中的值放在动态标签中
	vartext_time.set(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	vartext_GBPUSD.set(printdic['GBPUSD'])
	vartext_USDHKD.set(printdic['USDHKD'])
	vartext_GBPHKD.set(printdic['GBPHKD'])
	vartext_EURUSD.set(printdic['EURUSD'])
	vartext_USDCHF.set(printdic['USDCHF'])
	vartext_CADUSD.set(printdic['CADUSD'])
	vartext_USDJPY.set(printdic['USDJPY'])
	vartext_EURJPY.set(printdic['EURJPY'])
	vartext_GBPJPY.set(printdic['GBPJPY'])
	vartext_GBPCHF.set(printdic['GBPCHF'])
	vartext_CADJPY.set(printdic['CADJPY'])
	Iftaohui(printdic)
	# printdic = {} # 我感觉可以不用重置这个字典，因为update方法可以直接按照键来更新值
		# pricelist = []
		#time.sleep(0.5)

# 定义一个可以带计时器的启动程序

def autostart():
	global Entry_time
	second = int(Entry_time.get())
	start()
	root.after(second * 1000, autostart)

# 布局
def buju(root):
	global Entry_time
	Button_start = tkinter.Button(root, text = "Refresh", width = 10, height = 1, fg = "blue", command = start)
	Button_start.grid(row = 0, column = 0)
	Button_autostart = tkinter.Button(root, text = "AutoRefresh", width = 10, height = 1, fg = "red", command = autostart)
	Button_autostart.grid(row = 0, column = 1)
	label_settime = tkinter.Label(root, text = "Set Time Interval", width = 20, height = 1, bg = 'white')
	label_settime.grid(row = 0, column = 2)
	Entry_time = tkinter.Entry(root, width = 10)
	Entry_time.grid(row = 0, column = 3)
	label_time = tkinter.Label(root, width = 30, height = 1, bg = 'white', textvariable = vartext_time)
	label_time.grid(row = 1, column = 1, columnspan = 2)

	# 这部分是固定的标签，带下划线的是固定标签
	label_ExName = tkinter.Label(root, text = "Ex.Name", width = 10, height = 1, bg = 'white')
	label_ExName.grid(row = 2, column = 0)
	label_price = tkinter.Label(root, text = "Price", width = 10, height = 1, bg = 'white')
	label_price.grid(row = 2, column = 1)
	label_taohui = tkinter.Label(root, text = "Arbitrage", width = 10, height = 1, bg = 'white')
	label_taohui.grid(row = 2, column = 3)
	label_yuce = tkinter.Label(root, text = "Forecast", width = 10, height = 1, bg = 'white')
	label_yuce.grid(row = 2, column = 2)
	label_GBPUSD = tkinter.Label(root, text = "GBPUSD", width = 10, height = 1, bg = 'white')
	label_USDHKD = tkinter.Label(root, text = "USDHKD", width = 10, height = 1, bg = 'white')
	label_GBPHKD = tkinter.Label(root, text = "GBPHKD", width = 10, height = 1, bg = 'white')
	label_EURUSD = tkinter.Label(root, text = "EURUSD", width = 10, height = 1, bg = 'white')
	label_USDCHF = tkinter.Label(root, text = "USDCHF", width = 10, height = 1, bg = 'white')
	label_CADUSD = tkinter.Label(root, text = "CADUSD", width = 10, height = 1, bg = 'white')
	label_USDJPY = tkinter.Label(root, text = "USDJPY", width = 10, height = 1, bg = 'white')
	label_EURJPY = tkinter.Label(root, text = "EURJPY", width = 10, height = 1, bg = 'white')
	label_GBPJPY = tkinter.Label(root, text = "GBPJPY", width = 10, height = 1, bg = 'white')
	label_GBPCHF = tkinter.Label(root, text = "GBPCHF", width = 10, height = 1, bg = 'white')
	label_CADJPY = tkinter.Label(root, text = "CADJPY", width = 10, height = 1, bg = 'white')
	label_GBPUSD.grid(row = 3, column = 0)
	label_USDHKD.grid(row = 4, column = 0)
	label_GBPHKD.grid(row = 5, column = 0)
	label_EURUSD.grid(row = 6, column = 0)
	label_USDCHF.grid(row = 7, column = 0)
	label_CADUSD.grid(row = 8, column = 0)
	label_USDJPY.grid(row = 9, column = 0)
	label_EURJPY.grid(row = 10, column = 0)
	label_GBPJPY.grid(row = 11, column = 0)
	label_GBPCHF.grid(row = 12, column = 0)
	label_CADJPY.grid(row = 13, column = 0)

	# 这部分是会变动的标签，不带下划线的是可变标签
	# 这一组是价格的标签
	labelGBPUSD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_GBPUSD)
	labelUSDHKD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_USDHKD)
	labelGBPHKD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_GBPHKD)
	labelEURUSD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_EURUSD)
	labelUSDCHF = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_USDCHF)
	labelCADUSD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_CADUSD)
	labelUSDJPY = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_USDJPY)
	labelEURJPY = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_EURJPY)
	labelGBPJPY = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_GBPJPY)
	labelGBPCHF = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_GBPCHF)
	labelCADJPY = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_CADJPY)
	labelGBPUSD.grid(row = 3, column = 1)
	labelUSDHKD.grid(row = 4, column = 1)
	labelGBPHKD.grid(row = 5, column = 1)
	labelEURUSD.grid(row = 6, column = 1)
	labelUSDCHF.grid(row = 7, column = 1)
	labelCADUSD.grid(row = 8, column = 1)
	labelUSDJPY.grid(row = 9, column = 1)
	labelEURJPY.grid(row = 10, column = 1)
	labelGBPJPY.grid(row = 11, column = 1)
	labelGBPCHF.grid(row = 12, column = 1)
	labelCADJPY.grid(row = 13, column = 1)

	# 这一组是能否套汇
	labeltaohui1 = tkinter.Label(root, width = 30, height = 1, bg = 'white', anchor = 'sw', textvariable = vartext_taohui1)
	labeltaohui2 = tkinter.Label(root, width = 30, height = 1, bg = 'white', anchor = 'sw', textvariable = vartext_taohui2)
	labeltaohui3 = tkinter.Label(root, width = 30, height = 1, bg = 'white', anchor = 'sw', textvariable = vartext_taohui3)
	labeltaohui4 = tkinter.Label(root, width = 30, height = 1, bg = 'white', anchor = 'sw', textvariable = vartext_taohui4)
	labeltaohui5 = tkinter.Label(root, width = 30, height = 1, bg = 'white', anchor = 'sw', textvariable = vartext_taohui5)
	labeltaohui1.grid(row = 3, column = 3, columnspan = 3)
	labeltaohui2.grid(row = 4, column = 3, columnspan = 3)
	labeltaohui3.grid(row = 5, column = 3, columnspan = 3)
	labeltaohui4.grid(row = 6, column = 3, columnspan = 3)
	labeltaohui5.grid(row = 7, column = 3, columnspan = 3)

	# 这一组是预测数据
	labelyuceGBPUSD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreGBPUSD)
	labelyuceUSDHKD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreUSDHKD)
	labelyuceGBPHKD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreGBPHKD)
	labelyuceEURUSD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreEURUSD)
	labelyuceUSDCHF = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreUSDCHF)
	labelyuceCADUSD = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreCADUSD)
	labelyuceUSDJPY = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreUSDJPY)
	labelyuceEURJPY = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreEURJPY)
	labelyuceGBPJPY = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreGBPJPY)
	labelyuceGBPCHF = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreGBPCHF)
	labelyuceCADJPY = tkinter.Label(root, width = 10, height = 1, bg = 'white', textvariable = vartext_foreCADJPY)

	labelyuceGBPUSD.grid(row = 3, column = 2)
	labelyuceUSDHKD.grid(row = 4, column = 2)
	labelyuceGBPHKD.grid(row = 5, column = 2)
	labelyuceEURUSD.grid(row = 6, column = 2)
	labelyuceUSDCHF.grid(row = 7, column = 2)
	labelyuceCADUSD.grid(row = 8, column = 2)
	labelyuceUSDJPY.grid(row = 9, column = 2)
	labelyuceEURJPY.grid(row = 10, column = 2)
	labelyuceGBPJPY.grid(row = 11, column = 2)
	labelyuceGBPCHF.grid(row = 12, column = 2)
	labelyuceCADJPY.grid(row = 13, column = 2)

# 菜单，我也装个b
def caidan(root):
	menu = tkinter.Menu(root)
	submenu1 = tkinter.Menu(menu, tearoff = 0)
	menu.add_cascade(label='查看', menu = submenu1)
	submenu2 = tkinter.Menu(menu, tearoff = 0)
	submenu2.add_command(label = '复制')
	submenu2.add_command(label = '粘贴')
	menu.add_cascade(label= '编辑', menu = submenu2)
	submenu = tkinter.Menu(menu, tearoff = 0)
	submenu.add_command(label = '查看帮助')
	submenu.add_separator()
	submenu.add_command(label = '关于计算机')
	menu.add_cascade(label= '帮助', menu = submenu)
	root.config(menu = menu)


# 启动程序，开始循环
buju(root)
caidan(root)
root.mainloop()

