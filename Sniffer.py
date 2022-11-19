from classes.MessageHandler import *
from classes.TestServer import *

msgHandler = MessageHandler.MessageHandler()

# Sniffs messages infinitely until interrupted.
while True:
    msgHandler.sniffMessages()
