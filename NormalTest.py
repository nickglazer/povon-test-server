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
        name = "/home/pi/Desktop/logs/"+time+".csv"
    else:
        os.makedirs("/Users/Nicholas/Desktop/logs", exist_ok=True)
        name = "/Users/Nicholas/Desktop/logs/"+time+".csv"
except:
    raise

f = open(name, 'w')
f.close()

testServer = TestServer()

while True:
    # get message, parsed, from message handler from test server
    dataString = testServer.waitForData()

    if dataString == None:
        continue

    f = open(name, 'a')
    f.write(",".join([str(x/10) for x in dataString['data']])+'\n')
    f.close()
