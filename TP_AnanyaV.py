##Contains all the tkinter as well as primary functions used in the project

from tkinter import *
import random
import math 
import os
from pyaudioSample import record
from pyaudioSample import WavePlayerLoop
import string
import threading
from TPclasses import Cat
from TPclasses import Building
from TPclasses import Power
from TPclasses import Speed
from TPclasses import Magnet
from TPclasses import Shield
from TPclasses import Fish
from TPclasses import Enemy
from TPclasses import flyingEnemy
from TPclasses import movingEnemy
from TPclasses import Bone
    

    
####################################Taken from 112 website

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

####################################

def init(data):
    data.mode = "StartScreen"
    data.bubble = PhotoImage(file="bubble.png")
    data.enemyPic = PhotoImage(file = "enemy.png")
    data.enemyPic2 = PhotoImage(file = "movingEnm.png")
    data.bonePic = PhotoImage(file = "fish.png")
    data.fishPic = PhotoImage(file = "coin.png")
    data.crowPic = PhotoImage(file = "crow.png")
    data.enmPicWidth = data.enemyPic.width()
    data.enmPicHeight = data.enemyPic.height()
    data.cx = data.width/2
    data.cy = data.height/2
    data.cat = Cat(data.cx,data.cy)
    data.buildingList = [Building(2000,data.height/2,data.cx,\
    data.cy+data.cat.height/2+data.height/4,\
    "firebrick3")]#stores building objects
    data.timerCalls = 0
    data.jump = False
    data.comingDown1 = False
    data.comingDown2 = False
    data.landing = True
    data.landed = True#stores whether cat is on a building 
    data.score = 0
    data.fishNum = {data.buildingList[0]:[5,set()]}#maps no. and 
    #set of fish objects to building objects
    data.displayGameOver = False
    data.fishSize = 20
    data.discardList = []
    data.enemyList = {}
    data.hasEnemy = {}
    data.enemySpeed = 100
    data.boneList = []
    data.speed = 60
    data.enemyDir = "Right"
    data.enemyMovingList = []
    data.buildingCount = 0
    data.generateIcon = False
    data.icon = None
    data.iconPic1 = PhotoImage(file="speed.png")
    data.timerVal = 20#dictates when building is generated
    data.hitTime = 0
    data.enemyJump = False
    data.enemyLanded = True
    data.enemyComingDown = False
    data.reverseBoneList = []
    data.reverseBone = False
    data.jumpTwice = False
    data.jumpPoint = 0
    data.displayHelp = False
    data.enemyJumpPoint = 0
    data.dist = 0
    data.vertDist = 0
    data.jumpLim = 80
    data.displayStats = False
    data.moon = PhotoImage(file = "moon.png")
    data.clouds = PhotoImage(file = "clouds.png")
    data.enmSpeed = 10
    data.colorList = ("IndianRed1","plum2","salmon","bisque","peach puff",\
    "light goldenrod","MediumPurple3","pale green", "medium sea green",\
    "VioletRed1","gold","brown1","brown2")
    data.enemyCalc = {}#stores jump data of cat so that the moving enemy 
    #can imitate it (jump height, jump point, etc.)
    data.curBuilding = data.buildingList[0]#current building cat is on
    data.magnetFish = []
    data.addedToFile = False
    data.displayTextBox = False
    data.StatName = ""
    data.pressEnter = False
    data.crowList = []
    data.drawShield = False
    data.recordColors = {0:"red",1:"red",2:"red"}
    data.gameSound = False
    data.pressNext = False
    data.pause = False
    data.jumpSound = None
    data.enemySound = None
    data.jumpSound2 = None
    data.fishSound = None
    data.enemySoundStart = 0
    data.fishSoundStart = 0
    data.gameOver = None
    data.collided = False
    
    

def mousePressed(event, data):
    if data.mode=="StartScreen":
        if data.cx - 200 <= event.x <= data.cx+200 and \
        data.cy-125<= event.y <= data.cy-75:
            data.mode = "Record"
        elif data.cx - 200 <= event.x <= data.cx+200 and \
        data.cy-25<= event.y <= data.cy+25:
            data.displayHelp = True
        elif data.cx - 200 <= event.x <= data.cx+200 and \
        data.cy+75<= event.y <= data.cy+125:
            data.displayStats = True
        if data.displayStats:
            if data.cx + 250 <= event.x <= data.cx+350 and \
            data.cy+290<= event.y <= data.cy+320:
                data.displayStats = False
        if data.displayHelp:
            if data.cx + 330 <= event.x <= data.cx+380 and \
            data.cy-80<= event.y <= data.cy-55:
                data.displayHelp = False
    elif data.mode == "GameOver" and data.displayTextBox:
        if data.cx - 200 <= event.x <= data.cx+280 and \
        data.cy+50<= event.y <= data.cy+80:
            if data.StatName == "":
                data.StatName = "Anon"#if no name is entered
            data.displayTextBox = False
            data.pressEnter = True
    elif data.mode == "Record":
        if data.cx + 50 <= event.x <= data.cx+150 and \
        data.cy-300<= event.y <= data.cy-225:
            record("jumpSound.wav")
            data.recordColors[0] = "green"
        elif data.cx + 50 <= event.x <= data.cx+150 and \
        data.cy-125<= event.y <= data.cy-50:
            record("enemy.wav")
            data.recordColors[1] = "green"
        elif data.cx + 50 <= event.x <= data.cx+150 and \
        data.cy+50<= event.y <= data.cy+125:
            record("fish.wav")
            data.recordColors[2] = "green"
        if (data.width-300 <= event.x <= data.width-200 and \
        data.height-100<= event.y <= data.height-50) and data.pressNext:
            data.mode = "Play"
       
        

def generateBuilding(data):#used to generate  a Building objects
#height and width of buildings change with score
    if data.score<15:
       bWidth = random.randint(900,1000)
       y = random.randint(720,750)
    elif data.score<50:
       bWidth = random.randint(800,850)
       y = random.randint(700,750)
    elif data.score<100:
       bWidth = random.randint(700,750)
       y = random.randint(680,750)
    else:
       bWidth = random.randint(650,700)
       y = random.randint(680,750)
    x = data.cx + data.width/2
    bHeight = 2*(data.height-y)
    color = random.choice(data.colorList)
    b = Building(bWidth,bHeight,x,y,color)#stores Building object
    data.buildingList.append(b)
    fSet = set() #holds all Fish objects on a building
    num = random.randint(2,5)#determine no. of fish on building
    x1 = b.x-b.width/2 + data.fishPic.width()/2
    y1 = b.y-b.height/2 - data.fishPic.height()/2
    gap = ((b.width-(num*data.fishPic.width())))/\
    (num-1)#calculates gap between fish
    for i in range(num):
        fSet.add(Fish(x1,y1))
        x1 += gap+data.fishSize
    data.fishNum[b] = [num,fSet]
    if data.score>10:#immobile enemies generated after score of 10
        data.hasEnemy[b] = random.choice((True,False))
        #determines if a building is to have an (immobile) enemy on it or not
        if data.hasEnemy[b] == True:
            data.enemyList[b] = Enemy(random.randint\
            (int(b.x-b.width/2+data.enmPicWidth/2),int(b.x+b.width/2-\
            data.enmPicWidth/2)),int(b.y-b.height/2-data.enmPicHeight/2+10))
    

def generateMovingEnemy(data):#generates moving enemy that follows cat
    if (data.buildingList[0].x+data.enemyPic2.width()/2>=0) and \
    data.enemyCalc.get(data.buildingList[0],0)!= 0 and \
    (data.timerDelay==data.enemyCalc[data.buildingList[0]][2]):
        #ensures enemy isn't generated on a gap between buildings
        b = data.buildingList[0] 
        x1 = data.enemyPic2.width()/2
        y1 = data.height - b.height - data.enemyPic2.height()/2
        data.enemyMovingList.append(movingEnemy(x1,y1))

def generateFlyingEnemy(data):#generates flying enemy that follows cat
    x1 = data.crowPic.width()/2
    y1 = random.randint(10,90)
    data.crowList.append(flyingEnemy(x1,y1))
    
    

def distance(x1,y1,x2,y2):#calculates distance between given co-ordinates
    return math.sqrt(((y2-y1)**2)+((x2-x1)**2))
    
def keyPressed(event, data):
    if data.mode == "Play" and not data.pause:
        if event.keysym == "Up" and data.jump!=True and data.comingDown1!=True \
        and data.comingDown2!=True and data.jumpTwice!=True:
            #the cat should not already be in the process of jumping or coming 
            #down in order to jump
            data.jumpSound = WavePlayerLoop("jumpSound.wav")
            data.jumpSound.play()
            data.jump = True
            data.jumpPoint = data.cat.y
            space = (data.curBuilding.x + data.curBuilding.width/2)-data.cat.x
            #space stores the distance bewteen the point at which the cat jumps 
            #and the end of the building
            data.enemyCalc[data.curBuilding] = [space,60,data.timerDelay]
        elif event.keysym=="Up" and (data.jump==True or data.comingDown1==True)\
        and data.comingDown2!=True and data.jumpTwice!=True:
            #used to allow the cat to jump a second time while already in air
            data.jumpSound2 = WavePlayerLoop("jumpSound.wav")
            data.jumpSound2.play()
            data.jumpTwice = True
            data.jumpPoint = data.cat.y
            data.jump = False
            if data.enemyCalc.get(data.curBuilding,0)!=0:
               data.enemyCalc[data.curBuilding][1] = 120
            #if cat jumps twice, its jump height is stored as 120 in enemyCalc
        if event.keysym == "x" and not data.reverseBone:
            try:#thread is closed before starting another thread
                data.fishSound.stop()
            except:
                pass
            data.fishSound = WavePlayerLoop("fish.wav")
            data.fishSound.play()
            data.fishSoundStart = data.timerCalls
            x1 = data.cat.x+data.cat.width/2+data.bonePic.width()
            y1 = data.cat.y
            data.boneList.append(Bone(x1,y1))
        elif event.keysym == "x" and data.reverseBone:
            try:
                data.fishSound.stop()
            except:
                pass
            data.fishSound = WavePlayerLoop("fish.wav")
            data.fishSound.play()
            data.fishSoundStart = data.timerCalls
            x1 = data.cat.x-data.cat.width/2-data.bonePic.width()/2
            y1 = data.cat.y
            data.reverseBoneList.append(Bone(x1,y1))
            data.reverseBone = False
        if event.keysym == "Left":
            data.reverseBone = True#user can shoot bone to the left
    if data.mode == "Play" and event.keysym == "p":#pauses game
        if data.pause == True:
            data.pause = False
        else:
            data.pause = True
    elif data.mode == "GameOver":
        if data.displayTextBox:
            #allows user to enter name for high score
            if (event.keysym in string.ascii_lowercase or event.keysym in \
            string.ascii_uppercase or event.keysym in string.whitespace) and \
            len(data.StatName)<= 8:
                data.StatName += event.keysym
            elif event.keysym == "BackSpace" and data.StatName!= "":
                data.StatName=data.StatName[:-1]
        elif data.displayGameOver:
            if event.keysym == "h":#go home
               if data.gameOver!=None:#closes thread
                   data.gameOver.stop()
               init(data)
            elif event.keysym == "r":#restart
               if data.gameOver!=None:#closes thread
                   data.gameOver.stop()
               init(data)
               data.mode = "Play"
    
def timerFired(data):
    if data.mode == "Play" and not data.pause:
        data.landed = False
        data.timerCalls += 1
        if data.mode == "Play":
            if data.jump:
                data.landing = False
                if data.jumpPoint - data.cat.y < 60:
                   data.cat.jump(20)
                else:
                    data.comingDown1 = True#stores whether cat is coming down
                    data.jump = False
            elif data.jumpTwice == True:
                if data.jumpPoint - data.cat.y < 60:
                   data.cat.jump(20)
                else:
                    data.jump = False
                    data.jumpTwice = False
                    data.comingDown2 = True
                    data.comingDown1 = False
            elif data.comingDown1 or data.comingDown2:
                data.cat.jump(-20)
                for i in data.buildingList:
                    if data.cat.landsOnBuilding(i):#checks if cat has landed
                        data.comingDown1 = False
                        data.comingDown2 = False
                        data.landed = True
            if data.cat.y + data.cat.height/2 >=data.height:
            #game over if character is no longer visible on screen as it has 
            #fallen all the way down
                data.mode="GameOver"
            for i in data.buildingList:
                    if i.x+i.width<=0:
                        data.buildingList.remove(i)
                        del data.fishNum[i]
                        if data.hasEnemy.get(i,0)!=0:
                            del data.hasEnemy[i]
                        if data.enemyList.get(i,0)!=0:
                            del data.enemyList[i]
                        if data.enemyCalc.get(i,0)!=0:
                            del data.enemyCalc[i]
                    else:
                        i.x-=data.speed
                        for j in data.fishNum[i][1]:
                            j.x -= data.speed
                            if data.cat.collidesWithFish(j):
                                data.discardList.append(j)
                        for k in data.discardList:
                            data.fishNum[i][1].discard(k)
                            data.score+=1
                        data.discardList = []
                        for enm in data.enemyList:
                            if data.cat.collidesWithEnemy(data.enemyList[enm]):
                                #game ends if cat collides with enemy
                                data.collided = True
                                data.mode = "GameOver"
                                data.displayGameOver = True
                                data.gameSound = True
                        if data.score>10:
                            if data.hasEnemy.get(i,0)!=0 and \
                            data.hasEnemy[i]==True:
                                data.enemyList[i].x-=data.speed
                        
                    if data.cat.landsOnBuilding(i) and not data.jump:
                        data.landed = True
                        try:
                           data.jumpSound.stop()
                        except:
                            pass
                        try:
                           data.jumpSound2.stop()
                        except:
                           pass
                        data.curBuilding = i
                        data.cat.y+= ((i.y - data.cat.y) - (i.height/2 + \
                        data.cat.height/2))#brings bottom of cat to level
                    elif data.cat.clashesWithBuilding(i):
                        data.cat.x = i.x-i.width/2-data.cat.width/2
                        data.mode = "GameOver"
            if len(data.buildingList)==1 and \
            data.cat.landsOnBuilding(data.buildingList[0]):
                #sometimes when list has only one element cat randomly vanishes 
                data.landed = True
            if not data.jump and not data.jumpTwice and \
            not data.comingDown1 and not data.landed and not data.comingDown2:
#if the cat is not on a building and is not in the midst of coming down/jumping
                data.mode = "GameOver"
                data.cat.x = data.curBuilding.x + data.curBuilding.width/2 + \
                data.cat.width/2
            
            for bone in data.boneList:
                for enm in data.enemyList:
                    if bone.collidesWithEnemy(data.enemyList[enm]):
                        try: 
                           data.enemySound.stop()
                        except:
                           pass
                        data.enemySound = WavePlayerLoop("enemy.wav")
                        data.enemySound.play()
                        data.enemySoundStart = data.timerCalls
                        del data.enemyList[enm]
                        del data.hasEnemy[enm]
                        data.boneList.remove(bone)
                        data.score+=2
                        break;
                for enm in data.crowList:
                    if bone.collidesWithEnemy(enm):
                        try: 
                           data.enemySound.stop()
                        except:
                           pass
                        data.enemySound = WavePlayerLoop("enemy.wav")
                        data.enemySound.play()
                        data.enemySoundStart = data.timerCalls
                        data.crowList.remove(enm)
                        data.boneList.remove(bone)
                        data.score+=3
                        break;
                if bone in data.boneList:
                   if bone.x-bone.width/2>data.width:
                       data.boneList.remove(bone)
                   else:
                       bone.x+=50
            for bone in data.reverseBoneList:
                for enm in data.enemyList:
                    if bone.collidesWithEnemy(data.enemyList[enm]):
                        try: 
                           data.enemySound.stop()
                        except:
                           pass
                        data.enemySound = WavePlayerLoop("enemy.wav")
                        data.enemySound.play()
                        data.enemySoundStart = data.timerCalls
                        del data.enemyList[enm]
                        del data.hasEnemy[enm]
                        data.reverseBoneList.remove(bone)
                        data.score+=2
                        break;
                for enm in data.enemyMovingList:
                    if bone.collidesWithEnemy(enm):
                        try: 
                           data.enemySound.stop()
                        except:
                           pass
                        data.enemySound = WavePlayerLoop("enemy.wav")
                        data.enemySound.play()
                        data.enemySoundStart = data.timerCalls
                        data.enemyMovingList.remove(enm)
                        data.reverseBoneList.remove(bone)
                        data.score+=3
                        break;
                for enm in data.crowList:
                    if bone.collidesWithEnemy(enm):
                        try: 
                           data.enemySound.stop()
                        except:
                           pass
                        data.enemySound = WavePlayerLoop("enemy.wav")
                        data.enemySound.play()
                        data.enemySoundStart = data.timerCalls
                        data.crowList.remove(enm)
                        data.reverseBoneList.remove(bone)
                        data.score+=3
                        break;
                if bone in data.reverseBoneList:
                   if bone.x-bone.width/2<=0:
                      data.reverseBoneList.remove(bone)
                   else:
                      bone.x-=50
            
            if data.score>30 and data.timerCalls%100==True:
                #crow generated every 10s after score hits 30
                generateFlyingEnemy(data)
            for i in data.crowList:
                if data.cat.collidesWithEnemy(i):
                    data.mode = "GameOver"
                    data.displayGameOver = True
                    data.gameSound = True
                else:
                    if i.x<data.cat.x:
                        i.x+=30
                    else:
                        i.x-=30
                    if i.y<data.cat.y-data.cat.height/2:
                        i.y+=30
                    else:
                        i.y-=30
                
            if data.score>20 and data.timerCalls%50==True:
                #moving enemy generated every 5s after score hits 20
                generateMovingEnemy(data)
            for i in data.enemyMovingList:
                if data.cat.collidesWithEnemy(i):
                    data.collided = True
                    data.mode = "GameOver"
                    data.displayGameOver = True
                    data.gameSound = True
                for b in data.buildingList:
                    if i.landsOnBuilding(b):
                        if data.enemyCalc.get(b,0)!=0:
                          data.jumpLim = data.enemyCalc[b][1]
                          #jumpLim is total height an enemy should jump
                          if abs((b.x + b.width/2)-i.x)<=data.enemyCalc[b][0]+50:
                              #checks if enemy should jump
                              data.enemyJump = True
                              data.enemyJumpPoint = i.y
                    if data.enemyJump:
                        if data.enemyJumpPoint - i.y < data.jumpLim:
                            i.jump(20)
                        else:
                            data.enemyComingDown = True#stores whether enemy 
                            #is coming down
                            data.enemyJump = False
                    elif data.enemyComingDown:
                        i.jump(-20)
                        for c in data.buildingList:
                            if i.landsOnBuilding(c):
                                data.enemyComingDown = False
                    if i.landsOnBuilding(b) and not data.enemyJump:
                        if i.y<(b.y - b.height/2 - i.height/2):
                            i.y+= (b.y - b.height/2 - i.height/2)-i.y#brings 
                            #bottom of enemy to level
                        elif i.y>(b.y - b.height/2 - i.height/2):
                            i.y-= i.y-(b.y - b.height/2 - i.height/2)
                    else:
                        i.x+=data.enmSpeed
            if data.timerCalls%data.timerVal==0:#building generated every 2s
                generateBuilding(data)
                data.buildingCount+=1
                if data.buildingCount%6==0:#random icon generated for every
                #8th building
                    data.generateIcon = True
                    b = data.buildingList[-1]
                    m = Magnet(random.randint(int(b.x-b.width/2+\
                    data.iconPic1.width()/2),int(b.x+b.width/2-\
                    data.iconPic1.width()/2)),\
                    int(b.y-b.height/2-data.iconPic1.height()/2))
                    s = Speed(random.randint(int(b.x-b.width/2+\
                    data.iconPic1.width()/2),int(b.x+b.width/2-\
                    data.iconPic1.width()/2)),int(b.y-b.height/2-\
                    data.iconPic1.height()/2))
                    shd = Shield(random.randint(int(b.x-b.width/2+\
                    data.iconPic1.width()/2),int(b.x+b.width/2-\
                    data.iconPic1.width()/2)),int(b.y-b.height/2-\
                    data.iconPic1.height()/2))
                    data.icon = random.choice([m,s,shd])
            if type(data.icon) == Speed:#increases speed of cat 
                if data.generateIcon:
                    if data.cat.collidesWithPower(data.icon):
                        data.hitTime = data.timerCalls
                        data.generateIcon = False
                        data.timerDelay = 50
                        data.enmSpeed = 10
                    else:
                        data.icon.x-=data.speed
                elif data.hitTime!=0:
                    if (data.timerCalls - data.hitTime) >= 100:#icon effect 
                    #wears off after 5s
                        data.timerDelay = 100
                        data.enmSpeed = 20
                        data.hitTime = 0
            elif type(data.icon) == Magnet:
                #adds fish to score if cat is close to it
                if data.generateIcon:
                    if data.cat.collidesWithPower(data.icon):
                        data.hitTime = data.timerCalls
                        data.generateIcon = False
                    else:
                        data.icon.x-=data.speed
                elif data.hitTime!=0:
                    if (data.timerCalls - data.hitTime) >= 50:#icon effect
                    #wears off after 5s
                        data.hitTime = 0
                        data.score+=len(data.magnetFish)
                        data.magnetFish = []
                    else:
                        for f in data.fishNum:
                            for fish in data.fishNum[f][1]:
                                if distance(data.cat.x,data.cat.y,\
                                fish.x,fish.y) <= 300:
                                   data.magnetFish.append(fish)
                                   data.discardList.append(fish)
                            for x in data.discardList:
                                data.fishNum[f][1].remove(x)
                            data.discardList = []
                        for fish in data.magnetFish:
                                if data.cat.collidesWithFish(fish):
                                    data.magnetFish.remove(fish)
                                    data.score+=1
                                else:
                                    #moves fish towards the cat
                                    if fish.x>data.cat.x:
                                        fish.x-=50
                                    elif fish.x<data.cat.x:
                                        fish.x+=50
                                    if fish.y>data.cat.y:
                                        fish.y-=20
                                    elif fish.y<data.cat.y:
                                        fish.y+=20
            elif type(data.icon) == Shield:#protects cat from enemies
                if data.generateIcon:
                    if data.cat.collidesWithPower(data.icon):
                        data.hitTime = data.timerCalls
                        data.generateIcon = False
                        data.drawShield = True
                    else:
                        data.icon.x-=data.speed
                elif data.hitTime!=0:
                    if (data.timerCalls - data.hitTime) >= 50:#icon effect
                    #wears off after 5s
                        data.hitTime = 0
                        data.drawShield = False
                    else:
                        for enm in data.enemyList:
                            if distance(data.cat.x,data.cat.y,\
                            data.enemyList[enm].x,data.enemyList[enm].y)<=200:
                                del data.enemyList[enm]
                                del data.hasEnemy[enm]
                                try: 
                                  data.enemySound.stop()
                                except:
                                  pass
                                data.enemySound = WavePlayerLoop("enemy.wav")
                                data.enemySound.play()
                                data.enemySoundStart = data.timerCalls
                                data.score+=2
                                break;
                        for enm in data.crowList:
                            if distance(data.cat.x,data.cat.y,enm.x,enm.y)<=300:
                                data.crowList.remove(enm)
                                try: 
                                  data.enemySound.stop()
                                except:
                                  pass
                                data.enemySound = WavePlayerLoop("enemy.wav")
                                data.enemySound.play()
                                data.enemySoundStart = data.timerCalls
                                data.score+=3
                                break;
                        for enm in data.enemyMovingList:
                            if distance(data.cat.x,data.cat.y,enm.x,enm.y)<=300:
                                data.enemyMovingList.remove(enm)
                                try: 
                                  data.enemySound.stop()
                                except:
                                  pass
                                data.enemySound = WavePlayerLoop("enemy.wav")
                                data.enemySound.play()
                                data.enemySoundStart = data.timerCalls
                                data.score+=3
                                break;
           
            if data.enemySound!=None and (data.timerCalls - \
            data.enemySoundStart)>=20 and \
            data.enemySoundStart!=0:#closes thread for "enemy hit" sound
                data.enemySoundStart = 0
                data.enemySound.stop()
            
            if data.fishSound!=None and (data.timerCalls - \
            data.fishSoundStart)>=20 and \
            data.fishSoundStart!=0:#closes thread for "bone shooting" sound
                data.fishSoundStart = 0
                data.fishSound.stop()
                    
    elif data.mode=="GameOver":
        #closes any existing threads
        if data.jumpSound!=None:
            data.jumpSound.stop()
        if data.jumpSound2!=None:
            data.jumpSound2.stop()
        if data.enemySound!=None:
            data.enemySound.stop()
        if data.fishSound!=None:
            data.fishSound.stop()
        data.drawShield = False
        data.timerDelay = 100#if speed icon was in use, effects are reverted
        if data.cat.y-data.cat.height/2<=data.height:
            data.cat.jump(-40)
        else:
            data.displayGameOver = True
            if not data.addedToFile:#checks if score (if in top 5) has not been
            #added to file
                try:
                    scoreList = getScoreList("score.txt")[0]
                    nameList = getScoreList("score.txt")[1]
                    for i in range(len(scoreList)):
                        if scoreList[i] == -1:#if slot is empty
                            if not data.pressEnter:
                               data.displayTextBox = True
                            else:
                                scoreList[i] = data.score
                                nameList[i] = data.StatName
                                break;
                        elif data.score>scoreList[i]:
                            if not data.pressEnter:
                                data.displayTextBox = True
                            else:
                                scoreList.insert(i,data.score)
                                nameList.insert(i,data.StatName)
                                break;
                    if len(scoreList)>5:
                        scoreList.pop()
                        nameList.pop()
                    contents = ""
                    for i in range(len(scoreList)):
                        if i==4:
                            contents+=str(scoreList[i])+":"+nameList[i]
                        else:
                            contents+=str(scoreList[i])+":"+nameList[i]+","
                    writeFile("score.txt",contents)
                except:#if score.txt has not yet been made
                    if not data.pressEnter:
                       data.displayTextBox = True
                    else:
                       writeFile("score.txt",str(data.score)+":"+data.StatName)
                if data.pressEnter:
                   data.addedToFile = True
                
def getScoreList(file):#takes score file & returns two lists of scores and names
    doc = readFile(file)
    scoreList = [-1,-1,-1,-1,-1]
    nameList = ["","","","",""]
    count = 0
    for score in doc.split(","):
        sections = score.split(":")
        number = sections[0]
        name = sections[1]
        scoreList[count]=int(number)
        nameList[count] = name
        count+=1
    return (scoreList,nameList)

def pressNext(data):#checks whether next can be pressed on record screen (all 
 #sounds have been recorded)
    for color in data.recordColors:
        if data.recordColors[color]!="green":
            return False
    return True


def redrawAll(canvas, data):
    if data.mode=="StartScreen":
        canvas.create_text(data.cx,200,text="CAT ON A ROOF",font="Verdana \
        80 bold", fill = "DeepPink2" )
        canvas.create_rectangle(data.cx-200,data.cy-125,data.cx+200,\
        data.cy-75,fill="orange")
        canvas.create_text(data.cx,data.cy-100,text="START",\
        font="Arial 22 bold")
        canvas.create_rectangle(data.cx-200,data.cy-25,data.cx+200,data.cy+25,\
        fill="deep pink")
        canvas.create_text(data.cx,data.cy,text="HELP",font="Arial 22 bold")
        canvas.create_rectangle(data.cx-200,data.cy+75,data.cx+200,data.cy+125,\
        fill="green yellow")
        canvas.create_text(data.cx,data.cy+100,text="STATS",\
        font="Arial 22 bold")
        if data.displayHelp:
            canvas.create_rectangle(data.cx-400,data.cy-100,data.cx+400,\
            data.cy+100,fill="white")
            canvas.create_text(data.cx-65,data.cy-70,
            text="""Ginger the cat has embarked on an exciting journey to \
satiate his unsatiable hunger for fish!""",font="Arial 16 bold",\
fill = "magenta")
            canvas.create_text(data.cx,data.cy,text="""HOW TO PLAY:\n1) \
Press the Up key once to jump and twice to jump higher!\n2) Press 'x' to shoot \
fish bones at enemies on the right! Press the Left key followed by 'x' to \
shoot at enemies on the left!\n3) Collect fish to increase your score!\n4) \
Shooting stationary enemies gives you 2 points!\n5) Shooting moving and flying \
enemies gives you 3 points!\n6) HAVE FUN :)""",font="Arial 13 bold")
            canvas.create_rectangle(data.cx+330,data.cy-80,data.cx+380,\
            data.cy-55,fill="red")
            canvas.create_text(data.cx+355,data.cy-67.5,text="Close",\
            font="Arial 10 bold" )
        if data.displayStats:
            canvas.create_rectangle(data.cx-400,data.cy-350,data.cx+400,\
            data.cy+350,fill="light salmon")
            x1,y1,x2,y2 = data.cx-250, data.cy-250, data.cx-50,data.cy-190
            yInc = 110
            xInc = 300 
            boxWidth = 100
            boxHeight = 60
            try:
              scoreList = [-1,-1,-1,-1,-1]
              nameList = ["","","","",""]
              filename = readFile("score.txt")
              elems = filename.split(",")
              count = 0
              for elem in elems:
                  section = elem.split(":")
                  scoreList[count] = section[0]
                  nameList[count] = section[1]
                  count+=1
            except:
              scoreList = [-1,-1,-1,-1,-1]
              nameList = ["","","","",""]
            canvas.create_text(data.cx, data.cy-300,text="HIGH SCORES",\
            font="verdana 24 bold",fill = "DeepPink4")
            for i in range(5):
                canvas.create_rectangle(x1,y1,x2,y2,fill="salmon")
                canvas.create_rectangle(x1+xInc,y1,x2+xInc,y2,fill="salmon")
                canvas.create_text(x1-20,y1+20,text=str(i+1),\
                font="Arial 16 bold",fill = "DeepPink4")
                if nameList[i]!="":
                   canvas.create_text(x1+boxWidth/2+5,y1+boxHeight/2,\
                   text=nameList[i],font="Arial 16 bold",\
                   anchor=W,fill = "DeepPink4",width=80)
                   canvas.create_text(x1+xInc+boxWidth/2+20,y1+boxHeight/2,\
                   text=scoreList[i],font="Arial 20 bold",anchor=W,\
                   fill = "DeepPink4")
                y1 += yInc
                y2 += yInc
            canvas.create_rectangle(data.cx+250,data.cy+290,\
            data.cx+350,data.cy+320,fill="red")
            canvas.create_text(data.cx+300,data.cy+305,text="Close")
            
    elif data.mode == "Record":
        x1,y1,x2,y2 = data.cx-250,data.cy-300,data.cx-50,data.cy-225
        nameDict = {0:"Jump!",1:"Enemy defeated!",2:"Shoot fish!"}
        for i in range(3):
            canvas.create_rectangle(x1,y1,x2,y2,fill="grey")
            canvas.create_rectangle(x1+300,y1,x2+200,y2,\
            fill = data.recordColors[i])
            canvas.create_text(x1+350,y1+37.5,text="Record!", \
            font = "Arial 16 bold")
            canvas.create_text(x1+100,y1+37.5,text=nameDict[i],\
            font = "Arial 16 bold",fill="white")
            y1+=175
            y2+=175
        canvas.create_text(data.cx,data.cy+300,text="""Click on the Record \
button to record your own sound! The button will turn from red to green once \
recording has stopped!""",font = "Arial 28 bold",fill="white")
        if pressNext(data):
            data.pressNext = True 
            canvas.create_rectangle(data.width-300,data.height-100,\
            data.width-200,data.height-50,fill="light green")
            canvas.create_text(data.width-250,data.height-75,text="Next")
        else:
            data.pressNext = False
            canvas.create_rectangle(data.width-300,data.height-100,\
            data.width-200,data.height-50,fill="gray")
            canvas.create_text(data.width-250,data.height-75,text="Next")
        
                
    else:
        canvas.create_image(200,200,image=data.moon)
        canvas.create_image(250,250,image=data.clouds)
        data.cat.draw(canvas)
        for i in data.buildingList:
            i.draw(canvas)
            for j in data.fishNum[i][1]:
                j.draw(canvas)
            if data.score>10:
                if data.hasEnemy.get(i,0)!=0 and data.hasEnemy[i]==True:
                    enemy = data.enemyList[i]
                    enemy.draw(canvas)
        for bone in data.boneList:
            bone.draw(canvas)
        for bone in data.reverseBoneList:
            bone.draw(canvas)
        canvas.create_text(data.width/15,data.height/10,text = "Score: " + \
        str(data.score), font="Arial 20 bold", fill = "magenta")
        canvas.tag_raise(data.cat)
        for enm in data.enemyMovingList:
            enm.draw(canvas)
        if data.generateIcon:
            data.icon.draw(canvas)
        for fish in data.magnetFish:
            fish.draw(canvas)
        for bird in data.crowList:
            bird.draw(canvas)
        if data.drawShield:
            canvas.create_image(data.cat.x,data.cat.y,image=data.bubble)
        canvas.create_text(data.width-200,50,text="Press 'p' to pause!",\
        font = "Arial 22 bold", fill = "orange")
        if data.displayGameOver:
            canvas.create_text(data.cx,data.cy,text = "GAME OVER!",\
            font="Arial 28 bold", fill = "magenta")
            canvas.create_text(data.cx, data.cy+50, \
            text = "Press 'r' to restart!", font = "Arial 22 bold", \
            fill = "magenta" )
            canvas.create_text(data.cx, data.cy+100, \
            text = "Press 'h' to go home!", font = "Arial 22 bold", \
            fill = "magenta" )
            if data.gameSound and data.collided:
                data.gameOver = WavePlayerLoop("gameOver.wav")
                data.gameOver.play()
                data.gameSound = False
            elif not data.collided:
                data.gameOver = WavePlayerLoop("gameOver.wav")
                data.gameOver.play()
                data.collided = True
        if data.displayTextBox and data.displayGameOver:
            canvas.create_rectangle(data.cx-300,data.cy-100,\
            data.cx+300,data.cy+100,fill="pink")
            canvas.create_text(data.cx-25,data.cy-80,\
            text="Great job! Enter your name!",font="Arial 20 bold")
            canvas.create_rectangle(data.cx-50,data.cy-10,\
            data.cx+50,data.cy+10,fill="white")
            canvas.create_text(data.cx,data.cy,text=data.StatName)
            canvas.create_rectangle(data.cx+200,data.cy+50,data.cx+280,\
            data.cy+80,fill="green")
            canvas.create_text(data.cx+240,data.cy+65,text="Go!")

def run(width=300, height=300):#Adapted from 15-112 website course notes
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='medium blue', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    class Struct(object): pass
    data = Struct()

    data.width = width
    data.height = height
    data.timerDelay = 100 
    root = Tk()
    root.resizable(width=False, height=False) 
    init(data)
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()

    
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop() 
    print("bye!")

run(2000, 900)