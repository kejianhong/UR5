# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import math
import time
import sim

''''''
RAD2DEG=math.pi/180
tstep=0.1#step

#information about joint
jointNum=6
baseName='UR5'
jointName='UR5_joint'

#set the motor position
t=np.linspace(0,0.5*np.pi,200,endpoint=False)
x=2*np.pi*np.sin(t)

print('Program started')

''''''
#close all the other API
sim.simxFinish(-1)

#test per 0.2 second
while True:
    clientID=sim.simxStart('127.0.0.1',20000,True,True,5000,5)
    sim.simxStartSimulation(clientID,sim.simx_opmode_oneshot)#请求开始仿真
    if clientID !=-1:
        break
    else:
        time.sleep(0.2)
        print('Fail connecting to remote API Server !')
print('Connection success !')

''''''
#set the same step with the coppeliasim
sim.simxSetFloatingParameter(clientID,sim.sim_floatparam_simulation_time_step,tstep,sim.simx_opmode_blocking)
sim.simxSynchronous(clientID,True)#为True，client端负责触发下一个仿真程序

#get the handle of the server
_,baseHandle=sim.simxGetObjectHandle(clientID,baseName,sim.simx_opmode_blocking)#基底句柄
#get the handle of 6 joints
jointHandle=np.zeros((jointNum,),dtype=int)
for i in range(jointNum):
    _,returnHandle=sim.simxGetObjectHandle(clientID,jointName+str(i+1),sim.simx_opmode_blocking)
    jointHandle[i]=returnHandle

print('Handles available')

#get the initial position of the joints
jointConfig=np.zeros((jointNum,))
for  i in range(jointNum):
    _,jointPosition=sim.simxGetJointPosition(clientID,jointHandle[i],sim.simx_opmode_streaming)
    jointConfig[i]=jointPosition
    

lastCmdTime=sim.simxGetLastCmdTime(clientID)
sim.simxSynchronousTrigger(clientID)

#start simulation
while sim.simxGetConnectionId(clientID) !=-1:
    
    for i in range(200):
        currentCmdTime=sim.simxGetLastCmdTime(clientID)
        dt=currentCmdTime-lastCmdTime
        
        '''control code'''
        
        for j in range(jointNum):
            _,jpos=sim.simxGetJointPosition(clientID,jointHandle[j],sim.simx_opmode_buffer)
            jointConfig[j]=jpos
            
        #stop the simulation to set all the positioin of 6 joints at the same time
        sim.simxPauseCommunication(clientID,True)
        
        '''change the number here to control different joint'''
        for k in range(0,1):
            sim.simxSetJointTargetPosition(clientID,jointHandle[k],x[i],sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID,False)
        lastCmdTime=currentCmdTime
        sim.simxSynchronousTrigger(clientID)
        sim.simxGetPingTime(clientID)
    sim.simxFinish(-1)
    sim.simxStopSimulation(clientID,sim.simx_opmode_oneshot)