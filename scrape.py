 #!/bin/python
 
from bs4 import BeautifulSoup
from lxml import etree
import requests
import re
import urllib2
import threading
import datetime
import time


vlccl_home_team = "GIANTS BLUE"
pcl_home_team = "Mavericks"
threads = []

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]


# PCL data ___________________________________________________________________________
r1 = requests.get("https://www.cricclubs.com/PCL/teamSchedule.do?teamId=115&clubId=117", verify=False)

data = r1.text
soup = BeautifulSoup(data, "lxml")
#print soup.find("td", text="League").find_next_sibling("td").next
table = soup.find('table', attrs={'class': 'sortable table'})

rows = table.findAll("tr")
flag = 1
pcl_list1 = []
for tr in rows:
	if flag:
		flag = 0
		continue
	td_list = tr.find_all("td")
	pcl_list1.append(td_list[1].next)
	pcl_list1.append(td_list[2].next)
	pcl_list1.append(td_list[3].next)
	pcl_list1.append(td_list[4].next)

print pcl_list1
pcl_list2 = []
for row in table.findAll('a'):
	pcl_list2.append(row.text)

print pcl_list2

# LCCL data ___________________________________________________________________________
r1 = requests.get("https://cricclubs.com/vlccl/fixtures.do?league=36&teamId=712&clubId=146", verify=False)

data1 = r1.text
soup1 = BeautifulSoup(data1, "lxml")
table = soup1.find('table', attrs={'class': 'sortable table'})

#print soup1.prettify()
rows = table.findAll("tr")
flag = 1
lccl_list1 = []
for tr in rows:
	if flag:
		flag = 0
		continue
	td_list = tr.find_all("td")
	lccl_list1.append(td_list[1].next)
	lccl_list1.append(td_list[2].next)
	lccl_list1.append(td_list[3].next)
	lccl_list1.append(td_list[4].next)

print lccl_list1

lccl_list2 = []
for row in table.findAll('a'):
	lccl_list2.append(row.text)

print lccl_list2

# end of LCCL__________________________________________________________________________

def get_date_time(s, t):
	date1 = datetime.datetime.today()
	date2 = (datetime.datetime(int(s[6:]), int(s[:2]), int(s[3:5]), int(t[:2]), int(t[3:5])))
	if date1 < date2:
		return 1
	else:
		return 0

def game_day_fetch_score():
	return


def monitor(e):
	"""threader worker function"""
	while True:
		print "Monitor thread started"
		print "First Game :",  lccl_list1[2], pcl_list1[2]
		event_is_set = e.wait()
		if get_date_time(lccl_list1[2], lccl_list1[3]):
			print "Hello, Sarath!! you don't have a game in LCCL today"
		else:
			game_day_fetch_score()
			print "Game bro!!"
		e.clear()

e = threading.Event()
t = threading.Thread(target=monitor,args=(e,))
threads.append(t)
t.start()

while True:
	time.sleep(1)
	print "Main loop set the the flag.."
	e.set()


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
