#python3
import requests, json, time

csv = open('data.csv', 'w')		#open  data.csv and erase prev contents
csv.write('Bitcoin Data \n')	#title
csv.write('Date,Time,Price,Action,Profit')	#column titles
csv.close()						#close file

prev_data = 0				#set prev_data to 0
profit = -1					
#set profit to -1 because it will be incrmented if bitcoin's price is greater than 0

def get_data (prev_data, profit): 
	data = requests.get('https://www.bitstamp.net/api/ticker/')	#get data
	
	#use try and except in case data doesn't load or is corrupted for some reason
	try:
		data = json.loads(data.content.decode())	#content of request to json 
	except:
		print('Error getting data')		#print error
		return prev_data, profit 		#return prev_data and Profit

	price = data['last']	#set price to price from request so I don't have to keep typing data['last']
	action = 'Nothing'	#do nothing unless we can make a profit

	if float(price) > (float(prev_data) * 1.0249):
		#actually rate is 1.49% but changed to 2.49% for 1% profit
		prev_data = price	#set prev_price to price so can make next comparision
		profit += 1			#increment the % profit
		if profit > 0:
			action = 'Sell'		#set action to sell because I'll make a 1% profit

	csv = open('data.csv', 'a')		#open file, append mode
	csv.write('\n' + time.strftime('%B %d') + ',')	#date
	csv.write(time.strftime('%H:%M') + ',')			#time
	csv.write('$' + price + ',')					#price
	csv.write(action + ',')							#Sell or don't sell
	csv.write(str(profit) + '%')					#amount of times to sell
	csv.close()										#close

	print(time.strftime('%B %d at %H:%M'))		#print date to console
	print('Price: $' + data['last'])			#print price to console
	print('Profit ' + str(profit) + '%' + '\n')		#print the % profit to console
	return prev_data, profit

while(time.strftime('%B %d at %H:%M') != 'September 26 at 23:38'):	
	#run until desired date and call get_data() every 30 seconds
	prev_data, profit = get_data(prev_data, profit)
	time.sleep(30)