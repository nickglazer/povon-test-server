import socket
import sys

from classes.TestServer import *

# Fake test made up as proof of concept.
# echo "Polling" | nc -w1 -u 127.0.0.1 5005
testServer = TestServer()

testServer.sendMessage("Hello, World!")

testServer.waitForMessage("PowerOn")

testServer.waitForMessage("Polling")

testServer.waitForMessage("StartReady")
    
print("\nTest Passed")