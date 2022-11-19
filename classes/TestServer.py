import sys

from classes import MessageHandler

# This class pretends to be the server. Abstracts the message
# handler from the day-to-day testing.


class TestServer:

    def __init__(self):
        self._msgHandler = MessageHandler.MessageHandler()

    def sendMessage(self, data):
        print("Sending: \""+data+"\"")
        self._msgHandler.sendMessage(data)

    def waitForMessage(self, data):
        print("Waiting for: \""+data+"\"")
        if (self._msgHandler.waitForMessage(data)):
            print("Received: \""+data+"\"")
        else:
            print("Failure waiting for \"" + data + "\"")
            print("Test Failed")
            sys.exit(0)

    def waitForData(self):
        return self._msgHandler.waitForData()
