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
import matplotlib.pyplot as plt
'''''' 
RAD2DEG=math.pi/180
tstep=0.05
baseName='Plane'
jointName='joint'
t=np.linspace(0,2,200,endpoint=False)
x=np.pi*t**2
#t=np.linspace(0,0.5*np.pi,200,endpoint=False)
#x=4*np.pi*np.sin(t)
print('Program started')

sim.simxFinish(-1)

while True:
    clientID=sim.simxStart('127.0.0.1',19997,True,True,5000,5)
    sim.simxStartSimulation(clientID,sim.simx_opmode_oneshot)
    sim.simxSynchronous(clientID,True)
    sim.simxSynchronousTrigger(clientID)
    
    if clientID !=-1:
        break
    else:
        time.sleep(0.2)
        print('Fail connecting to remote API Server !')
print('Connection success !')

''''''
_,baseHandle=sim.simxGetObjectHandle(clientID,baseName,sim.simx_opmode_blocking)
_,jointHandle=sim.simxGetObjectHandle(clientID,jointName,sim.simx_opmode_blocking)
print('Handles available')
     

while sim.simxGetConnectionId(clientID) !=-1:
    time.sleep(5)
    sim.simxSetFloatingParameter(clientID,sim.sim_floatparam_simulation_time_step,tstep,sim.simx_opmode_blocking)#设置仿真步长，保持API端和Server端相同步长
    for i in range(200):
        _,jpos=sim.simxGetJointPosition(clientID,jointHandle,sim.simx_opmode_streaming)
        print(jpos/RAD2DEG)
        
        sim.simxSetJointTargetPosition(clientID,jointHandle,x[i],sim.simx_opmode_streaming)
        sim.simxSynchronous(clientID,True)
        sim.simxSynchronousTrigger(clientID)
        
    sim.simxStopSimulation(clientID,sim.simx_opmode_oneshot)
    sim.simxFinish(-1)

t=[]
for i in range(200):
    t.append(0.05*i)

#afa=-4*np.pi*np.sin(t)*(0.5*np.pi/10)*(0.5*np.pi/10)
afa=np.array([2*np.pi for i in range(200)])
print(afa)
T=0.5*10*0.05**2*afa

plt.subplot()
plt.plot(t,T)