import subprocess, threading, re, winsound
from time import sleep

class Ping(object):
    def __init__(self, host):
        self.host = host

    def ping(self):
        subprocess.call("ping %s -t > ping.txt" % self.host, shell = True)

    def getping(self):
        pingfile = open("ping.txt", "r")
        pingresults = pingfile.read()
        return pingresults

def parseLines(lines):
    result = []
    for line in lines:
        if line:
            searchObj=re.search(r'Reply from .* time=(.*)ms', line, re.M|re.I)
            if searchObj:
                result.append(searchObj.group(1))
    return result

def getAverage(pingArray):
    sum=0
    for number in pingArray[-20:]:
        sum = sum + int(number)
    return sum / len(pingArray)

def main(host):
    PingClass = Ping(host)
    
    
    startthread(PingClass.ping)# if you want to execute code while pinging. 
    lines= PingClass.getping().splitlines()  
    averagePing=100
    while (len(lines) < 10 or averagePing > 50):
        sleep(1)    
        lines= PingClass.getping().splitlines()        
        pingArray = parseLines(lines)
        averagePing= getAverage(pingArray)
        print(averagePing)
    
    frequency = 2500  # Set Frequency To 2500 Hertz
    winsound.Beep(frequency, 1500)

def startthread(method):
    threading.Thread(target = method).start()

main("www.google.com")
