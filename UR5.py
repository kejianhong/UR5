# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 18:11:01 2020

@author: KJH
"""
from __future__ import division
import numpy as np
import math
import time
import sim
''''''
RAD2DEG=math.pi/180
tstep=0.05

jointNum=6  
baseName='UR5'
jointName='UR5_joint'

#''' state1 q1,dt=0.05'''
#t=np.linspace(0,0.5*np.pi,400,endpoint=False)
#x=4*np.pi*np.sin(t)
#'''state1 q2,dt=0.05'''
#t=np.linspace(0,4*np.pi,400,endpoint=False)
#x=0.5*np.pi*np.sin(t)-0.5*np.pi
#'''state1 q3,dt=0.05'''
#t=np.linspace(0,4*np.pi,400,endpoint=False)
#x=0.5*np.pi*np.sin(t)
#'''state1 q4,dat=0.05'''
#t=np.linspace(0,0.5*np.pi,400,endpoint=False)
#x=4*np.pi*np.sin(t)-0.5*np.pi
'''state2 q5,dt=0.05'''
t=np.linspace(0,0.5*np.pi,400,endpoint=False)
x=4*np.pi*np.sin(t)
#'''q6'''
#t=np.linspace(0,0.5*np.pi,400,endpoint=False)
#x=4*np.pi*np.sin(t)

print('Program started')

''''''
sim.simxFinish(-1)

while True:
    clientID=sim.simxStart('127.0.0.1',19997
                           ,True,True,5000,5)
    sim.simxStartSimulation(clientID,sim.simx_opmode_oneshot)
    sim.simxSynchronous(clientID,True)
    sim.simxSynchronousTrigger(clientID)

    if clientID !=-1:
        break
    else:
        time.sleep(0.2)
        print('Fail connecting to remote API Server !')
print('Connection success !')


_,baseHandle=sim.simxGetObjectHandle(clientID,baseName,sim.simx_opmode_blocking)
jointHandle=np.zeros((jointNum,),dtype=int)
for i in range(jointNum):
    _,returnHandle=sim.simxGetObjectHandle(clientID,jointName+str(i+1),sim.simx_opmode_blocking)
    jointHandle[i]=returnHandle
print('Handles available')

sim.simxSetFloatingParameter(clientID,sim.sim_floatparam_simulation_time_step,tstep,sim.simx_opmode_blocking)

jointConfig=np.zeros((jointNum,))   
''''''

lastCmdTime=sim.simxGetLastCmdTime(clientID)

while sim.simxGetConnectionId(clientID) !=-1:
    time.sleep(2)
    lastCmdTime=sim.simxGetLastCmdTime(clientID)
    
    for i in range(400):
        currentCmdTime=sim.simxGetLastCmdTime(clientID)
        dt=currentCmdTime-lastCmdTime
        print(i)
        for k in range(jointNum):
            _,jointPosition=sim.simxGetJointPosition(clientID,jointHandle[k],sim.simx_opmode_streaming)
            jointConfig[k]=jointPosition
        print(jointConfig[4]/RAD2DEG)
        
        for m in range(4,5):
            sim.simxSetJointTargetPosition(clientID,jointHandle[m],x[i],sim.simx_opmode_oneshot)
        sim.simxSynchronous(clientID,True)
        sim.simxSynchronousTrigger(clientID)
        lastCmdTime=currentCmdTime

    sim.simxFinish(-1)

