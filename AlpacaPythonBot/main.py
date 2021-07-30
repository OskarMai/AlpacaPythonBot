import time#to add wait time
import numpy as np#to create arrays
import talib#to calculate SMA
import datetime#to get current time
import requests#to send GET requests
import json#for json obj manipulation
from config import *#to get starting parameters


#print(api.get_bars("SPY", TimeFrame.Hour, "2021-02-08","2021-02-08",limit = 100,adjustment='raw').df)
fromdate = datetime.datetime(2020,8,5)
todate = datetime.datetime(2020,8,10)
timeframes = {
	'15Min':15,
	'30Min':30,
	'1H':60,
}
class MeanRev():
	ticker = "SPY"
	def get_holdings(self):#gets amount of shares in ticker name
		try:
			amount = float(api.get_position(ticker).qty)
		except:
			amount = 0 
		return amount

	def get_sma50(self):
		returned_data = api.get_barset(ticker, 'minute',limit = 50)
		closeList = []
		for bar in returned_data[ticker]:
			closeList.append(bar.c)#appending close price to closeList
		closeList = np.array(closeList,dtype=np.float64)
		SMA50 = talib.SMA(closeList,50)[-1]
		return SMA50

	def get_sma150(self):
		returned_data = api.get_barset(ticker, 'minute',limit = 150)
		closeList = []
		for bar in returned_data[ticker]:
			closeList.append(bar.c)#appending close price to closeList
		closeList = np.array(closeList,dtype=np.float64)
		SMA150 = talib.SMA(closeList,150)[-1]
		return SMA150

	def get_price(self):#gets current price on the current ticker set. Change ticker in config.py
		quote = json.loads(requests.get(LATEST_QUOTE,headers=HEADERS).content)['quote']
		bid = quote['bp']
		ask = quote['ap']
		price = (ask+bid)/2
		return price

	def start(self):
		#run program 
		print("Starting Program\n")
		SMA50 = self.get_sma50()
		SMA150 = self.get_sma150()
		print(SMA50,SMA150)
		if(self.get_holdings()>0):
			position=1
		else:
			position=0
		print("Starting Position: "+str(position))
		while(api.get_clock().is_open or True):#only runs the algorithm when the market is open
			SMA50=self.get_sma50()
			SMA150=self.get_sma150()
			if(SMA50<SMA150 and position==0):#buy when sma20 goes below sma50
				print("SMA: ",SMA50,SMA150)
				cash = float(api.get_account().cash)
				quantity=cash/(get_price()/positionSizing)
				order = api.submit_order(ticker,quantity,"buy",type="market",time_in_force="day")
				print("buy order filled at: " +str(datetime.datetime.now()) + " ,position: "+str(position))
				position=1#time to sell
			elif(SMA150<=SMA50 and position==1):
				print("SMA: ",SMA50,SMA150)
				amount = self.get_holdings()#gets current amount of shares in ticker and sells all
				order = api.submit_order(ticker,amount,"sell",type="market",time_in_force="day")
				print("sell order filled at: " +str(datetime.datetime.now()) + " ,position: "+str(position))
				position = 0
			time.sleep(10)# wait a bit before continuing

			#while loop to check if last order was filled
			while(api.list_orders(ticker,limit=1) and api.list_orders(ticker,limit=1)[0].filled_at== None and api.list_orders(ticker,limit=1)[0].canceled_at==None):
				print(api.list_orders(ticker, limit=1)[0])
				print("order not filled yet")
				time.sleep(2)#wait this amount of time before trying again
			print("waiting",SMA50,SMA150)
		print("market is closed\n")
		print("Total Equity: "+api.get_account().equity)
		#end of program
		print("Program Ended")

if __name__=="__main__":
	obj = MeanRev()
	obj.start()
	
	
