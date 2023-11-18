import serial
import time
import math
import numpy as np
import matplotlib.pyplot as plt
# from mpl_toolkits import mplot3d
import csv
import pandas as pd
from matplotlib.animation import FuncAnimation

### Create a csv file ###
header = ['Degree', 'XCoordinate', 'YCoordinate']
with open('storeData.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

# Create a struct #
class my2DStruct:
    # value1: store yawDegree
    # value2: store distance 
    def __init__ (self, value1, value2):
        self.value1= value1
        self.value2= value2

# Create a two dimension array to store and implement filter with 3 row/ 5000 collumm # 
array_2d = [[my2DStruct(0.0, 0.0) for _ in range(8000)] for _ in range(5)]
xAxes=[]
yAxes=[]
posArray= []

# Define function drawing 3D Mapping 
def drawing3D():
    # myFigure = plt.figure(dpi=200, figsize=(10,10))
    # ax = plt.axes(projection ='3d')
    xAxes=[]
    yAxes=[]
    zAxes=[]
    
    xAxes1=[]
    yAxes1=[]
    zAxes1=[]
    
    xAxes2=[]
    yAxes2=[]
    zAxes2=[]
    
    limit_of_data = True
    changePOV= True
    # Read file to store # 
    with open("data3D.txt", "a") as file:
       while limit_of_data:
           while arduino.in_waiting == 0:
                pass
            # Read data from arduino # 
           dataPacket = arduino.readline()
           dataPacket  = str(dataPacket, 'utf-8')    
           dataPacket  = dataPacket.strip('\r\n')
           if (dataPacket == 'End Data'):
                limit_of_data = False
           else:
                # Calculate to draw 3D # 
                splitData = dataPacket.split(',')
                dist    = float(splitData[2])
                pitch   = float(splitData[1]) *3.14/180
                yaw     = float(splitData[0]) *3.14/180
                
                xAxes.append(dist*(np.cos(pitch))*(np.cos(yaw)))
                yAxes.append(dist*(np.cos(pitch))*(np.sin(yaw)))
                zAxes.append(dist*(np.sin(pitch)))
                
                if(yaw>0 and yaw<=3.14):
                    xAxes1.append(dist*(np.cos(pitch))*(np.cos(yaw)))
                    yAxes1.append(dist*(np.cos(pitch))*(np.sin(yaw)))
                    zAxes1.append(dist*(np.sin(pitch)))
                    
                elif(yaw>3.14 and yaw<=6.28):
                    xAxes2.append(dist*(np.cos(pitch))*(np.cos(yaw)))
                    yAxes2.append(dist*(np.cos(pitch))*(np.sin(yaw)))
                    zAxes2.append(dist*(np.sin(pitch)))

                
                xTemp= dist*(np.cos(pitch))*(np.cos(yaw))               
                yTemp= dist*(np.cos(pitch))*(np.sin(yaw))
                zTemp= dist*(np.sin(pitch))
                
                print(xTemp,yTemp,zTemp, dist)
                
                file.write(str(xTemp) + " " + str(yTemp) + " " + str(zTemp))
                file.write('\n')
    
    # loop to input and display user-defined elev, azim, roll
    while changePOV:
        # get user input for elev, azim, roll
        elev = input("Enter the elevation angle in degrees: ")
        if elev == 'end':
            changePOV= False
            break
        elev = int(elev)

        azim = input("Enter the azimuth angle in degrees: ")
        if azim == 'end':
            changePOV= False
            break
        azim = int(azim)

        roll = input("Enter the roll angle in degrees: ")
        if roll == 'end':
            changePOV= False
            break
        roll = int(roll)
        
        POVMode= input("Enter the POVMode: ")
        if POVMode== 'end':
            changePOV= False
            break
        POVMode= int(POVMode) 
        # POVMode=1 to view 0-180 || POVMode=2 to view 180-360 || POVMode=0 To view full
        
        
        if(1==POVMode):
            myFigure = plt.figure(dpi=200, figsize=(10,10))
            ax1 = plt.axes(projection ='3d')
            ax1.view_init(elev, azim, roll)  
            ax1.scatter(xAxes1,yAxes1,zAxes1,s=0.1,c='green')
            ax1.scatter(xAxes1[0], yAxes1[0ion ='3d')
            ax2.view_init(elev, azim, roll)  
            ax2.scatter(xAxes2,yAxes2,zAxes2,s=0.1,c='green')
            ax2.scatter(xAxes2[0], yAxes2[0], zAxes2[0], s=30, c = 'red')
            plt.title('Elevation: %d°, Azimuth: %d°, Roll: %d°' % (elev, azim, roll))
            # display the plot
            plt.show()
        
        else:
            myFigure = plt.figure(dpi=200, figsize=(10,10))
            ax = plt.axes(projection ='3d')
            ax.view_init(elev, azim, roll)  
            ax.scatter(xAxes,yAxes,zAxes,s=0.1,c='green')
            ax.scatter(xAxes[0], yAxes[0], zAxes[0], s=30, c = 'red')
            plt.title('Elevation: %d°, Azimuth: %d°, Roll: %d°' % (elev, azim, roll))
            # display the plot
            plt.show()       

# Use for collect only 1 yawDegree #
def checkInArray(value):
    idx=0

    # If posArray is empty -> Get the value to Array # 
    if(len(posArray)==0):
         posArray.append(value)
    # Else if posArray already has -> return 0 to not add to Array # 
    else:
        for idx in range(len(posArray)):
            if(value== posArray[idx]):
                return 0
        return 1


# Process Array to get posArray that is an array to store only one value for each yawDegree # 
def processArray():
    idx=0
    for idx in range(8000):                                    
        if(checkInArray(array_2d[0][idx].value1)==1):
            posArray.append(array_2d[0][idx].value1)

# Function to calculate rootMeanSquare of each yawDegree # 
def calculateRootMeanSquare(value):
    idxRow=0
    idxCollum=0
    count=1
    RMS=0

    # idxRow here need to adjust ( Because now is setting 3 rounds -> range 2 is enough )
    # This function will scan for all -> Find the yawDegree to calculate the mean of value # 
    for idxRow in range(5):
        for idxCollum in range(8000):
            if(array_2d[idxRow][idxCollum].value1== value and array_2d[idxRow][idxCollum].value2 !=0 and array_2d[idxRow][idxCollum].value2 <500):
                RMS= RMS + array_2d[idxRow][idxCollum].value2* array_2d[idxRow][idxCollum].value2
                count= count+1
                break
    return math.sqrt(RMS/count)

                

# Function to call each yawDegree to calculate rootMeanSquare       
def rootMeanSquare():
    idx=0
    RMSResult=0

    # For idx of posArray to calculate the mean of its yawDegree | For example: at yawDegree: 0.8 -> We have 0.7; 1.0 -> Get the mean of its distance #
    for idx in range(len(posArray)):
        RMSResult=calculateRootMeanSquare(posArray[idx])

        # Calculate xAxesValue and yAxesValue to draw 
        xAxesValue= RMSResult*(np.cos(posArray[idx]*3.14/180))
        yAxesValue= RMSResult*(np.sin(posArray[idx]*3.14/180))
        xAxes.append(xAxesValue)
        yAxes.append(yAxesValue)

        # This writeList is to store in file # 
        writeList = [posArray[idx], xAxesValue, yAxesValue]
        with open('storeData.csv', 'a', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(writeList)        
    

# Define function drawing 2D Mapping
def drawing2D():

    # Create a new figure #
    fig, ax = plt.subplots()

    # Variable to check limit of round to measure # 
    limit_of_data = True

    # Round of array to draw 2D # 
    rowOfArray=0

    # Collum of array to draw 3D # 
    # If collumofArray==0 -> Draw 2D #
    collumOfArray=0

    # Start while # 
    while limit_of_data:
        while arduino.in_waiting == 0:
            pass

        # Read line sent from arduino depending on Mode #
        # Process the dataPacket receiving from arduino # 
        dataPacket = arduino.readline()
        dataPacket  = str(dataPacket, 'utf-8')    
        dataPacket  = dataPacket.strip('\r\n')
        print(dataPacket)
        
        # If dataPacket == End Data -> Stop ! # 
        if (dataPacket == 'End Data'):
            limit_of_data = False
        # If dataPacket == Round up -> Increase size of array to store value -> Draw # 
        elif (dataPacket == 'Round Up'):
            rowOfArray= rowOfArray+1
            collumOfArray=0   
                     
        else:
            # Get the line from arduino # 
            splitData = dataPacket.split(',')
            # [0] : PosX 0-> 360 
            # [1] : PosY 0-> 360 
            # [2] : distance get from arduino 
            yawDegree= float(splitData[0])
            dist    = float(splitData[2])

            # Set value yawDegree to PosX (value1) || Set value dist -> value2 #
            array_2d[rowOfArray][collumOfArray].value1= yawDegree
            array_2d[rowOfArray][collumOfArray].value2= dist
          
            # Each + 1 collumm -> up round +1 #
            collumOfArray= collumOfArray+1
            # Print to console #
            print(yawDegree,dist)

            ax.clear

    # End while # 

    # Process Array to get the quality of 2D mapping # 
    # Process to get an Array of each distance #
    processArray()

    # Then when get the Array of each distance -> Process to get rootMeanSquare and get to xAxes, yAxes to draw # 
    rootMeanSquare()
    
    # Add to draw # 
    ax.scatter(xAxes,yAxes,s=0.1,c='green')
    
    for i in range(1600):
        ax.scatter(xAxes[i],yAxes[i],s=0.1,c='red')

    ax.scatter(0, 0, s=30, c = 'red')
    ax.set_xlim(-400, 400)
    ax.set_ylim(-400, 400)
    plt.show()


### Start main thread of programme ###

# Connect with arduino through serial 
arduino = serial.Serial(
    port='COM7',
    baudrate=115200
)

# Delay time
time.sleep(1)

# Variable to control program working or not #       
programWorking= True


while programWorking:
    # Three modes: 0: Stop Lidar || 1: 2D 5 rounds || 2: 3D 90 degree pitch (Test may be 20 degree )
    # Taking input from user

    print("Waiting for input number: ")
    modeWorking = input("Enter a mode working: ")

    # robot_pos_x = float(input("Enter robot x_position: "))
    # robot_pos_y = float(input("Enter robot y_position: "))
    # robot_pos_z = float(input("Enter robot z_position: "))

    # Send to arduino (change modeWorking to bytes)
    arduino.write(bytes(modeWorking, 'utf-8'))

    # Delay 0.05 s 
    time.sleep(0.05)

    # Depend on which mode to start 
    if(modeWorking== '0'):
        programWorking= False
    elif (modeWorking== '1'):
        drawing2D()
    elif (modeWorking== '2'):
        drawing3D()
    
#### End Main Thread Program ####