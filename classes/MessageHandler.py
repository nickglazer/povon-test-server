import socket
import time
import codecs
import sys

# This class handles the receiving, sending, and parsing of messages
# to and from the Povon Power Monitoring for testing.


class MessageHandler:

    # "127.0.0.1" # ip address for coms(127.0.0.1 is loopback)
    _UDP_IP = "192.168.1.3"
    _UDP_PORT = 5000  # port number for coms
    _TIMEOUT = 10  # timeout in seconds
    _DBG_FLG = True  # allows debug print

    def __init__(self):
        self._sock = socket.socket(socket.AF_INET,
                                   socket.SOCK_DGRAM)
        self._sock.bind((MessageHandler._UDP_IP, MessageHandler._UDP_PORT))
        self._sock.settimeout(MessageHandler._TIMEOUT)

    def sendMessage(self, message):
        if MessageHandler._DBG_FLG:
            print("DEBUG:: UDP target IP: ", MessageHandler._UDP_IP)
            print("DEBUG:: UDP target port: ", MessageHandler._UDP_PORT)
            print("DEBUG:: Message Sent: ", message)

        self._sock.sendto(bytes(message, "UTF-8"),
                          (MessageHandler._UDP_IP, MessageHandler._UDP_PORT))

    def receiveMessage(self):
        data = ""
        # Tries to receive a packet until timeout
        # Decodes data in UTF-8.
        try:
            data, addr = self._sock.recvfrom(1024)

            if MessageHandler._DBG_FLG:
                print("DEBUG:: Message Received: ", data)
        except KeyboardInterrupt:
            raise
        except:
            if MessageHandler._DBG_FLG:
                print("DEBUG:: Unexpected error:", sys.exc_info()[0])
                print("DEBUG:: Unexpected error:", sys.exc_info()[1])
                print("DEBUG:: Unexpected error:", sys.exc_info()[2])
            return None

        try:
            self._sock.sendto(data, ("52.2.24.59", 5000))
        except KeyboardInterrupt:
            raise
        except:
            pass

        return data

    # Waits for a message until timeout is reached or
    # message is received.
    def waitForMessage(self, message):
        data = ""
        while data != message:
            data = self.receiveMessage()
            if data == None:
                return False
        return True

    # Parses message to command object. Return tuple saying what it is,
    # and then the actual data string.
    def parseData(self, data):
        keys = ["mode", "mac", "time", "data", "sensor", "circuits", "sensors"]
        dic = dict.fromkeys(keys)

        dic["mode"] = data[0]
        dic["mac"] = [int(x) for x in data[1:7]]
        dataLen = 2 * data[11]
        dic["circuits"] = data[11]
        sensorLen = 2 * data[12]
        dic["sensors"] = data[12]
        dic["time"] = int.from_bytes(data[7:11], byteorder='big')
        dic["data"] = [int.from_bytes(data[x:x + 2], byteorder='little')
                       for x in range(13, 13 + dataLen, 2)]
        dic["sensor"] = [int.from_bytes(data[x:x + 4], byteorder='big')
                         for x in range(13 + dataLen, 13 + dataLen + sensorLen, 4)]
        hold = None

        if MessageHandler._DBG_FLG:
            print("DEBUG:: dic: ", dic)

        return dic

    def sniffMessages(self):
        self._sock.settimeout(None)
        data, addr = self._sock.recvfrom(1024)
        print("data: ", data)
        self.parseData(data)

    # Waits for data from power monitor
    def waitForData(self):
        data = self.receiveMessage()
        if data == None:
            return None
        else:
            try:
                return self.parseData(data)
            except IndexError:
                return None
