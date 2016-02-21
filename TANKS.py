#TANKS
#BY: SOURAV B.

#IMPORTS AND INITIAL SETUP

from tkinter import *
from time import *
from math import *

root = Tk()
s = Canvas(root, width = 1200, height = 900,background = "white")
s.pack()


def DrawWall(Orientation,Level,Min,Max): #DRAWS WALLS, USED LATER TO DRAW MAP
    
    if Orientation == "h": #WALLS ARE EITHER VERTICAL OR HORIZONTAL
        s.create_line(Min,Level,Max,Level,fill = "SlateGray4",width = 5)
    else:
        s.create_line(Level,Min,Level,Max,fill = "SlateGray4",width = 5)

    WallOrientations.append(Orientation)
    WallLevels.append(Level)
    WallMins.append(Min)
    WallMaxs.append(Max)


def getEquationOfLine(x1,y1,x2,y2): #RETURNS ARRAY WITH "M" VALUE AND "B" VALUE, EXCEPTION FOR VERTICAL LINE
    
    if x1 == x2:
        Equation = ["undefined",x1] #RETURNS "UNDEFINED" SLOPE AND X - INTERCEPT FOR VERTICAL LINE
        
    else:
        m = (y2 - y1)/(x2 - x1)
        b = y1 - m*x1
        Equation = [m,b]
            
    return Equation
    

def CheckHit(x1,y1,x2,y2,x3,y3,x4,y4,XAmmo,YAmmo): #RETURNS TRUE IF A PLAYER HAS BEEN HIT, OTHERWISE RETURNS FALSE
    
    EqA = getEquationOfLine(x1,y1,x2,y2) #USES INEQUALITIES
    EqB = getEquationOfLine(x2,y2,x3,y3)
    EqC = getEquationOfLine(x3,y3,x4,y4)
    EqD = getEquationOfLine(x4,y4,x1,y1)

    if EqA[0] == "undefined" or EqC[0] == "undefined" or EqB[0] == 0 or EqD[0] == 0: #CASE 1 - TANK POINTING UP

        #SECOND CONDITION MUST BE ADDED BECAUSE OF A SPECIFIC TEST CASE (DUE TO PYTHON ROUNDING ERRORS) AND THIS MUST BE ACCOUNTED FOR

        if EqB[0] == 0:
            x1 = x2
            if y2 > y1:
                y1 = y2 - tankH
            else:
                y1 = y2 + tankH
            x4 = x3
            y4 = y1
            EqA = getEquationOfLine(x1,y1,x2,y2) 
            EqC = getEquationOfLine(x3,y3,x4,y4)
            EqD = getEquationOfLine(x4,y4,x1,y1)
            
        XCheck = False 
        YCheck = False
        
        if EqA[1] > EqC[1]:
            if XAmmo <= EqA[1] and XAmmo >= EqC[1]:
                XCheck = True
            if YAmmo >= EqB[1] and YAmmo <= EqD[1]:
                YCheck = True
                
        else:
            if XAmmo >= EqA[1] and XAmmo <= EqC[1]:
                XCheck = True
            if YAmmo <= EqB[1] and YAmmo >= EqD[1]:
                YCheck = True

        if XCheck == True and YCheck == True:
            return True
        
    elif EqA[0] == 0 or EqC[0] == 0 or EqB[0] == "undefined" or EqD[0] == "undefined": #CASE 2 - TANK POINTING TO THE SIDE

        #ANOTHER SECOND CONDITION DUE TO PYTHON ROUNDING ERRORS

        if EqD[0] == "undefined":
            if y1 > y4:
                x2 = x1 + tankH
            else:
                x2 = x1 - tankH
            y2 = y1
            x3 = x2
            y3 = y4
            EqA = getEquationOfLine(x1,y1,x2,y2) 
            EqB = getEquationOfLine(x2,y2,x3,y3)
            EqC = getEquationOfLine(x3,y3,x4,y4)
            
        XCheck = False 
        YCheck = False #MUST CHECK IF THE INEQUALITY IS SATISFIED
        
        if EqA[1] < EqC[1]:
            if YAmmo >= EqA[1] and YAmmo <= EqC[1]:
                YCheck = True
            if XAmmo >= EqB[1] and XAmmo <= EqD[1]:
                XCheck = True
                
        else:
            if YAmmo <= EqA[1] and YAmmo >= EqC[1]:
                YCheck = True
            if XAmmo <= EqB[1] and XAmmo >= EqD[1]:
                XCheck = True
            
        if XCheck == True and YCheck == True:
            return True

    else:   #CASE 3 - TANK ON AN ANGLE

        Check1 = False
        Check2 = False
        
        if EqA[1] < EqC[1]:
            if YAmmo >= XAmmo*EqA[0] + EqA[1] and YAmmo <= XAmmo*EqC[0] + EqC[1]:
                Check1 = True
        else:
            if YAmmo <= XAmmo*EqA[0] + EqA[1] and YAmmo >= XAmmo*EqC[0] + EqC[1]:
                Check1 = True
                
        if EqB[1] < EqD[1]:
            if YAmmo >= XAmmo*EqB[0] + EqB[1] and YAmmo <= XAmmo*EqD[0] + EqD[1]:
                Check2 = True
        else:
            if YAmmo <= XAmmo*EqB[0] + EqB[1] and YAmmo >= XAmmo*EqD[0] + EqD[1]:
                Check2 = True

        if Check1 == True and Check2 == True:
            return True
        
    return False

def SetHealthBars(): #SETS UP HEALTH BARS AND IN-GAME TITLE

    global P1HPLabel,P2HPLabel,P1HPLabelC,P2HPLabelC,P1HP,P2HP,P1HPNum,P1HPNumShade,P2HPNum,P2HPNumShade

    #TITLE

    TanksTitle = s.create_text(600,100,text = "TANKS",fill = "black",font = "Arial 55 bold")

    #LABELS

    #CREATES SHADES

    P1HPLabelShade = s.create_text(251,76,text = "Player 1 HP",fill = "grey",font = "Arial 28")
    P2HPLabelShade = s.create_text(901,76,text = "Player 2 HP",fill = "grey",font = "Arial 28")

    P1HPLabel = s.create_text(250,75,text = "Player 1 HP",fill = "black",font = "Arial 28")
    P2HPLabel = s.create_text(900,75,text = "Player 2 HP",fill = "black",font = "Arial 28")

    P1HPLabelC = s.create_oval(362,62,388,88,fill = TankC)
    P2HPLabelC = s.create_oval(1012,62,1038,88,fill = P2TankC)

    #HEALTH BARS

    P1HP = s.create_rectangle(150,100,400,150,fill = "green")
    P2HP = s.create_rectangle(800,100,1050,150,fill = "green")
    
    P1HPNum = s.create_text(191,171,text = "10/10",fill = "grey",font = "Arial 20")
    P1HPNumShade = s.create_text(190,170,text = "10/10",fill = "black",font = "Arial 20")

    P2HPNum = s.create_text(841,171,text = "10/10",fill = "grey",font = "Arial 20")
    P2HPNumShade = s.create_text(840,170,text = "10/10",fill = "black",font = "Arial 20")
    
        
def UpdateHealthBars(): #UPDATES HEALTH BARS BASED ON CURRENT PLAYER 1 AND PLAYER 2 HP LEVELS

    global P1HP,P2HP,P1HPNum,P1HPNumShade,P2HPNum,P2HPNumShade,P1Life,P2Life

    s.delete(P1HP,P2HP,P1HPNum,P1HPNumShade,P2HPNum,P2HPNumShade)

    #COLOUR OF THE HEALTH BAR IS DETERMINED BY THE HP LEVEL

    if P1Life > 6:
        c = "green"
    elif P1Life > 3:
        c = "yellow"
    else:
        c = "red"

    if P2Life > 6:
        c2 = "green"
    elif P2Life > 3:
        c2 = "yellow"
    else:
        c2 = "red"

    if P1Life > 0:
        P1HP = s.create_rectangle(150,100,150 + P1Life*25,150,fill = c)
    if P2Life > 0:
        P2HP = s.create_rectangle(800,100,800 + P2Life*25,150,fill = c2)

    if P1Life < 0:
        P1Life = 0
    if P2Life < 0:
        P2Life = 0

    P1HPNum = s.create_text(191,171,text = str(P1Life) + "/10",fill = "grey",font = "Arial 20")
    P1HPNumShade = s.create_text(190,170,text = str(P1Life) + "/10",fill = "black",font = "Arial 20")

    P2HPNum = s.create_text(841,171,text = str(P2Life) + "/10",fill = "grey",font = "Arial 20")
    P2HPNumShade = s.create_text(840,170,text = str(P2Life) + "/10",fill = "black",font = "Arial 20")

    
def SetInitialValues(): #SETS UP VARIOUS GENERAL VARIABLES AS WELL AS PLAYER 1'S VARIABLES

    global tankW,tankH,tankX,tankY,tankR,tankSpeed,tankSETTheta,tankTheta,tankTopR,CannonW,CannonH,TreadW,TreadH,tank,tankTop,Cannon,TreadR,TreadL
    global AmmoSpeed,AmmoR,AmmoParticles,AmmoXs,AmmoYs,AmmoThetas,X3,Y3,X4,Y4,Escape,LastFireTime,FiringRate,TankColors,TankC,Ic,AmmoOwners
    global xR1,yR1,xR2,yR2,xL3,yL3,xL4,yL4
    global P1Life,CountdownCheck,Craters,Collisions,P1Up,P1Down,P1Left,P1Right,P1Firing,AI
    global WallHitMoves,LastWallHit

    AI = True 
        
    #USED FOR AI
    
    WallHitMoves = [0,0,0,0] #IN ORDER: UP, DOWN, LEFT, RIGHT
    LastWallHit = 0

    #TANK VARIABLES
    
    tankW = 30 
    tankH = 50
    
    #STARTING POSITION
    
    tankX = 75     
    tankY = 825
    tankR = ((tankW**2 + tankH**2)**0.5)/2
    tankSpeed = 5
    tankSETTheta = atan(tankW/tankH)
    tankTheta = 0

    tankTopR = 10

    CannonW = 10
    CannonH = 20

    TreadW = 12
    TreadH = 60

    P1Life = 10

    #VARIABLES FOR AMMO AND CRATERS

    AmmoSpeed = 10
    AmmoR = 5
    AmmoParticles = []
    AmmoXs = []
    AmmoYs = []
    AmmoThetas = []
    AmmoOwners = []

    Craters = []

    #MOVEMENT VARIABLES

    P1Up = False
    P1Down = False
    P1Left = False
    P1Right = False

    P1Firing = False

    Collisions = []

    #TANK COLOUR VARIABLES

    TankColors = ["red","orange","green","cyan","purple"]
        
    Ic = 0
    TankC = TankColors[Ic]

    #FIRING RATE VARIABLES

    LastFireTime = clock()
    FiringRate = 1 #IN SECONDS

    CountdownCheck = True

    Escape = False

    #TANK BODY VALUES

    theta1 = tankTheta - tankSETTheta
    theta2 = tankTheta + tankSETTheta

    xA = tankX + cos(theta1)*tankR
    xB = tankX + cos(theta2)*tankR
    yA = tankY - sin(theta1)*tankR
    yB = tankY - sin(theta2)*tankR

    xA2 = tankX - cos(theta1)*tankR
    xB2 = tankX - cos(theta2)*tankR
    yA2 = tankY + sin(theta1)*tankR
    yB2 = tankY + sin(theta2)*tankR

    #TANK CANNON VALUES

    X1 = tankX + sin(tankTheta)*CannonW/2
    Y1 = tankY + cos(tankTheta)*CannonW/2
    X2 = tankX - sin(tankTheta)*CannonW/2
    Y2 = tankY - cos(tankTheta)*CannonW/2

    X3 = X2 + cos(tankTheta)*CannonH
    Y3 = Y2 - sin(tankTheta)*CannonH
    X4 = X1 + cos(tankTheta)*CannonH
    Y4 = Y1 - sin(tankTheta)*CannonH

    #TANK TREAD VALUES

    #RIGHT TREAD

    Xref = tankX + sin(tankTheta)*(tankW/2 + TreadW)
    Yref = tankY + cos(tankTheta)*(tankW/2 + TreadW)

    xR1 = Xref - cos(tankTheta)*TreadH/2
    yR1 = Yref + sin(tankTheta)*TreadH/2
    xR2 = Xref + cos(tankTheta)*TreadH/2
    yR2 = Yref - sin(tankTheta)*TreadH/2

    xR3 = xR2 - sin(tankTheta)*TreadW
    yR3 = yR2 - cos(tankTheta)*TreadW
    xR4 = xR1 - sin(tankTheta)*TreadW
    yR4 = yR1 - cos(tankTheta)*TreadW

    #LEFT TREAD

    Xref = tankX - sin(tankTheta)*(tankW/2)
    Yref = tankY - cos(tankTheta)*(tankW/2)

    xL1 = Xref - cos(tankTheta)*TreadH/2
    yL1 = Yref + sin(tankTheta)*TreadH/2
    xL2 = Xref + cos(tankTheta)*TreadH/2
    yL2 = Yref - sin(tankTheta)*TreadH/2

    xL3 = xL2 - sin(tankTheta)*TreadW
    yL3 = yL2 - cos(tankTheta)*TreadW
    xL4 = xL1 - sin(tankTheta)*TreadW
    yL4 = yL1 - cos(tankTheta)*TreadW

    #CREATES PLAYER 1'S TANK

    tank = s.create_polygon(xA,yA,xB,yB,xA2,yA2,xB2,yB2,fill = TankC,outline = "black",width = 2)
    Cannon = s.create_polygon(X1,Y1,X2,Y2,X3,Y3,X4,Y4,fill = TankC,outline = "black",width = 2)
    tankTop = s.create_oval(tankX - tankTopR,tankY - tankTopR,tankX + tankTopR,tankY + tankTopR,fill = TankC,width = 2)
    TreadR = s.create_polygon(xR1,yR1,xR2,yR2,xR3,yR3,xR4,yR4,fill = "black",width = 2)
    TreadL = s.create_polygon(xL1,yL1,xL2,yL2,xL3,yL3,xL4,yL4,fill = "black",width = 2)


def SetInitialValuesP2(): #INITIAL SETUP FOR PLAYER 2

    global P2tankX,P2tankY,P2tankTheta,P2tank,P2tankTop,P2Cannon,P2TreadR,P2TreadL
    global P2X3,P2Y3,P2X4,P2Y4,P2TankC,P2Ic,P2LastFireTime
    global P2xR1,P2yR1,P2xR2,P2yR2,P2xL3,P2yL3,P2xL4,P2yL4,TESTP2xR1,TESTP2yR1,TESTP2xR2,TESTP2yR2,TESTP2xL3,TESTP2yL3,TESTP2xL4,TESTP2yL4
    global P2Life,P2Up,P2Down,P2Left,P2Right,P2Firing

    #STARTING POSITION
    
    P2tankX = 1125      
    P2tankY = 275
    P2tankTheta = radians(180)

    #PLAYER 2'S COLOUR

    P2Ic = (Ic + 1) % len(TankColors)
    P2TankC = TankColors[P2Ic]

    P2LastFireTime = clock()

    P2Life = 10
    
    P2Up = False
    P2Down = False
    P2Left = False
    P2Right = False

    P2Firing = False

    #TANK BODY VALUES

    P2theta1 = P2tankTheta - tankSETTheta
    P2theta2 = P2tankTheta + tankSETTheta

    P2xA = P2tankX + cos(P2theta1)*tankR
    P2xB = P2tankX + cos(P2theta2)*tankR
    P2yA = P2tankY - sin(P2theta1)*tankR
    P2yB = P2tankY - sin(P2theta2)*tankR

    P2xA2 = P2tankX - cos(P2theta1)*tankR
    P2xB2 = P2tankX - cos(P2theta2)*tankR
    P2yA2 = P2tankY + sin(P2theta1)*tankR
    P2yB2 = P2tankY + sin(P2theta2)*tankR

    #TANK CANNON VALUES

    P2X1 = P2tankX + sin(P2tankTheta)*CannonW/2
    P2Y1 = P2tankY + cos(P2tankTheta)*CannonW/2
    P2X2 = P2tankX - sin(P2tankTheta)*CannonW/2
    P2Y2 = P2tankY - cos(P2tankTheta)*CannonW/2

    P2X3 = P2X2 + cos(P2tankTheta)*CannonH
    P2Y3 = P2Y2 - sin(P2tankTheta)*CannonH
    P2X4 = P2X1 + cos(P2tankTheta)*CannonH
    P2Y4 = P2Y1 - sin(P2tankTheta)*CannonH

    #TANK TREAD VALUES

    #RIGHT TREAD

    P2Xref = P2tankX + sin(P2tankTheta)*(tankW/2 + TreadW)
    P2Yref = P2tankY + cos(P2tankTheta)*(tankW/2 + TreadW)

    P2xR1 = P2Xref - cos(P2tankTheta)*TreadH/2
    P2yR1 = P2Yref + sin(P2tankTheta)*TreadH/2
    P2xR2 = P2Xref + cos(P2tankTheta)*TreadH/2
    P2yR2 = P2Yref - sin(P2tankTheta)*TreadH/2

    P2xR3 = P2xR2 - sin(P2tankTheta)*TreadW
    P2yR3 = P2yR2 - cos(P2tankTheta)*TreadW
    P2xR4 = P2xR1 - sin(P2tankTheta)*TreadW
    P2yR4 = P2yR1 - cos(P2tankTheta)*TreadW

    #LEFT TREAD

    P2Xref = P2tankX - sin(P2tankTheta)*(tankW/2)
    P2Yref = P2tankY - cos(P2tankTheta)*(tankW/2)

    P2xL1 = P2Xref - cos(P2tankTheta)*TreadH/2
    P2yL1 = P2Yref + sin(P2tankTheta)*TreadH/2
    P2xL2 = P2Xref + cos(P2tankTheta)*TreadH/2
    P2yL2 = P2Yref - sin(P2tankTheta)*TreadH/2

    P2xL3 = P2xL2 - sin(P2tankTheta)*TreadW
    P2yL3 = P2yL2 - cos(P2tankTheta)*TreadW
    P2xL4 = P2xL1 - sin(P2tankTheta)*TreadW
    P2yL4 = P2yL1 - cos(P2tankTheta)*TreadW

    #INITIAL TEST VALUES

    TESTP2xR1 = P2xR1
    TESTP2yR1 = P2yR1
    TESTP2xR2 = P2xR2
    TESTP2yR2 = P2yR2

    TESTP2xL3 = P2xL3
    TESTP2yL3 = P2yL3
    TESTP2xL4 = P2xL4
    TESTP2yL4 = P2yL4

    #CREATES PLAYER 2'S TANK
    
    P2tank = s.create_polygon(P2xA,P2yA,P2xB,P2yB,P2xA2,P2yA2,P2xB2,P2yB2,fill = P2TankC,outline = "black",width = 2)
    P2Cannon = s.create_polygon(P2X1,P2Y1,P2X2,P2Y2,P2X3,P2Y3,P2X4,P2Y4,fill = P2TankC,outline = "black",width = 2)
    P2tankTop = s.create_oval(P2tankX - tankTopR,P2tankY - tankTopR,P2tankX + tankTopR,P2tankY + tankTopR,fill = P2TankC,width = 2)
    P2TreadR = s.create_polygon(P2xR1,P2yR1,P2xR2,P2yR2,P2xR3,P2yR3,P2xR4,P2yR4,fill = "black",width = 2)
    P2TreadL = s.create_polygon(P2xL1,P2yL1,P2xL2,P2yL2,P2xL3,P2yL3,P2xL4,P2yL4,fill = "black",width = 2)
    

def CheckIfReloaded(PlayerNumber): #CHECKS IF A PLAYER HAS RELOADED

    global LastFireTime,P2LastFireTime

    if PlayerNumber == 1: #IN MANY SCENARIOS THE PLAYER NUMBER MUST BE CONSIDERED AND OTHER CODE MUST BE RUN FOR THE OTHER PLAYER

        elapsed_time = clock() - LastFireTime #CHECKS TO SEE IF THE PLAYER RELOADED BASED ON THE LAST TIME THEY FIRED

        if elapsed_time >= FiringRate:
            LastFireTime = clock()
            return True
        
        return False

    else:

        elapsed_time = clock() - P2LastFireTime

        if elapsed_time >= FiringRate:
            P2LastFireTime = clock()
            return True
        
        return False    

def CheckIfPlayerHit(): #CHECKS IF A PLAYER HAS BEEN HIT 

    global P1Life,P2Life

    if len(AmmoParticles) > 0:
            
        Hit = False
        Hit2 = False
        I = -1 
        I2 = -1
        
        for i in range(0,len(AmmoParticles)): #CHECKS EVERY AMMO PARTICLE

            if AmmoOwners[i] == 2:
                if CheckHit(xR1,yR1,xR2,yR2,xL3,yL3,xL4,yL4,AmmoXs[i],AmmoYs[i]) == True:
                    Hit = CheckHit(xR1,yR1,xR2,yR2,xL3,yL3,xL4,yL4,AmmoXs[i],AmmoYs[i])
                    I = i
                    
            else:
                if CheckHit(P2xR1,P2yR1,P2xR2,P2yR2,P2xL3,P2yL3,P2xL4,P2yL4,AmmoXs[i],AmmoYs[i]) == True:
                    Hit2 = CheckHit(P2xR1,P2yR1,P2xR2,P2yR2,P2xL3,P2yL3,P2xL4,P2yL4,AmmoXs[i],AmmoYs[i])
                    I2 = i
                    
                    
        if Hit == True or Hit2 == True: #RUNS THE ANIMATION AS WELL
            
            if Hit == True and Hit2 == True: #IF BOTH PLAYERS HIT
                
                for i in range(0,80):
                    explosion = s.create_oval(AmmoXs[I] - i,AmmoYs[I] - i,AmmoXs[I] + i,AmmoYs[I] + i,fill = "white")
                    explosion2 = s.create_oval(AmmoXs[I2] - i,AmmoYs[I2] - i,AmmoXs[I2] + i,AmmoYs[I2] + i,fill = "white")
                    s.update()
                    sleep(0.00075)
                    s.delete(explosion,explosion2)

                if GetDist(P2tankX,P2tankY,AmmoXs[I],AmmoYs[I]) <= 80:
                    P2Life -= 1

                s.delete(AmmoParticles[I])
                AmmoXs[I] = "A"
                AmmoXs.remove(AmmoXs[I])
                AmmoYs[I] = "A"
                AmmoYs.remove(AmmoYs[I])
                AmmoParticles.remove(AmmoParticles[I]) 
                AmmoThetas[I] = "A"
                AmmoThetas.remove(AmmoThetas[I])
                AmmoOwners[I] = 0
                AmmoOwners.remove(AmmoOwners[I])

                if I < I2:
                    I2 -= 1

                if GetDist(tankX,tankY,AmmoXs[I2],AmmoYs[I2]) <= 80:
                    P1Life -= 1

                s.delete(AmmoParticles[I2])
                AmmoXs[I2] = "A"
                AmmoXs.remove(AmmoXs[I2])
                AmmoYs[I2] = "A"
                AmmoYs.remove(AmmoYs[I2])
                AmmoParticles.remove(AmmoParticles[I2])
                AmmoThetas[I2] = "A"
                AmmoThetas.remove(AmmoThetas[I2])
                AmmoOwners[I2] = 0
                AmmoOwners.remove(AmmoOwners[I2])
                
                P1Life -= 2
                P2Life -= 2

            elif Hit == True: #IF PLAYER 1 HAS BEEN HIT
                
                for i in range(0,100):
                    explosion = s.create_oval(AmmoXs[I] - i,AmmoYs[I] - i,AmmoXs[I] + i,AmmoYs[I] + i,fill = "white")
                    s.update()
                    sleep(0.00075)
                    s.delete(explosion)

                if GetDist(P2tankX,P2tankY,AmmoXs[I],AmmoYs[I]) <= 80:
                    P2Life -= 1

                s.delete(AmmoParticles[I])
                AmmoXs[I] = "A"
                AmmoXs.remove(AmmoXs[I])
                AmmoYs[I] = "A"
                AmmoYs.remove(AmmoYs[I])
                AmmoParticles.remove(AmmoParticles[I])
                AmmoThetas[I] = "A"
                AmmoThetas.remove(AmmoThetas[I])
                AmmoOwners[I] = 0
                AmmoOwners.remove(AmmoOwners[I])

                P1Life -= 2

            else: #IF PLAYER 2 HAS BEEN HIT
                
                for i in range(0,100):
                    explosion2 = s.create_oval(AmmoXs[I2] - i,AmmoYs[I2] - i,AmmoXs[I2] + i,AmmoYs[I2] + i,fill = "white")
                    s.update()
                    sleep(0.00075)
                    s.delete(explosion2)

                if GetDist(tankX,tankY,AmmoXs[I2],AmmoYs[I2]) <= 80:
                    P1Life -= 1

                s.delete(AmmoParticles[I2])
                AmmoXs[I2] = "A"
                AmmoXs.remove(AmmoXs[I2])
                AmmoYs[I2] = "A"
                AmmoYs.remove(AmmoYs[I2])
                AmmoParticles.remove(AmmoParticles[I2])
                AmmoThetas[I2] = "A"
                AmmoThetas.remove(AmmoThetas[I2])
                AmmoOwners[I2] = 0
                AmmoOwners.remove(AmmoOwners[I2])

                P2Life -= 2

            UpdateHealthBars() #UPDATES HEALTH BARS


def MakeNewAmmo(PlayerNumber): #MAKES A NEW AMMO     
    
    global AmmoParticles,AmmoXs,AmmoYs,AmmoThetas,AmmoOwners

    if PlayerNumber == 1:
        X = (X3 + X4)/2 #CREATES AMMO AT TIP OF CANNON
        Y = (Y3 + Y4)/2
        AmmoThetas.append(tankTheta)

    else:
        X = (P2X3 + P2X4)/2
        Y = (P2Y3 + P2Y4)/2
        AmmoThetas.append(P2tankTheta)
    
    AmmoXs.append(X)
    AmmoYs.append(Y)
    AmmoParticles.append(0)
    AmmoOwners.append(PlayerNumber)
    

def UpdateAmmoPosition(): #UPDATES AMMO POSITIONS
    
    global AmmoParticles,AmmoXs,AmmoYs
    
    for i in range(0,len(AmmoParticles)):
        AmmoXs[i] += cos(AmmoThetas[i])*AmmoSpeed
        AmmoYs[i] -= sin(AmmoThetas[i])*AmmoSpeed


def DrawAmmo(): #DRAWS THE AMMO PARTICLES
    
    for i in range(len(AmmoParticles)):
        
        if AmmoOwners[i] == 1:
            C = TankC
        else:
            C = P2TankC
        
        AmmoParticles[i] = s.create_oval(AmmoXs[i] - AmmoR,AmmoYs[i] - AmmoR,AmmoXs[i] + AmmoR,AmmoYs[i] + AmmoR,fill = C)


def deleteAmmo(): #DELETES THE AMMO PARTICLES
    
    for i in range(len(AmmoParticles)):
        s.delete(AmmoParticles[i])


def CreateWalls(): #MAP CREATED HERE

    global WallOrientations,WallLevels,WallMins,WallMaxs

    WallOrientations = []
    WallLevels = []
    WallMins = []
    WallMaxs = []

    #MAP BORDER
    
    DrawWall("h",200,0,1200)
    DrawWall("h",900,0,1200) 
    DrawWall("v",0,200,900)
    DrawWall("v",1200,200,900)

    #WALLS CREATING A "STARTING BASE" FOR EACH PLAYER
      
    DrawWall("h",350,900,1200)
    DrawWall("h",750,0,300)

    #OBSTACLES IN THE MIDDLE OF THE MAP
    
    DrawWall("v",300,340,410)
    DrawWall("v",300,540,610)
    DrawWall("v",900,490,560)
    DrawWall("v",900,690,760)

    DrawWall("h",500,440,510)
    DrawWall("h",600,690,760)

    
def CheckIfHitWall(PlayerNumber): #CHECK IF A PLAYER HAS HIT A WALL, RETURNS TRUE OR FALSE
    
    if PlayerNumber == 1:
        
        x1 = TESTxR1
        y1 = TESTyR1
        x2 = TESTxR2
        y2 = TESTyR2
        x3 = TESTxL3
        y3 = TESTyL3
        x4 = TESTxL4
        y4 = TESTyL4

    else:

        x1 = TESTP2xR1
        y1 = TESTP2yR1
        x2 = TESTP2xR2
        y2 = TESTP2yR2
        x3 = TESTP2xL3
        y3 = TESTP2yL3
        x4 = TESTP2xL4
        y4 = TESTP2yL4

    for i in range(0,len(WallOrientations)): #CHECKS EVERY WALL

        EqA = getEquationOfLine(x1,y1,x2,y2) #USES INEQUALITIES 
        EqB = getEquationOfLine(x2,y2,x3,y3)
        EqC = getEquationOfLine(x3,y3,x4,y4)
        EqD = getEquationOfLine(x4,y4,x1,y1)
        
        if WallOrientations[i] == "h": #IF WALL IS HORIZONTAL

            if EqA[0] == "undefined" or EqC[0] == "undefined" or EqB[0] == 0 or EqD[0] == 0: #TANK FACING UP
                
                if WallMins[i] <= x2 <= WallMaxs[i] or WallMins[i] <= x3 <= WallMaxs[i]: 
                    if y1 < WallLevels[i] and y2 > WallLevels[i]:
                        return True
                    elif y1 > WallLevels[i] and y2 < WallLevels[i]:
                        return True

            elif EqA[0] == 0 or EqC[0] == 0 or EqB[0] == "undefined" or EqD[0] == "undefined": #TANK FACING THE SIDE
                
                if WallMins[i] <= x1 <= WallMaxs[i] or WallMins[i] <= x2 <= WallMaxs[i]:
                    if y2 < WallLevels[i] and y3 > WallLevels[i]:
                        return True
                    elif y2 > WallLevels[i] and y3 < WallLevels[i]:
                        return True
                    
            else: #TANK ON AN ANGLE

                X = (WallLevels[i] - EqA[1])/EqA[0]
                if WallMins[i] <= X <= WallMaxs[i]:
                    if x1 <= X <= x2 or x2 <= X <= x1:
                        return True
                X = (WallLevels[i] - EqB[1])/EqB[0]
                if WallMins[i] <= X <= WallMaxs[i]:
                    if x2 <= X <= x3 or x3 <= X <= x2:
                        return True
                X = (WallLevels[i] - EqC[1])/EqC[0]
                if WallMins[i] <= X <= WallMaxs[i]:
                    if x3 <= X <= x4 or x4 <= X <= x3:
                        return True
                X = (WallLevels[i] - EqD[1])/EqD[0]
                if WallMins[i] <= X <= WallMaxs[i]:
                    if x1 <= X <= x4 or x4 <= X <= x1:
                        return True
                    
        else: #IF WALL IS VERTICAL

            if EqA[0] == "undefined" or EqC[0] == "undefined" or EqB[0] == 0 or EqD[0] == 0: #TANK FACING UP
                
                if WallMins[i] <= y1 <= WallMaxs[i] or WallMins[i] <= y2 <= WallMaxs[i]: 
                    if x2 < WallLevels[i] and x3 > WallLevels[i]:
                        return True
                    elif x2 > WallLevels[i] and x3 < WallLevels[i]:
                        return True

            elif EqA[0] == 0 or EqC[0] == 0 or EqB[0] == "undefined" or EqD[0] == "undefined": #TANK FACING THE SIDE
                
                if WallMins[i] <= y2 <= WallMaxs[i] or WallMins[i] <= y3 <= WallMaxs[i]:
                    if x1 < WallLevels[i] and x2 > WallLevels[i]:
                        return True
                    elif x1 > WallLevels[i] and x2 < WallLevels[i]:
                        return True
                    
            else: #TANK ON AN ANGLE
                
                Y = EqA[0]*WallLevels[i] + EqA[1]
                if WallMins[i] <= Y <= WallMaxs[i]:
                    if y1 <= Y <= y2 or y2 <= Y <= y1:
                        return True
                Y = EqB[0]*WallLevels[i] + EqB[1]
                if WallMins[i] <= Y <= WallMaxs[i]:
                    if y2 < Y < y3 or y3 < Y < y2: #MUST ACCOUNT FOR ANOTHER PYTHON BUG
                        return True
                Y = EqC[0]*WallLevels[i] + EqC[1]
                if WallMins[i] <= Y <= WallMaxs[i]:
                    if y3 <= Y <= y4 or y4 <= Y <= y3:
                        return True
                Y = EqD[0]*WallLevels[i] + EqD[1]
                if WallMins[i] <= Y <= WallMaxs[i]:
                    if y1 < Y < y4 or y4 < Y < y1: #MUST ACCOUNT FOR ANOTHER PYTHON BUG
                        return True

    return False


def GetDist(x1,y1,x2,y2): #RETURNS DISTANCE BETWEEN 2 POINTS

    D = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    
    return D


def CheckPlayerOverlap(PlayerNumber): #CHECKS IF PLAYERS ARE OVERLAPPING, RETURNS TRUE OR FALSE

    global P1Life,P2Life,Collisions

    if GetDist(tankX,tankY,P2tankX,P2tankY) <= tankR*2: #CHECKS FOR COLLISIONS
        
        Collisions.append(1)
        
        if Collisions[len(Collisions)-1] != Collisions[len(Collisions) - 2]: #IF ALREADY COLLIDED, DOES NOT COUNT THE COLLISION MORE THAN ONCE
            P1Life -= 2 #COLLISION DAMAGE
            P2Life -= 2
            UpdateHealthBars()
            
        return True

    Collisions.append(0)

    return False
    

def CheckIfAmmoHitWall(): #CHECKS IF AMMO HITS WALLS OR OTHER AMMO, THEN RUNS AN ANIMATION AND DELETES AMMO

    i = 0
    
    while i < len(AmmoParticles): #CHECKS EVERY AMMO
        
        x1 = AmmoXs[i] #CONSIDERS CURRENT AMMO POSITION AND FUTURE POSITION
        y1 = AmmoYs[i]
        x2 = x1 + cos(AmmoThetas[i])*AmmoSpeed
        y2 = y1 - sin(AmmoThetas[i])*AmmoSpeed
        removed = False
        
        for j in range(0,len(WallOrientations)): #CHECKS EVERY WALL
            
            if WallOrientations[j] == "h": #IF WALL IS HORIZONTAL

                if WallMins[j] <= x1 <= WallMaxs[j]: 
                
                    if y1 <= WallLevels[j] + AmmoR and y2 >= WallLevels[j] - AmmoR or y1 >= WallLevels[j] - AmmoR and y2 <= WallLevels[j] + AmmoR: #USES INEQUALITIES
                        
                        crater = s.create_oval(AmmoXs[i] - 10,WallLevels[j] - 10,AmmoXs[i] + 10,WallLevels[j] + 10,fill = "black")
                        Craters.append(crater)
                        s.delete(AmmoParticles[i])
                        AmmoParticles.remove(AmmoParticles[i])
                        AmmoXs[i] = "A"
                        AmmoXs.remove(AmmoXs[i])
                        AmmoYs[i] = "A"
                        AmmoYs.remove(AmmoYs[i])
                        AmmoThetas[i] = "A"
                        AmmoThetas.remove(AmmoThetas[i])
                        AmmoOwners[i] = 0 #MUST RESET VALUES BEFORE REMOVING FROM AN ARRAY OTHERWISE BUG OCCURS
                        AmmoOwners.remove(AmmoOwners[i])
                        removed = True

            else: #IF WALL IS VERTICAL

                if WallMins[j] <= y1 <= WallMaxs[j]: 

                    if x1 <= WallLevels[j] + AmmoR and x2 >= WallLevels[j] - AmmoR or x1 >= WallLevels[j] - AmmoR and x2 <= WallLevels[j] + AmmoR:
                        
                        crater = s.create_oval(WallLevels[j] - 10,AmmoYs[i] - 10,WallLevels[j] + 10,AmmoYs[i] + 10,fill = "black")
                        Craters.append(crater)
                        s.delete(AmmoParticles[i])
                        AmmoParticles.remove(AmmoParticles[i])
                        AmmoXs[i] = "A"
                        AmmoXs.remove(AmmoXs[i])
                        AmmoYs[i] = "A"
                        AmmoYs.remove(AmmoYs[i])
                        AmmoThetas[i] = "A"
                        AmmoThetas.remove(AmmoThetas[i])
                        AmmoOwners[i] = 0
                        AmmoOwners.remove(AmmoOwners[i])
                        removed = True

        if removed == False:
            
            i += 1


def KeyPressHandler(event): #HANDLES KEYSTROKES                
    
    global tankX,tankY,tankTheta,P2tankX,P2tankY,P2tankTheta,Escape

    global P1Up,P1Down,P1Left,P1Right,P1Firing,P2Up,P2Down,P2Left,P2Right,P2Firing

    if CountdownCheck == False: #DOES NOT ALLOW INPUT DURING COUNTDOWN

        if event.keysym.lower() == "w": #.lower() USED IN CASE THE CAPS LOCK IS ON
            P1Up = True

        elif event.keysym.lower() == "s":
            P1Down = True

        elif event.keysym.lower() == "a":
            P1Left = True

        elif event.keysym.lower() == "d":
            P1Right = True

        elif event.keysym.lower() == "q":
            P1Firing = True

        elif event.keysym == "Up" and AI == False:
            P2Up = True
            
        elif event.keysym == "Down" and AI == False:
            P2Down = True

        elif event.keysym == "Left" and AI == False:
            P2Left = True

        elif event.keysym == "Right" and AI == False:
            P2Right = True

        elif event.keysym.lower() == "m" and AI == False:
            P2Firing = True

        elif event.keysym == "Escape":
            Escape = True


def KeyReleaseHandler(event): #HANDLES KEY-RELEASES

    global P1Up,P1Down,P1Left,P1Right,P1Firing,P2Up,P2Down,P2Left,P2Right,P2Firing

    if CountdownCheck == False: #DOES NOT ALLOW INPUT DURING COUNTDOWN

        if event.keysym.lower() == "w":
            P1Up = False

        elif event.keysym.lower() == "s":
            P1Down = False

        elif event.keysym.lower() == "a":
            P1Left = False

        elif event.keysym.lower() == "d":
            P1Right = False

        elif event.keysym.lower() == "q":
            P1Firing = False

        elif event.keysym == "Up" and AI == False:
            P2Up = False
            
        elif event.keysym == "Down" and AI == False:
            P2Down = False

        elif event.keysym == "Left" and AI == False:
            P2Left = False

        elif event.keysym == "Right" and AI == False:
            P2Right = False

        elif event.keysym.lower() == "m" and AI == False:
            P2Firing = False


def CreateMainScreen(): #CREATES MAIN SCREEN GRAPHICS
    
    global Ready,bg,title,buttonA,buttonAText,buttonB,buttonBText

    Ready = False

    #MAIN SCREEN GRAPHICS
    
    bg = s.create_rectangle(0,0,1200,900,fill = "black")
    title = s.create_text(600,200,text = "TANKS",fill = "white",font = "Arial 150 bold")
    buttonA = s.create_rectangle(50,450,550,650,fill = "red")
    buttonAText = s.create_text(300,550,text = "1 Player Mode",fill = "black",font = "Arial 40 bold")
    buttonB = s.create_rectangle(650,450,1150,650,fill = "blue")
    buttonBText = s.create_text(900,550,text = "2 Player Mode",fill = "black",font = "Arial 40 bold")
    s.update()


def DeleteMainScreen(): #DELETES MAINSCREEN

    s.delete(bg,title,buttonA,buttonAText,buttonB,buttonBText)


def ClickHandler(event): #HANDLES CLICKS  

    global TankC,Ic,P2TankC,P2Ic,P1HPLabelC,P2HPLabelC,AI,Ready

    X = event.x #CURRENT MOUSE POSITION
    Y = event.y

    if CountdownCheck == True and Ready == False: #DETECTS BUTTON PRESSES ON MAIN SCREEN

        if 50 <= X <= 550 and 450 <= Y <= 650:
            AI = True
            Ready = True
        elif 650 <= X <= 1150 and 450 <= Y <= 650:
            AI = False
            Ready = True
    
    elif CountdownCheck == False and Ready == True: #CHANGES PLAYER COLOUR

        d = ((X - tankX)**2 + (Y - tankY)**2)**0.5

        d2 = ((X - P2tankX)**2 + (Y - P2tankY)**2)**0.5

        if d <= tankTopR:
            Ic += 1
            Ic = Ic % len(TankColors)
            if Ic == P2Ic: #ENSURES BOTH TANKS HAVE DIFFERENT COLOURS
                Ic += 1
                Ic = Ic % len(TankColors)
            TankC = TankColors[Ic]

        elif d2 <= tankTopR:
            P2Ic += 1
            P2Ic = P2Ic % len(TankColors)
            if P2Ic == Ic:
                P2Ic += 1
                P2Ic = P2Ic % len(TankColors)
            P2TankC = TankColors[P2Ic]

        s.delete(P1HPLabelC,P2HPLabelC)
        
        P1HPLabelC = s.create_oval(362,62,388,88,fill = TankC)
        P2HPLabelC = s.create_oval(1012,62,1038,88,fill = P2TankC)


def updateTankPosition(): #UPDATES PLAYER 1'S POSITION
    
    global tank,tankTop,Cannon,TreadR,TreadL,X3,Y3,X4,Y4
    global xR1,yR1,xR2,yR2,xL3,yL3,xL4,yL4,TESTxR1,TESTyR1,TESTxR2,TESTyR2,TESTxL3,TESTyL3,TESTxL4,TESTyL4
    global tankX,tankY,tankTheta
    global P1Up,P1Down,P1Left,P1Right

    if P1Up == True:
        tankX += cos(tankTheta)*tankSpeed
        tankY -= sin(tankTheta)*tankSpeed
        
    if P1Down == True:
        tankX -= cos(tankTheta)*tankSpeed
        tankY += sin(tankTheta)*tankSpeed

    if P1Left == True:
        tankTheta += radians(3)

    if P1Right == True:
        tankTheta -= radians(3)

    #CALCULATE MAIN 4 POUNTS FIRST
    #TESTS TO CHECK IF THE MOVE CAN BE PERFORMED, IF NOT IT REVERSES THE MOVE
    #THESE TESTS ARE RUN SO THAT ALL THE POINTS DO NOT HAVE TO BE RECALCULATED

    Xref = tankX + sin(tankTheta)*(tankW/2 + TreadW)
    Yref = tankY + cos(tankTheta)*(tankW/2 + TreadW)

    TESTxR1 = Xref - cos(tankTheta)*TreadH/2
    TESTyR1 = Yref + sin(tankTheta)*TreadH/2
    TESTxR2 = Xref + cos(tankTheta)*TreadH/2
    TESTyR2 = Yref - sin(tankTheta)*TreadH/2

    Xref = tankX - sin(tankTheta)*(tankW/2)
    Yref = tankY - cos(tankTheta)*(tankW/2)

    TESTxL1 = Xref - cos(tankTheta)*TreadH/2
    TESTyL1 = Yref + sin(tankTheta)*TreadH/2
    TESTxL2 = Xref + cos(tankTheta)*TreadH/2
    TESTyL2 = Yref - sin(tankTheta)*TreadH/2

    TESTxL3 = TESTxL2 - sin(tankTheta)*TreadW
    TESTyL3 = TESTyL2 - cos(tankTheta)*TreadW
    TESTxL4 = TESTxL1 - sin(tankTheta)*TreadW
    TESTyL4 = TESTyL1 - cos(tankTheta)*TreadW

    #IF HIT WALL, STOPS MOVING

    if CheckIfHitWall(1) == True or CheckPlayerOverlap(1) == True:
        
        if P1Up == True:
            tankX -= cos(tankTheta)*tankSpeed
            tankY += sin(tankTheta)*tankSpeed
        P1Up = False
            
        if P1Down == True:
            tankX += cos(tankTheta)*tankSpeed
            tankY -= sin(tankTheta)*tankSpeed
        P1Down = False

        if P1Left == True:
            tankTheta -= radians(3)
        P1Left = False

        if P1Right == True:
            tankTheta += radians(3)
        P1Right = False
    
    #TANK BODY
    
    theta1 = tankTheta - tankSETTheta
    theta2 = tankTheta + tankSETTheta

    xA = tankX + cos(theta1)*tankR
    xB = tankX + cos(theta2)*tankR
    yA = tankY - sin(theta1)*tankR
    yB = tankY - sin(theta2)*tankR

    xA2 = tankX - cos(theta1)*tankR
    xB2 = tankX - cos(theta2)*tankR
    yA2 = tankY + sin(theta1)*tankR
    yB2 = tankY + sin(theta2)*tankR

    #CANNON

    X1 = tankX + sin(tankTheta)*CannonW/2
    Y1 = tankY + cos(tankTheta)*CannonW/2
    X2 = tankX - sin(tankTheta)*CannonW/2
    Y2 = tankY - cos(tankTheta)*CannonW/2
    
    X3 = X2 + cos(tankTheta)*CannonH
    Y3 = Y2 - sin(tankTheta)*CannonH
    X4 = X1 + cos(tankTheta)*CannonH
    Y4 = Y1 - sin(tankTheta)*CannonH

    #RIGHT TREAD
   
    Xref = tankX + sin(tankTheta)*(tankW/2 + TreadW)
    Yref = tankY + cos(tankTheta)*(tankW/2 + TreadW)

    xR1 = Xref - cos(tankTheta)*TreadH/2
    yR1 = Yref + sin(tankTheta)*TreadH/2
    xR2 = Xref + cos(tankTheta)*TreadH/2
    yR2 = Yref - sin(tankTheta)*TreadH/2

    xR3 = xR2 - sin(tankTheta)*TreadW
    yR3 = yR2 - cos(tankTheta)*TreadW
    xR4 = xR1 - sin(tankTheta)*TreadW
    yR4 = yR1 - cos(tankTheta)*TreadW

    #LEFT TREAD

    Xref = tankX - sin(tankTheta)*(tankW/2)
    Yref = tankY - cos(tankTheta)*(tankW/2)

    xL1 = Xref - cos(tankTheta)*TreadH/2
    yL1 = Yref + sin(tankTheta)*TreadH/2
    xL2 = Xref + cos(tankTheta)*TreadH/2
    yL2 = Yref - sin(tankTheta)*TreadH/2

    xL3 = xL2 - sin(tankTheta)*TreadW
    yL3 = yL2 - cos(tankTheta)*TreadW
    xL4 = xL1 - sin(tankTheta)*TreadW
    yL4 = yL1 - cos(tankTheta)*TreadW

    #DELETES OLD TANK PARTS

    s.delete(tank,Cannon,tankTop,TreadR,TreadL)

    #CREATES NEW TANK PARTS
    
    tank = s.create_polygon(xA,yA,xB,yB,xA2,yA2,xB2,yB2,fill = TankC,outline = "black",width = 2)
    Cannon = s.create_polygon(X1,Y1,X2,Y2,X3,Y3,X4,Y4,fill = TankC,outline = "black",width = 2)
    tankTop = s.create_oval(tankX - tankTopR,tankY - tankTopR,tankX + tankTopR,tankY + tankTopR,fill = TankC,width = 2)
    TreadR = s.create_polygon(xR1,yR1,xR2,yR2,xR3,yR3,xR4,yR4,fill = "black",width = 2)
    TreadL = s.create_polygon(xL1,yL1,xL2,yL2,xL3,yL3,xL4,yL4,fill = "black",width = 2)


def AIMove(): #DECENTLY SMART AI 

    global P2Up,P2Down,P2Left,P2Right,P2Firing,LastWallHit

    P2Up = False
    P2Down = False
    P2Left = False
    P2Right = False
    P2Firing = False

    EqMain = getEquationOfLine(tankX,tankY,P2tankX,P2tankY) #DRAWS AN IMAGINARY LINE BETWEEN THE CENTRE OF THE TWO TANKS

    #CHECKS IF ANY WALLS ARE BLOCKING THE OPPONENT
    #IF THERE IS A CLEAR PATH, ANGLES ITSELF ACCORDINGLY THEN FIRES

    #CHECKS IF WALL IS BLOCKING OPPONENT

    WallBlock = False

    if EqMain[0] == "undefined": #IF THE TANKS ARE VERTICALLY ALIGNED
        
        for i in range(0,len(WallOrientations)):
            if WallOrientations[i] == "h":
                if WallMins[i] <= EqMain[1] <= WallMaxs[i]: #USES MORE INEQUALITIES 
                    if tankY <= WallLevels[i] <= P2tankY or P2tankY <= WallLevels[i] <= tankY:
                        I = i
                        WallBlock = True
            else:
                if EqMain[1] == WallLevels[i]:
                    if tankY <= WallMins[i] <= P2tankY and tankY <= WallMaxs[i] <= P2tankY or P2tankY <= WallMins[i] <= tankY and P2tankY <= WallMaxs[i] <= tankY:
                        I = i
                        WallBlock = True
                    
    elif EqMain[0] == 0: #IF THE TANKS ARE HORIZONTALLY ALIGNED
        
        for i in range(0,len(WallOrientations)):
            if WallOrientations[i] == "h":
                if EqMain[1] == WallLevels[i]:
                    if tankX <= WallMins[i] <= P2tankX and tankX <= WallMaxs[i] <= P2tankX or P2tankX <= WallMins[i] <= tankX and P2tankX <= WallMaxs[i] <= tankX:
                        I = i
                        WallBlock = True
            else:
                if WallMins[i] <= EqMain[1] <= WallMaxs[i]:
                    if tankX <= WallLevels[i] <= P2tankX or P2tankX <= WallLevels[i] <= tankX:
                        I = i
                        WallBlock = True
                        
    else: #IF THE LINE BETWEEN THE TANKS IS ANGLED
        
        for i in range(0,len(WallOrientations)):
            if WallOrientations[i] == "h":
                X = (WallLevels[i] - EqMain[1])/EqMain[0]
                if WallMins[i] <= X <= WallMaxs[i]:
                    if tankX <= X <= P2tankX or P2tankX <= X <= tankX:
                        I = i
                        WallBlock = True
            else:
                Y = EqMain[0]*WallLevels[i] + EqMain[1]
                if WallMins[i] <= Y <= WallMaxs[i]:
                    if tankY <= Y <= P2tankY or P2tankY <= Y <= tankY:
                        I = i
                        WallBlock = True

    if CheckIfHitWall(2) == True or CheckPlayerOverlap(2) == True or LastWallHit > 10: #IF AN OBSTACLE HAS BEEN HIT RECENTLY

        if WallHitMoves[0] == 1:
            P2Down = True
        if WallHitMoves[1] == 1:
            P2Up = True
        if WallHitMoves[2] == 1:
            P2Right = True
        if WallHitMoves[3] == 1:
            P2Left = True
        LastWallHit -= 1

    #AI MOVEMENT
    #MOVES UP AND DOWN AND TURNS (LEFT AND RIGHT) TO MOVE INTO POSITION
            
    elif WallBlock == True or LastWallHit > 0:

        if LastWallHit > 0:
            LastWallHit -= 1 #CONTINUES TO CHECK IF WALL HAS BEEN HIT RECENTLY SO THE TANK CAN MOVE INTO POSITION INSTEAD OF AIMING
        
        PA = P2tankTheta % radians(360)
        
        #SIMPLE PATHFINDER ALGORITHM
            
        board = []
        
        #CREATES A GRID OUT OF THE MAP
        #FINDS A GOOD MOVE (FOR THE COMPUTER) FOR EACH TILE IN THE GRID
        
        for column in range(0,24): 
            board.append([])
            for row in range(0,14):
                board[column].append(0)

        #DETERMINES BOTH PLAYERS' POSITIONS
        
        OPPtankXSquare = int(tankX/50)
        OPPtankYSquare = int((tankY - 200)/50)
        AItankXSquare = int(P2tankX/50)
        AItankYSquare = int((P2tankY - 200)/50)
        
        for column in range(0,24): #ASSIGNS AN OPTIMAL MOVE FOR EACH TILE
            for row in range(0,14):
                if column == OPPtankXSquare:
                    if row < OPPtankYSquare:
                        board[column][row] = "Down"

                    else:
                        board[column][row] = "Up"

                elif column < OPPtankXSquare:
                    board[column][row] = "Right"

                else:
                    board[column][row] = "Left"
                    
        for i in range(0,len(WallOrientations)): #RE-ASSIGNS MOVES FOR CERTAIN TILES THAT ARE BORDERING WALLS
            
            if WallOrientations[i] == "h": #IF WALL IS HORIZONTAL
                
                BotRowSquare = int((WallLevels[i] - 200)/50)    
                TopRowSquare = BotRowSquare - 1
                if BotRowSquare > 13:
                    BotRowSquare = 13
                if TopRowSquare < 0:
                    TopRowSquare = 0
                MinSquare = int(WallMins[i]/50)
                MaxSquare = int(WallMaxs[i]/50)
                if MaxSquare > 23:
                    MaxSquare = 23
                if WallMins[i] % 50 == 0 and MinSquare > 0:
                    MinSquare -= 1
                iterations = MaxSquare - MinSquare + 1
                if MinSquare == 0:
                    optimalMove = "Right"
                else:
                    optimalMove = "Left"
                    
                for j in range(0,iterations):
                    board[MinSquare + j][BotRowSquare] = optimalMove
                    board[MinSquare + j][TopRowSquare] = optimalMove
                    
                    if MinSquare + j == MaxSquare: #FOR THE EDGES OF THE WALLS
                        
                        if AItankYSquare <= OPPtankYSquare: 
                            if 3 <= P2tankX % 50 <= 7: #MUST HAVE ENOUGH ROOM TO TURN
                                board[MinSquare][BotRowSquare] = "Down"
                                board[MinSquare][TopRowSquare] = "Down"
                            if 43 <= P2tankX % 50 <= 47:
                                board[MaxSquare][BotRowSquare] = "Down"
                                board[MaxSquare][TopRowSquare] = "Down"
                        else:
                            if 3 <= P2tankX % 50 <= 7:
                                board[MinSquare][BotRowSquare] = "Up"
                                board[MinSquare][TopRowSquare] = "Up"
                            if 43 <= P2tankX % 50 <= 47:
                                board[MaxSquare][BotRowSquare] = "Up"
                                board[MaxSquare][TopRowSquare] = "Up"
                            
            else: #IF WALL IS VERTICAL
                
                TopColumnSquare = int(WallLevels[i]/50)   
                BotColumnSquare = TopColumnSquare - 1
                if TopColumnSquare > 23:
                    TopColumnSquare = 23
                if BotColumnSquare < 0:
                    BotColumnSquare = 0
                MinSquare = int((WallMins[i] - 200)/50)
                MaxSquare = int((WallMaxs[i] - 200)/50)
                if MaxSquare > 13:
                    MaxSquare = 13
                if WallMins[i] % 50 == 0 and MinSquare > 0:
                    MinSquare -= 1
                iterations = MaxSquare - MinSquare + 1
                if MinSquare == 0:
                    optimalMove = "Down"
                    if MaxSquare == 13: #SPECIAL TEST CASE SCENARIO
                        if tankY <= P2tankY:
                            optimalMove = "Up"
                        else:
                            optimalMove = "Down"
                else:
                    optimalMove = "Up"
                    
                for j in range(0,iterations):
                    board[TopColumnSquare][MinSquare + j] = optimalMove
                    board[BotColumnSquare][MinSquare + j] = optimalMove
                    
                    if MinSquare + j == MaxSquare: #FOR THE EDGES OF THE WALLS
                        
                        if AItankXSquare <= OPPtankXSquare:
                            if 3 <= P2tankY % 50 <= 7: #MUST HAVE ENOUGH ROOM TO TURN
                                board[TopColumnSquare][MinSquare] = "Right"
                                board[BotColumnSquare][MinSquare] = "Right"
                            if 43 <= P2tankY % 50 <= 47:
                                board[TopColumnSquare][MaxSquare] = "Right"
                                board[BotColumnSquare][MaxSquare] = "Right"
                        else:
                            if 3 <= P2tankY % 50 <= 7:
                                board[TopColumnSquare][MinSquare] = "Left"
                                board[BotColumnSquare][MinSquare] = "Left"
                            if 43 <= P2tankY % 50 <= 47:
                                board[TopColumnSquare][MaxSquare] = "Left"
                                board[BotColumnSquare][MaxSquare] = "Left"

        #CARRYING OUT DESIRED MOVE
                        
        DesiredMove = board[AItankXSquare][AItankYSquare]

        if DesiredMove == "Up": #ANGLES TANK BASED ON MOVE, THEN BEGINS TO MOVE FORWARD
            if abs(PA - radians(90)) < radians(2):
                P2Up = True
            elif radians(90) < PA <= radians(270):
                P2Right = True
            else:
                P2Left = True
        elif DesiredMove == "Down":
            if abs(PA - radians(270)) < radians(2): #IF THE ANGLE IS CLOSE ENOUGH TO DESIRED ANGLE, MOVES ACCORDINGLY (CREATED AS A RESULT OF PYTHON ROUNDING SINCE EXACT VALUES WILL NOT WORK IN SOME CASES)
                P2Up = True
            elif radians(90) <= PA < radians(270):
                P2Left = True
            else:
                P2Right = True
        elif DesiredMove == "Left":
            if abs(PA - radians(180)) < radians(2):
                P2Up = True
            elif 0 <= PA < radians(180):
                P2Left = True
            else:
                P2Right = True
        else:
            if PA < radians(2) or radians(360) - PA < radians(2):
                P2Up = True
            elif 0 < PA <= radians(180):
                P2Right = True
            else:
                P2Left = True
            
    else:
        
        #AI ANGLES ITSELF
        #TURNS LEFT AND RIGHT 
        #SHOOTS
        
        angles = []

        #FINDS ANGLES BETWEEN PLAYER 2'S TANK AND THE 4 CORNER TIPS OF PLAYER 1'S TANK
        #ANGLES PLAYER 2'S TANK BETWEEN THE MIN AND MAX ANGLES IN ORDER TO HIT THE OPPONENT

        #ANGLE FROM PLAYER 2 TO FIRST POINT OF PLAYER 1'S TANK
        
        h = GetDist(xR1,yR1,P2tankX,P2tankY)
        x = abs(xR1 - P2tankX)
        OppTheta = acos(x/h)
        if P2tankY > yR1 and P2tankX > xR1:
            OppTheta = radians(180) - OppTheta
        elif P2tankY <= yR1 and P2tankX >= xR1:
            OppTheta = radians(180) + OppTheta
        elif P2tankY < yR1 and P2tankX < xR1:
            OppTheta = radians(360) - OppTheta
        angles.append(OppTheta)

        #ANGLE FROM PLAYER 2 TO SECOND POINT OF PLAYER 1'S TANK
        
        h = GetDist(xR2,yR2,P2tankX,P2tankY)
        x = abs(xR2 - P2tankX)
        OppTheta = acos(x/h)
        if P2tankY > yR2 and P2tankX > xR2:
            OppTheta = radians(180) - OppTheta
        elif P2tankY <= yR2 and P2tankX >= xR2:
            OppTheta = radians(180) + OppTheta
        elif P2tankY < yR2 and P2tankX < xR2:
            OppTheta = radians(360) - OppTheta
        angles.append(OppTheta)

        #ANGLE FROM PLAYER 2 TO THIRD POINT OF PLAYER 1'S TANK
        
        h = GetDist(xL3,yL3,P2tankX,P2tankY)
        x = abs(xL3 - P2tankX)
        OppTheta = acos(x/h)
        if P2tankY > yL3 and P2tankX > xL3:
            OppTheta = radians(180) - OppTheta
        elif P2tankY <= yL3 and P2tankX >= xL3:
            OppTheta = radians(180) + OppTheta
        elif P2tankY < yL3 and P2tankX < xL3:
            OppTheta = radians(360) - OppTheta
        angles.append(OppTheta)

        #ANGLE FROM PLAYER 2 TO FOURTH POINT OF PLAYER 1'S TANK
        
        h = GetDist(xL4,yL4,P2tankX,P2tankY)
        x = abs(xL4 - P2tankX)
        OppTheta = acos(x/h)
        if P2tankY > yL4 and P2tankX > xL4:
            OppTheta = radians(180) - OppTheta
        elif P2tankY <= yL4 and P2tankX >= xL4:
            OppTheta = radians(180) + OppTheta
        elif P2tankY < yL4 and P2tankX < xL4:
            OppTheta = radians(360) - OppTheta
        angles.append(OppTheta)
        
        MinAngle = min(angles[0],angles[1],angles[2],angles[3])
        MaxAngle = max(angles[0],angles[1],angles[2],angles[3])

        PA = P2tankTheta % radians(360)

        #DETERMINES RANGE

        Check = MinAngle <= PA <= MaxAngle
        switch = False
        
        if MaxAngle - MinAngle > radians(180):
            Check = MaxAngle <= PA <= MinAngle + radians(360)
            switch = True

        #ANGLES ITSELF AND SHOOTS
            
        if Check == True:
            P2Firing = True
        elif abs(MinAngle - PA) <= radians(180) and MinAngle > PA or abs(MinAngle + radians(360) - PA) <= radians(180) and MinAngle < PA: #MUST ACCOUNT FOR UNIT CIRCLE - RESETTING ANGLE VALUE FROM 360 TO 0
            P2Left = True
        elif switch == True:
            if abs(MaxAngle - PA) <= radians(180) and MaxAngle > PA:
                P2Left = True
        else:
            P2Right = True 
    
    
def P2updateTankPosition(): #UPDATES PLAYER 2'S POSITION 

    global P2tank,P2tankTop,P2Cannon,P2TreadR,P2TreadL,P2X3,P2Y3,P2X4,P2Y4
    global P2tankX,P2tankY,P2tankTheta
    global P2xR1,P2yR1,P2xR2,P2yR2,P2xL3,P2yL3,P2xL4,P2yL4,TESTP2xR1,TESTP2yR1,TESTP2xR2,TESTP2yR2,TESTP2xL3,TESTP2yL3,TESTP2xL4,TESTP2yL4
    global P2Up,P2Down,P2Left,P2Right

    if AI == True: #IF "1 PLAYER MODE" HAS BEEN SELECTED, AI TAKES CONTROL OF PLAYER 2'S TANK
        
        global WallHitMoves,LastWallHit

        AIMove()

    #TESTS TO CHECK IF MOVE IS VALID
    
    if P2Up == True:
        P2tankX += cos(P2tankTheta)*tankSpeed
        P2tankY -= sin(P2tankTheta)*tankSpeed
        
    if P2Down == True:
        P2tankX -= cos(P2tankTheta)*tankSpeed
        P2tankY += sin(P2tankTheta)*tankSpeed

    if P2Left == True:
        P2tankTheta += radians(3)

    if P2Right == True:
        P2tankTheta -= radians(3)

    #CALCULATE MAIN 4 POUNTS FIRST

    P2Xref = P2tankX + sin(P2tankTheta)*(tankW/2 + TreadW)
    P2Yref = P2tankY + cos(P2tankTheta)*(tankW/2 + TreadW)

    TESTP2xR1 = P2Xref - cos(P2tankTheta)*TreadH/2
    TESTP2yR1 = P2Yref + sin(P2tankTheta)*TreadH/2
    TESTP2xR2 = P2Xref + cos(P2tankTheta)*TreadH/2
    TESTP2yR2 = P2Yref - sin(P2tankTheta)*TreadH/2

    P2Xref = P2tankX - sin(P2tankTheta)*(tankW/2)
    P2Yref = P2tankY - cos(P2tankTheta)*(tankW/2)

    TESTP2xL1 = P2Xref - cos(P2tankTheta)*TreadH/2
    TESTP2yL1 = P2Yref + sin(P2tankTheta)*TreadH/2
    TESTP2xL2 = P2Xref + cos(P2tankTheta)*TreadH/2
    TESTP2yL2 = P2Yref - sin(P2tankTheta)*TreadH/2

    TESTP2xL3 = TESTP2xL2 - sin(P2tankTheta)*TreadW
    TESTP2yL3 = TESTP2yL2 - cos(P2tankTheta)*TreadW
    TESTP2xL4 = TESTP2xL1 - sin(P2tankTheta)*TreadW
    TESTP2yL4 = TESTP2yL1 - cos(P2tankTheta)*TreadW

    if CheckIfHitWall(2) == True or CheckPlayerOverlap(2) == True:
        
        #IF PLAYER 2 HIT A WALL OR THE OPPONENT
        #THEN REVERSES MOVE

        if AI == True:
            for i in range(0,len(WallHitMoves)):
                WallHitMoves[i] = 0
            LastWallHit = 20
        
        if P2Up == True:
            P2tankX -= cos(P2tankTheta)*tankSpeed
            P2tankY += sin(P2tankTheta)*tankSpeed
            if AI == True:
                WallHitMoves[0] = 1    
        P2Up = False
            
        if P2Down == True:
            P2tankX += cos(P2tankTheta)*tankSpeed
            P2tankY -= sin(P2tankTheta)*tankSpeed
            if AI == True:
                WallHitMoves[1] = 1
        P2Down = False

        if P2Left == True:
            P2tankTheta -= radians(3)
            if AI == True:
                WallHitMoves[2] = 1
        P2Left = False

        if P2Right == True:
            P2tankTheta += radians(3)
            if AI == True:
                WallHitMoves[3] = 1
        P2Right = False

    #TANK BODY
    
    P2theta1 = P2tankTheta - tankSETTheta
    P2theta2 = P2tankTheta + tankSETTheta

    P2xA = P2tankX + cos(P2theta1)*tankR
    P2xB = P2tankX + cos(P2theta2)*tankR
    P2yA = P2tankY - sin(P2theta1)*tankR
    P2yB = P2tankY - sin(P2theta2)*tankR

    P2xA2 = P2tankX - cos(P2theta1)*tankR
    P2xB2 = P2tankX - cos(P2theta2)*tankR
    P2yA2 = P2tankY + sin(P2theta1)*tankR
    P2yB2 = P2tankY + sin(P2theta2)*tankR

    #TANK CANNON VALUES

    P2X1 = P2tankX + sin(P2tankTheta)*CannonW/2
    P2Y1 = P2tankY + cos(P2tankTheta)*CannonW/2
    P2X2 = P2tankX - sin(P2tankTheta)*CannonW/2
    P2Y2 = P2tankY - cos(P2tankTheta)*CannonW/2

    P2X3 = P2X2 + cos(P2tankTheta)*CannonH
    P2Y3 = P2Y2 - sin(P2tankTheta)*CannonH
    P2X4 = P2X1 + cos(P2tankTheta)*CannonH
    P2Y4 = P2Y1 - sin(P2tankTheta)*CannonH

    #TANK TREAD VALUES

    #RIGHT TREAD

    P2Xref = P2tankX + sin(P2tankTheta)*(tankW/2 + TreadW)
    P2Yref = P2tankY + cos(P2tankTheta)*(tankW/2 + TreadW)

    P2xR1 = P2Xref - cos(P2tankTheta)*TreadH/2
    P2yR1 = P2Yref + sin(P2tankTheta)*TreadH/2
    P2xR2 = P2Xref + cos(P2tankTheta)*TreadH/2
    P2yR2 = P2Yref - sin(P2tankTheta)*TreadH/2

    P2xR3 = P2xR2 - sin(P2tankTheta)*TreadW
    P2yR3 = P2yR2 - cos(P2tankTheta)*TreadW
    P2xR4 = P2xR1 - sin(P2tankTheta)*TreadW
    P2yR4 = P2yR1 - cos(P2tankTheta)*TreadW

    #LEFT TREAD

    P2Xref = P2tankX - sin(P2tankTheta)*(tankW/2)
    P2Yref = P2tankY - cos(P2tankTheta)*(tankW/2)

    P2xL1 = P2Xref - cos(P2tankTheta)*TreadH/2
    P2yL1 = P2Yref + sin(P2tankTheta)*TreadH/2
    P2xL2 = P2Xref + cos(P2tankTheta)*TreadH/2
    P2yL2 = P2Yref - sin(P2tankTheta)*TreadH/2

    P2xL3 = P2xL2 - sin(P2tankTheta)*TreadW
    P2yL3 = P2yL2 - cos(P2tankTheta)*TreadW
    P2xL4 = P2xL1 - sin(P2tankTheta)*TreadW
    P2yL4 = P2yL1 - cos(P2tankTheta)*TreadW

    #DELETES OLD TANK PARTS

    s.delete(P2tank,P2Cannon,P2tankTop,P2TreadR,P2TreadL)

    #CREATES NEW TANK PARTS

    P2tank = s.create_polygon(P2xA,P2yA,P2xB,P2yB,P2xA2,P2yA2,P2xB2,P2yB2,fill = P2TankC,outline = "black",width = 2)
    P2Cannon = s.create_polygon(P2X1,P2Y1,P2X2,P2Y2,P2X3,P2Y3,P2X4,P2Y4,fill = P2TankC,outline = "black",width = 2)
    P2tankTop = s.create_oval(P2tankX - tankTopR,P2tankY - tankTopR,P2tankX + tankTopR,P2tankY + tankTopR,fill = P2TankC,width = 2)
    P2TreadR = s.create_polygon(P2xR1,P2yR1,P2xR2,P2yR2,P2xR3,P2yR3,P2xR4,P2yR4,fill = "black",width = 2)
    P2TreadL = s.create_polygon(P2xL1,P2yL1,P2xL2,P2yL2,P2xL3,P2yL3,P2xL4,P2yL4,fill = "black",width = 2)


def endGame(): #DETERMINES WINNER AND THEN ENDS THE GAME

    #DELETES TANKS
    
    s.delete(tank,Cannon,tankTop,TreadR,TreadL,P2tank,P2Cannon,P2tankTop,P2TreadR,P2TreadL)

    #GAME OVER MESSAGE
    
    GameOver = s.create_text(600,450,text = "Game Over",fill = "black",font = "Arial 50")
    s.update()
    sleep(2)
    s.delete(GameOver)
    
    if P1Life > P2Life:
        msg = "Player 1 Wins!"
    elif P1Life == P2Life:
        msg = "Tie!"
    else:
        if AI == True:
            msg = "Computer Wins!"
        else:
            msg = "Player 2 Wins!"

    #DISPLAYS MESSAGE AND DESTROYS THE WINDOW
            
    s.create_text(600,450,text = msg,fill = "black",font = "Arial 50")
    s.update()
    sleep(2)
    root.destroy()


def Countdown(): #PERFORMS A COUNTDOWN BEFORE THE MATCH

    global CountdownCheck
    
    for i in range(0,3):
        
        numberShade = s.create_text(601,451,text = str(3 - i),fill = "grey",font = "Arial 50")
        number = s.create_text(600,450,text = str(3 - i),fill = "black",font = "Arial 50")
        s.update()
        sleep(1)
        s.delete(number,numberShade)

    #ARTISTIC SHADE FOR VISUAL APPEAL
        
    goShade = s.create_text(601,451,text = "Go!",fill = "grey",font = "Arial 50")
    go = s.create_text(600,450,text = "Go!",fill = "black",font = "Arial 50")
    s.update()
    sleep(1)
    s.delete(go,goShade)

    CountdownCheck = False
    

def DeleteOverlapAmmo(): #DELETES OVERLAPPING AMMO PARTICLES
    
    i = len(AmmoParticles) - 1 #CHECKS IF ANY TWO PARTICLES OVERLAP
    while i >= 0:
        j = len(AmmoParticles) - 1
        removed = False
        while j >= 0 and removed == False:
            NumRemoved = 0
            if i != j and AmmoOwners[i] != AmmoOwners[j]:
                
                if GetDist(AmmoXs[i],AmmoYs[i],AmmoXs[j],AmmoYs[j]) <= AmmoR*2:
                    
                    s.delete(AmmoParticles[i],AmmoParticles[j])

                    crater = s.create_oval(AmmoXs[i] - 10,AmmoYs[i] - 10,AmmoXs[i] + 10,AmmoYs[i] + 10,fill = "black")
                    Craters.append(crater)
                    
                    AmmoParticles.remove(AmmoParticles[i])
                    AmmoXs[i] = "A"
                    AmmoXs.remove(AmmoXs[i])
                    AmmoYs[i] = "A" #MUST RESET VALUE BEFORE REMOVING OTHERWISE A BUG MAY OCCUR
                    AmmoYs.remove(AmmoYs[i])
                    AmmoThetas[i] = "A"
                    AmmoThetas.remove(AmmoThetas[i])
                    AmmoOwners[i] = 0 
                    AmmoOwners.remove(AmmoOwners[i])

                    AmmoParticles.remove(AmmoParticles[j])
                    AmmoXs[j] = "A"
                    AmmoXs.remove(AmmoXs[j])
                    AmmoYs[j] = "A"
                    AmmoYs.remove(AmmoYs[j])
                    AmmoThetas[j] = "A"
                    AmmoThetas.remove(AmmoThetas[j])
                    AmmoOwners[j] = 0 
                    AmmoOwners.remove(AmmoOwners[j])

                    removed = True
                    NumRemoved = 1

            j -= 1
            i -= NumRemoved
            
        i -= 1
        

def RemoveCraters(): #DELETES CRATERS LEFT BY AMMO PARTICLES HITTING THE WALL OR OTHER AMMO PARTICLES

    global Craters

    if len(Craters) > 0:    
        for i in range(0,len(Craters)):
            s.delete(Craters[0])
            Craters.remove(Craters[0])
                    

def runGame(): #MAIN GAME 

    #INITIAL SETUP
    
    CreateWalls()
    
    SetInitialValues()
    SetInitialValuesP2()
    SetHealthBars()

    #MAIN SCREEN
    
    CreateMainScreen()

    while Ready == False: #STAYS ON MAIN SCREEN UNTIL A BUTTON HAS BEEN PRESSED
        s.update() #UPDATES SCREEN TO CHECK FOR MOUSE PRESSING BUTTON

    DeleteMainScreen()

    #STARTS MATCH
    
    Countdown()

    while Escape == False and P1Life > 0 and P2Life > 0: #RUNS BATTLE WHILE THE ESCAPE KEY HAS NOT BEEN PRESSED AND BOTH PLAYERS ARE ALIVE

        #UPDATES POSITIONS

        updateTankPosition()
        P2updateTankPosition()

        #IF A PLAYER IS FIRING AND RELOADED, CREATES AMMO

        if P1Firing == True and CheckIfReloaded(1) == True:
            MakeNewAmmo(1)
        if P2Firing == True and CheckIfReloaded(2) == True:
            MakeNewAmmo(2)
            
        UpdateAmmoPosition()
        CheckIfAmmoHitWall()
        DrawAmmo()
        DeleteOverlapAmmo()
        
        s.update()
        sleep(0.03)

        #DELETES VARIOUS GRAPHICS
        
        RemoveCraters()
        CheckIfPlayerHit()
        deleteAmmo()

    #ENDS MATCH
        
    endGame()
    

root.after(0,runGame)

s.focus_set()

#KEY BINDINGS

s.bind("<Key>",KeyPressHandler)
s.bind("<KeyRelease>", KeyReleaseHandler)
s.bind("<Button-1>",ClickHandler)
        
root.mainloop()
