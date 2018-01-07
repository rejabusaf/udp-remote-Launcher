
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
        self.Pid = 0
        self.process = 0
        del self.Path
        del FPath
        self._instances.add(weakref.ref(self))
        AppInstanceCounter += 1

    def startStopApp(self, receivedBin):
        if receivedBin == self.UDPBin:
            if self.Pid < 1:
                print(datetime.datetime.now(), ":", "Signal received to START", self.ApplicationID)
                if self.isTaskRunning():
                    print(datetime.datetime.now(), ":", self.ApplicationParameters , 'is already running')
                    return False
                else:
                    fullPath = str(explorerPath + ' "' + self.ApplicationPath + "\\" + self.ApplicationParameters+ '"')
                    print(fullPath)
                    self.process = subprocess.Popen(fullPath, shell=True)
                    self.process.communicate()
                    print(datetime.datetime.now(), ":", self.ApplicationParameters, 'Started with PID:', self.Pid)
                    self.Pid = self.process.pid
                    return True
            else:
                self.process.terminate()
                print(datetime.datetime.now(), ":", "Signal received to STOP", self.ApplicationParameters, )
                print(datetime.datetime.now(), ":", self.ApplicationParameters, 'with PID:', self.Pid, 'Stopped')
                self.Pid = 0
                return False

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
    wOLServer.bind(("", inListenPort))
    print(datetime.datetime.now(), ":", "Listening on 0.0.0.0 for Matching UDP Packets on port", inListenPort, '(UDP)')
    wOLData = wOLServer.recv(1024)
    wOLServer.shutdown(0)
    wOLDatastring = wOLData.decode("utf-8")
    return wOLDatastring


configFileName = "config.raw"
inListenPort = 170 # Print server
AppInstanceCounter = 1
explorerPath = '"C:\Windows\explorer.exe"'
Apps = []

if os.path.isfile('./'+configFileName):
    print(datetime.datetime.now(), ":", "Config File found: " + configFileName + ". Loading Buttons")
    Apps = pickle.load(open(configFileName, "rb"))
else:
    print(datetime.datetime.now(), ":", "No Config File found: config.raw")
    print(datetime.datetime.now(), ":", "Setup follows")
    print(datetime.datetime.now(), ":", "--------------------------------------------------------\n")
    inListenPort = input("Port number [ default: 170 ]:")
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
        Apps[i].startStopApp(capturedStr)
        
