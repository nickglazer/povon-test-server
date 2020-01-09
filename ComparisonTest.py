# This test will mimic normal operation of the Povon Power Monitor
# It will run for an indefinite amount of time collecting data and write
# to a csv file.
import os
import time
import sys

from classes.TestServer import *

time = time.strftime("%Y_%m_%d")+"__"+time.strftime("%H_%M_%S")

try:
    if sys.argv[1] == 'pi':
        os.makedirs("/home/pi/Desktop/logs", exist_ok=True)
        names = ["/home/pi/Desktop/logs/trackTotal.csv", "/home/pi/Desktop/logs/trackAll.csv",
            "/home/pi/Desktop/logs/"+time+"_sum.csv", "/home/pi/Desktop/logs/"+time+"_total.csv"]
    else:
        os.makedirs("/Users/Nicholas/Desktop/logs", exist_ok=True)
        names = ["/Users/Nicholas/Desktop/logs/trackTotal.csv", "/Users/Nicholas/Desktop/logs/trackAll.csv",
            "/Users/Nicholas/Desktop/logs/"+time+"_sum.csv", "/Users/Nicholas/Desktop/logs/"+time+"_total.csv"]
except:
    raise

f = open(names[0],'w')
f.close()
g = open(names[1],'w')
g.close()

h = open(names[2],'w')
h.close()
i = open(names[3],'w')
i.close()

testServer = TestServer()

hold = 0
holdList = []
while True:
    #get message, parsed, from message handler from test server
    dataString = testServer.waitForData()
    
    if dataString == None:
        continue
    
    # total
    if dataString['mac'] == [24, 254, 52, 243, 175, 28]:
        holdList = dataString['data'][-5:]
        hold = sum(holdList)
        lst = sorted(dataString['data'],reverse=True)
        total = sum(lst[1:3])/10
        
        f = open(names[0],'a')
        f.write(str(total))
        f.close()
        
        i = open(names[3]",'a')
        i.write(str(sum(lst[1:3])/10)+'\n')
        i.close()
    elif dataString['mac'] == [24, 254, 52, 243, 174, 152]:
        summa = (sum(dataString['data'])+hold)/10
        
        g = open(names[1],'a')
        g.write(",".join([str(x/10) for x in dataString['data']+holdList])+'\n')
        g.close()
        
        h = open(names[2],'a')
        h.write(str(summa))
        h.close()
