
import os
import socket
import subprocess
import datetime
import weakref
import pickle


class Launcher:

    _instances = set()

    def __init__(self, FPath):
        global AppInstanceCounter
        self.Path = (FPath.rsplit('\\',1))
        self.ApplicationID = AppInstanceCounter
        self.ApplicationPath = self.Path[0]
        self.ApplicationParameters = self.Path[1]
        self.UDPBin = str(AppInstanceCounter).zfill(2)
        del self.Path
        del FPath
        self._instances.add(weakref.ref(self))
        AppInstanceCounter += 1

    def openApp(self, receivedBin):
        if receivedBin == self.UDPBin:
            print(datetime.datetime.now(), ":", "Matching UDP Packet received for ApplicationID:", self.ApplicationID)
            if self.isTaskRunning():
                print(datetime.datetime.now(), ":", self.ApplicationParameters + 'is already running')
                return False
            else:
                print(datetime.datetime.now(), ":", 'Starting:', self.ApplicationParameters)
                subprocess.call([self.ApplicationPath + "\\" + self.ApplicationParameters], 0)
                return True

    def isTaskRunning(self):
        tasklist = os.popen('tasklist /v | findstr "' + self.ApplicationParameters + '"')
        if self.ApplicationParameters in tasklist:
            return True
        return False

    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    def __str__(self):
        return "Button #{} - ApplicationPath: {} - ApplicationParameters: {} - UDPBin: {}".format(self.ApplicationID, self.ApplicationPath, self.ApplicationParameters, self.UDPBin)


def getCapturedString():
    wOLServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    wOLServer.bind(("", wolPort))
    print(datetime.datetime.now(), ":", "Listening on 0.0.0.0 for Matching UDP Packets on port", wolPort, '(UDP)')
    wOLData = wOLServer.recv(1024)
    wOLServer.shutdown(0)
    wOLDatastring = wOLData.decode("utf-8")
    return wOLDatastring


configFileName = "config.raw"
wolPort = 55555
AppInstanceCounter = 1
Apps = []

if os.path.isfile('./'+configFileName):
    print(datetime.datetime.now(), ":", "Config File found: " + configFileName + ". Loading Buttons")
    Apps = pickle.load(open(configFileName, "rb"))
else:
    print(datetime.datetime.now(), ":", "No Config File found: config.raw")
    print(datetime.datetime.now(), ":", "Setup follows")
    print(datetime.datetime.now(), ":", "--------------------------------------------------------\n")
    for i in range(0,8):
        print(datetime.datetime.now(), ":", "Button #" + str(AppInstanceCounter),"setup follows:")
        inApplicationPath = input("Enter Command/Path >>>>>: ")
        Apps.append(1)
        Apps[i] = Launcher(inApplicationPath)
        print(datetime.datetime.now(), ":", "Action saved:",str(Apps[i]))
    pickle.dump(Apps, open(configFileName, "wb"), pickle.HIGHEST_PROTOCOL)

run = True

while run:
    capturedStr = getCapturedString()
    for i in range(0,8):
        Apps[i].openApp(capturedStr)
