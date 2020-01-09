from classes.MessageHandler import *
from classes.TestServer import *

msgHandler = MessageHandler.MessageHandler()

# Sniffs messages infinitely intil interuppted.
while True:
    msgHandler.sniffMessages()