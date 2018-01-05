
import os
import socket
import subprocess
import datetime
import weakref

wolPort = 55555
AppInstanceCounter = 1

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
            print(datetime.datetime.now(), ":\t", "Wake-on-LAN received for ApplicationID:", self.ApplicationID)
            if self.isTaskRunning():
                print(datetime.datetime.now(), ":\t", self.ApplicationParameters + 'is already running')
                return False
            else:
                print(datetime.datetime.now(), ":\t", 'Starting:', self.ApplicationParameters)
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


def getCapturedString():
    wOLServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    wOLServer.bind(("", wolPort))
    print(datetime.datetime.now(), ":\t", "Listening on 0.0.0.0 for Wake-on-LAN on port", wolPort, '(UDP)')
    wOLData = wOLServer.recv(1024)
    wOLServer.shutdown(0)
    wOLDatastring = wOLData.decode("utf-8")
    return wOLDatastring

print(datetime.datetime.now(), "First Time Setup")
print(datetime.datetime.now(), "--------------------------------------------------------\n")

print(datetime.datetime.now(), "Button No:",AppInstanceCounter,": setup follows:")
inApplicationPath = input("Enter Command/Path >>>>>: ")
App1 = Launcher(inApplicationPath)

print(datetime.datetime.now(), "Button No:",AppInstanceCounter,": setup follows:")
inApplicationPath = input("Enter Command/Path >>>>>: ")
App2 = Launcher(inApplicationPath)

print(datetime.datetime.now(), "Button No:",AppInstanceCounter,": setup follows:")
inApplicationPath = input("Enter Command/Path >>>>>: ")
App3 = Launcher(inApplicationPath)

print(datetime.datetime.now(), "Button No:",AppInstanceCounter,": setup follows:")
inApplicationPath = input("Enter Command/Path >>>>>: ")
App4 = Launcher(inApplicationPath)

print(datetime.datetime.now(), "Button No:",AppInstanceCounter,": setup follows:")
inApplicationPath = input("Enter Command/Path >>>>>: ")
App5 = Launcher(inApplicationPath)

print(datetime.datetime.now(), "Button No:",AppInstanceCounter,": setup follows:")
inApplicationPath = input("Enter Command/Path >>>>>: ")
App6 = Launcher(inApplicationPath)

print(datetime.datetime.now(), "Button No:",AppInstanceCounter,": setup follows:")
inApplicationPath = input("Enter Command/Path >>>>>: ")
App7 = Launcher(inApplicationPath)

print(datetime.datetime.now(), "Button No:",AppInstanceCounter,": setup follows:")
inApplicationPath = input("Enter Command/Path >>>>>: ")
App8 = Launcher(inApplicationPath)

run = True

while (run):
    capturedStr = getCapturedString()
    for obj in Launcher.getinstances():
        obj.openApp(capturedStr)

