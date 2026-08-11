import random
import time

currentOrientation = 0
currentBattery = 100
temperature = 20
startTime = time.time()

def readOrientation():
    global currentOrientation
    
    currentOrientation += random.randrange(1, 30)
    if currentOrientation > 360:
        currentOrientation = currentOrientation - 360
    return currentOrientation

def setOrientation(orientation):
    global currentOrientation
    currentOrientation = orientation

def getRuntTime():
    return round(time.time() - startTime)
