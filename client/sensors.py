import random
currentOrientation = 0

def readOrientation():
    global currentOrientation
    
    currentOrientation += random.randrange(1, 30)
    if currentOrientation > 360:
        currentOrientation = currentOrientation - 360
    return currentOrientation

def setOrientation(orientation):
    global currentOrientation
    currentOrientation = orientation
