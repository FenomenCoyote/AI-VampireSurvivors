import kbhit
from time import sleep, time
from fsm import FSM
from math import cos, sin, pi
import numpy as np
import cv2
import os

import win32.win32gui as win32gui
import win32.win32api as win32api
import win32con

import vgamepad as vg

from runAway import RunAway
from choose import Choose
from dead import Dead

from atMenuTransition import AtMenuTransition
from inGameTransition import InGameTransition
from gameOverTransition import GameOverTransition

FRAMES_PER_SECOND = 18
S_PER_FRAME = 1.0 / FRAMES_PER_SECOND

def getWindowHandler():
    hwndMain = win32gui.FindWindow(None, "Vampire Survivors")
    if hwndMain == 0:
        return 0

    hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)
    if hwndChild == 0:
        return 0
    
    return hwndChild


def press(gamepad, key):
    gamepad.press_button(key)
    return key
    
    
def release(gamepad, key):
    gamepad.release_button(key)
    return key


def movement(gamepad, directionAngle):

    x = cos(directionAngle)
    y = sin(directionAngle)
        
    gamepad.left_joystick_float(x, y)

def main():
    
    gamepad = vg.VX360Gamepad()
    
    handler = getWindowHandler()
    
    while handler == 0:
        print("Vampire Survivors not found")
        sleep(2)
        handler = getWindowHandler()
        
    
    kb = kbhit.KBHit()
    
    fsm = FSM(FRAMES_PER_SECOND, False)
    
    # states
    runAway = RunAway("Run Away") 
    choose = Choose("Choose")
    dead = Dead("Dead")
    
    # transitions  d
    atMenuTransition = AtMenuTransition()
    inGameTransition = InGameTransition()
    gameOverTransition = GameOverTransition()
    
    # join
    fsm.add(runAway, atMenuTransition, choose)
    fsm.add(runAway, gameOverTransition, dead)
    fsm.add(choose, inGameTransition, runAway)
    
    pressedBefore = [] 
    pressedNow = [] 
    
    sleepTimeMin = 1
    sleepTimeSum = []  
    timesExceededTime = 0 
    frames = 0
    
    for i in range(2, 0, -1): 
        print("starting in", i, "seconds...")
        sleep(1)
    print("starting now!")
    
    # stater
    fsm.ready(runAway)
    
    accept = vg.XUSB_BUTTON.XUSB_GAMEPAD_A 

    firstTick = True
    press(gamepad, accept)
    
    # if not os.path.exists('ScreenShots'):
    #     os.makedirs('ScreenShots')
    
    while True:
        if (kb.kbhit()):
            break
        
        frames += 1
        
        lastTickTime = time()
        
        move, directionAngle, pressSpaceBar = fsm.tick() 
        
        # fsm._info.view.save("ScreenShots/shotAt" + str(frames) + ".png")
          
        pressedNow = [] 
        
        if(move): movement(gamepad, directionAngle)
        else: gamepad.left_joystick(0, 0)
        if(pressSpaceBar): pressedNow.append(press(gamepad, accept))
            
        # release if i pressed the key before but im not pressing it now
        for k in pressedBefore:
            if not k in pressedNow:
                release(gamepad, k)

        pressedBefore = pressedNow.copy()
        
        gamepad.update()

        elapsedTime = time() - lastTickTime
        
        sleepTime = S_PER_FRAME - elapsedTime
        if(sleepTime < sleepTimeMin): sleepTimeMin = sleepTime
        if(sleepTime < 0): timesExceededTime += 1
                
        sleepTimeSum.append(max(0, sleepTime))
        sleep(max(sleepTime, 0))
        
        if(firstTick):
            firstTick = False
            release(gamepad, accept)
            gamepad.update()
        
    release(gamepad, vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.left_joystick_float(0, 0)
    gamepad.update()
    
    # time report
    print("\nseconds per frame:", S_PER_FRAME)
    print("percentage sleep time: ", ((sum(sleepTimeSum) / len(sleepTimeSum) / S_PER_FRAME) * 100), "%", sep='')
    print("minimum percentage slept time in a frame: ", ((sleepTimeMin / S_PER_FRAME) * 100), "%", sep='')
    print("times where tick exceeded frame time: ", timesExceededTime, " of a total of: ", frames, " (", ((timesExceededTime / frames)*100), "%)", sep='')
    
    # monta un video del ultimo minuto que vio la IA, con 6 veces mas resolucion
    if fsm._info.makeVideo:
        print("making video...")
        images = fsm.getInfo().getViewsArray() 
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        video = cv2.VideoWriter("whatAIsaw.avi", fourcc, FRAMES_PER_SECOND, images[0].size)
        
        for img in images:
            video.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
            
        video.release()
    
    print("done")
    
    return 0


main()